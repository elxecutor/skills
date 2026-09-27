---
name: browser-use
description: "Direct browser control via CDP for web interaction: automation, scraping, testing, screenshots, and site/app work."
---

# Browser Use

Direct browser control via CDP. Use `bu` (wrapper at `~/.local/bin/bu`) — it auto-reads Brave's DevToolsActivePort so `BU_CDP_WS` is set per-session.

## When Not to Use

A basic fetch of public information needs no browser. If a plain HTTP request can read it — a public page, an API, docs — use `curl` or your fetch tool, and leave the browser alone. Use browser-use when the task needs interaction (click, type, navigate), the user's logged-in session, JS rendering, or a bot-protected page. If a direct fetch fails or returns a shell page, then escalate to the browser.

## Usage

```bash
bu <<'PY'
print(page_info())
PY
```

- Invoke as `bu`. Use heredocs for multi-line commands.
- Helpers are pre-imported.
- First navigation is `new_tab(url)`, not `goto_url(url)`.

## Local Chrome

If the daemon cannot connect, run diagnostics:

```bash
bu --doctor
```

If Chrome is not running at all, the harness launches it automatically and retries — no user action needed beyond clicking Allow if a permission popup appears.

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
- If the current tab is stale or internal, call `ensure_real_tab()`.
- Use `js(...)` for DOM inspection or extraction when coordinates are the wrong tool.
- Use `watch_network()` to see network requests in a dev-tool-like table.
- Login walls: stop and ask. Exception: use available SSO automatically when Chrome is already signed in; still stop for passwords, MFA, consent, or ambiguous account choice.
- Raw CDP is available with `cdp("Domain.method", ...)`.

## Recordings

```bash
bu recordings enable
bu recordings disable
bu recordings
```

## Gotchas

- `chrome://inspect/#remote-debugging` must be enabled for local Chrome control.
- Omnibox popups are not real work tabs.
- CDP target order is not Chrome's visible tab-strip order.
