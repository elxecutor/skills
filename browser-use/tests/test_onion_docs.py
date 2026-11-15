import ast
import re
import unittest
from pathlib import Path


SKILL = Path(__file__).resolve().parents[1]
REFERENCE = SKILL / 'references' / 'onion-tor.md'
ONION = 'http://example.onion/'


def python_examples():
    text = REFERENCE.read_text(encoding='utf-8')
    return re.findall(r'```python\n(.*?)\n```', text, re.DOTALL)


def load_workflow():
    examples = python_examples()
    matches = [example for example in examples if '# onion-tor-workflow' in example]
    if len(matches) != 1:
        raise AssertionError('Expected exactly one onion workflow example')
    namespace = {}
    exec(compile(matches[0], str(REFERENCE), 'exec'), namespace)
    return namespace['open_tor_tab']


class Clock:
    def __init__(self):
        self.current = 0.0

    def now(self):
        return self.current

    def sleep(self, amount):
        self.current += amount


class FakeBrowser:
    def __init__(self, *, pages=None, popup=True, navigation=None,
                 navigation_error=None, complete=True, info=None, text=True,
                 source_context='tor-context', source_exists=True):
        self.source = {'targetId': 'source', 'type': 'page',
                       'browserContextId': source_context, 'url': 'about:blank'}
        self.sources = [self.source] if source_exists else []
        if pages is None:
            pages = [self.page()]
        self.pages = pages
        self.popup = popup
        self.navigation = navigation if navigation is not None else {}
        self.navigation_error = navigation_error
        self.complete = complete
        self.info = info if info is not None else {'url': ONION, 'title': 'Example'}
        self.text = text
        self.calls = []
        self.opened = False
        self.clock = Clock()

    @staticmethod
    def page(target='new', *, context='tor-context', url='about:blank',
             opener='source'):
        return {'targetId': target, 'type': 'page', 'browserContextId': context,
                'url': url, 'openerId': opener}

    def cdp(self, method, **kwargs):
        self.calls.append((method, kwargs))
        if method == 'Target.getTargets':
            return {'targetInfos': self.sources + (self.pages if self.opened else [])}
        if method == 'Target.attachToTarget':
            return {'sessionId': 'source-session'}
        if method == 'Runtime.evaluate':
            self.opened = self.popup
            return {'result': {'value': self.popup}}
        if method in ('Target.detachFromTarget', 'Page.bringToFront'):
            return {}
        if method == 'Page.navigate':
            if self.navigation_error:
                raise self.navigation_error
            return self.navigation
        raise AssertionError(f'Unexpected CDP call: {method}')

    def switch_tab(self, target, activate=False):
        self.calls.append(('switch_tab', {'target': target, 'activate': activate}))

    def wait_for_load(self, timeout):
        self.calls.append(('wait_for_load', {'timeout': timeout}))
        return self.complete

    def page_info(self):
        self.calls.append(('page_info', {}))
        return self.info

    def js(self, expression):
        self.calls.append(('js', {'expression': expression}))
        if 'slice(0, 500)' in expression:
            return 'ERR_BLOCKED_BY_CLIENT'
        return self.text

    def api(self):
        return {'cdp': self.cdp, 'switch_tab': self.switch_tab,
                'wait_for_load': self.wait_for_load, 'page_info': self.page_info,
                'js': self.js}

    def run(self, destination=ONION):
        return load_workflow()(destination, 'source', self.api(), timeout=1,
                               tab_timeout=0.2, now=self.clock.now,
                               sleep=self.clock.sleep)

    def calls_named(self, method):
        return [params for name, params in self.calls if name == method]


class DocumentationTests(unittest.TestCase):
    def test_all_python_examples_parse(self):
        examples = python_examples()
        self.assertTrue(examples, 'Reference has no runnable Python examples')
        for example in examples:
            with self.subTest(example=example[:50]):
                ast.parse(example)

    def test_main_skill_links_reference_and_retains_allow_prompt(self):
        text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
        self.assertIn('references/onion-tor.md', text)
        self.assertIn('Wait for\nthe user to click Allow', text)
        self.assertIn('.onion', text)
        self.assertIn('Tor', text)

    def test_reference_explains_privacy_and_errors(self):
        text = REFERENCE.read_text(encoding='utf-8')
        for term in ('userGesture', 'openerId', 'browserContextId', 'switch_tab',
                     'ERR_BLOCKED_BY_CLIENT', 'ERR_NETWORK_CHANGED',
                     'chrome-error:', 'wait_for_load', 'Allow'):
            with self.subTest(term=term):
                self.assertIn(term, text)


class OnionWorkflowTests(unittest.TestCase):
    def assert_not_navigated_or_activated(self, browser):
        self.assertEqual(browser.calls_named('Page.navigate'), [])
        self.assertEqual(browser.calls_named('switch_tab'), [])

    def test_unique_same_context_blank_tab_is_activated_and_navigated(self):
        browser = FakeBrowser()
        result = browser.run()
        self.assertEqual(result['status'], 'review')
        self.assertEqual(result['target_id'], 'new')
        self.assertEqual(browser.calls_named('switch_tab'),
                         [{'target': 'new', 'activate': True}])
        self.assertEqual(browser.calls_named('Page.navigate')[0]['url'], ONION)
        evaluate = browser.calls_named('Runtime.evaluate')[0]
        self.assertTrue(evaluate['userGesture'])
        self.assertIn("window.open('about:blank'", evaluate['expression'])
        self.assertNotIn(ONION, evaluate['expression'])
        self.assertEqual(len(browser.calls_named('Target.detachFromTarget')), 1)

    def test_no_new_target_does_not_navigate(self):
        browser = FakeBrowser(pages=[])
        self.assertEqual(browser.run()['status'], 'failed')
        self.assert_not_navigated_or_activated(browser)

    def test_multiple_candidates_do_not_navigate(self):
        browser = FakeBrowser(pages=[FakeBrowser.page('a'), FakeBrowser.page('b')])
        self.assertEqual(browser.run()['status'], 'failed')
        self.assert_not_navigated_or_activated(browser)

    def test_wrong_context_does_not_navigate(self):
        browser = FakeBrowser(pages=[FakeBrowser.page(context='normal-context')])
        self.assertEqual(browser.run()['status'], 'failed')
        self.assert_not_navigated_or_activated(browser)

    def test_missing_context_does_not_navigate(self):
        browser = FakeBrowser(pages=[FakeBrowser.page(context=None)])
        self.assertEqual(browser.run()['status'], 'failed')
        self.assert_not_navigated_or_activated(browser)

    def test_unexpected_initial_url_does_not_navigate(self):
        browser = FakeBrowser(pages=[FakeBrowser.page(url='https://example.org/')])
        self.assertEqual(browser.run()['status'], 'failed')
        self.assert_not_navigated_or_activated(browser)

    def test_unrelated_opener_does_not_navigate(self):
        browser = FakeBrowser(pages=[FakeBrowser.page(opener='another-tab')])
        self.assertEqual(browser.run()['status'], 'failed')
        self.assert_not_navigated_or_activated(browser)

    def test_blocked_popup_does_not_navigate(self):
        browser = FakeBrowser(popup=False)
        self.assertEqual(browser.run()['status'], 'failed')
        self.assert_not_navigated_or_activated(browser)

    def test_missing_source_context_does_not_open_or_navigate(self):
        browser = FakeBrowser(source_context=None)
        self.assertEqual(browser.run()['status'], 'failed')
        self.assertEqual(browser.calls_named('Runtime.evaluate'), [])
        self.assert_not_navigated_or_activated(browser)

    def test_missing_source_does_not_open_or_navigate(self):
        browser = FakeBrowser(source_exists=False)
        self.assertEqual(browser.run()['status'], 'failed')
        self.assertEqual(browser.calls_named('Runtime.evaluate'), [])
        self.assert_not_navigated_or_activated(browser)

    def test_non_onion_and_credentials_are_rejected(self):
        for destination in ('https://example.org/', 'http://user:pass@example.onion/',
                            'javascript:alert(1)'):
            with self.subTest(destination=destination):
                browser = FakeBrowser()
                self.assertEqual(browser.run(destination)['status'], 'failed')
                self.assertEqual(browser.calls, [])

    def test_navigation_error_is_not_success(self):
        browser = FakeBrowser(navigation={'errorText': 'net::ERR_NETWORK_CHANGED'})
        result = browser.run()
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['reason'], 'net::ERR_NETWORK_CHANGED')
        self.assertEqual(len(browser.calls_named('Page.navigate')), 1)
        self.assertEqual(browser.calls_named('wait_for_load'), [])

    def test_timeout_inspects_same_tab_without_retry(self):
        browser = FakeBrowser(navigation_error=TimeoutError('timed out'))
        result = browser.run()
        self.assertEqual(result['status'], 'pending')
        self.assertEqual(result['target_id'], 'new')
        self.assertEqual(result['observed'], browser.info)
        self.assertEqual(len(browser.calls_named('Page.navigate')), 1)
        self.assertEqual(len(browser.calls_named('page_info')), 1)

    def test_browser_error_page_is_not_success_and_reports_details(self):
        browser = FakeBrowser(info={'url': 'chrome-error://chromewebdata/', 'title': 'Error'})
        result = browser.run()
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['details'], 'ERR_BLOCKED_BY_CLIENT')

    def test_redirect_is_reported_separately(self):
        browser = FakeBrowser(info={'url': 'http://other.onion/', 'title': 'Other'})
        self.assertEqual(browser.run()['status'], 'redirect')

    def test_document_not_ready_is_pending(self):
        browser = FakeBrowser(complete=False)
        self.assertEqual(browser.run()['status'], 'pending')

    def test_blank_page_and_no_text_are_pending(self):
        for browser in (FakeBrowser(info={'url': 'about:blank'}), FakeBrowser(text=False)):
            with self.subTest(info=browser.info, text=browser.text):
                self.assertEqual(browser.run()['status'], 'pending')

    def test_download_is_not_reported_as_loaded(self):
        browser = FakeBrowser(navigation={'isDownload': True})
        self.assertEqual(browser.run()['status'], 'failed')


if __name__ == '__main__':
    unittest.main()
