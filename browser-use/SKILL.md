---
name: browser-use
description: "Control the user's Chromium browser through CDP for interactive web tasks, authenticated pages, JavaScript-rendered sites, automation, testing, screenshots, and requested .onion browsing in Brave's Tor window. Prefer direct HTTP fetching for public static content unless the user requests browser interaction or Tor."
---

# Browser Use

Direct browser control via CDP. Use `~/.agents/skills/browser-use/bu`. It installs
its own namespaced Linux cache via UV when absent and controls the user's default
Chromium browser through its approved remote-debugging connection. The cache is
`$XDG_CACHE_HOME/opencode-skills/browser-use`, not a shared global tool install.

## When Not to Use

A basic fetch of public information needs no browser. If a plain HTTP request can read it — a public page, an API, docs — use `curl` or your fetch tool, and leave the browser alone. Use browser-use when the task needs interaction (click, type, navigate), the user's logged-in session, JS rendering, or a bot-protected page. If a direct fetch fails or returns a shell page, then escalate to the browser.

When the user requests a visible browser tab or browsing over Tor, use the requested browser/session instead of substituting an HTTP probe. For `.onion` sites in Brave's native Tor window, follow [the onion/Tor workflow](references/onion-tor.md): identify the user-confirmed Tor tab and preserve its context. Do not switch to a normal browser, proxy, or different mirror without permission.

## Usage

```bash
~/.agents/skills/browser-use/bu <<'PY'
print(page_info())
PY
```

- Invoke the skill-local `bu` wrapper. Use heredocs for multi-line commands.
- Helpers are pre-imported.
- For ordinary browsing, first navigation is `new_tab(url)`, not `goto_url(url)`. This default does not select an existing Brave Tor context; use [the onion/Tor workflow](references/onion-tor.md) instead for that case.

## Local Chrome

The first real `bu` invocation starts/reuses Browser Harness' local daemon and
keeps its CDP connection open while Chrome displays any Allow prompt. **Wait for
the user to click Allow; do not give up, open another connection, or run probes.**
`--doctor` only reports health; it does not start the daemon. After a definite
daemon crash, reload it once and retry the original command:

```bash
~/.agents/skills/browser-use/bu <<'PY'
ensure_real_tab()
print(page_info())
PY

# Only after a daemon crash, not while an Allow prompt is pending:
~/.agents/skills/browser-use/bu --reload
```

Diagnostics:

```bash
~/.agents/skills/browser-use/bu --doctor
```

If the browser is not remote-debuggable, ask the user to enable it at
`chrome://inspect/#remote-debugging`, then click Allow. An explicit `BU_CDP_WS`
can intentionally select a remote browser endpoint.

If Chrome is running but remote debugging is not enabled, open:

```text
chrome://inspect/#remote-debugging
```

Tick "Allow remote debugging for this browser instance" and click Allow if a permission popup appears. Then retry.

## Page Workflow

- Prefer to find elements with the accessibility tree, not screenshots: `cdp("Accessibility.getFullAXTree")["nodes"]` has every element's role, name, and `backendDOMNodeId` — filter in Python before printing (it is thousands of nodes). Coordinates: `q = cdp("DOM.getBoxModel", backendNodeId=n)["model"]["content"]; x, y = sum(q[0::2])/4, sum(q[1::2])/4` (viewport px, ready for `click_at_xy`; negative/oversized means scroll first).
- Clicking: AX node -> box center -> `click_at_xy(x, y)` -> verify with a targeted `js(...)`/`page_info()` check.
- Fall back to raw HTML via `js(...)` only when the AX tree lacks the element (canvas, exotic widgets); screenshot when layout or imagery matters.
- After navigation, call `wait_for_load()`.
- For ordinary browsing, if the current tab is stale or internal, call `ensure_real_tab()`. Do not use it to pick a Brave Tor tab: it may select a normal tab, while a new Tor tab may itself be an internal page.
- Use `js(...)` for DOM inspection or extraction when coordinates are the wrong tool.
- Use `watch_network()` to see network requests in a dev-tool-like table.
- Login walls: stop and ask. Exception: use available SSO automatically when Chrome is already signed in; still stop for passwords, MFA, consent, or ambiguous account choice.
- Raw CDP is available with `cdp("Domain.method", ...)`.

## Recordings

```bash
~/.agents/skills/browser-use/bu recordings enable
~/.agents/skills/browser-use/bu recordings disable
~/.agents/skills/browser-use/bu recordings
```

## Gotchas

- `chrome://inspect/#remote-debugging` must be enabled for local Chrome control.
- Omnibox popups are not real work tabs.
- CDP target order is not Chrome's visible tab-strip order.
