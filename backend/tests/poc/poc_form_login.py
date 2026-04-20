"""POC: Verify programmatic form login works for ERP SPA login.

方案 A — 编程式表单登录 with improved event dispatch.
Tests whether Vue-compatible form filling + login button click causes SPA redirect.

Prerequisites: ERP_BASE_URL, ERP_USERNAME, ERP_PASSWORD in .env
Usage: .venv/bin/python backend/tests/poc/poc_form_login.py
"""

import asyncio
import json
import os
from urllib.parse import urlparse

import httpx
from browser_use import BrowserSession
from browser_use.browser.profile import BrowserProfile, ViewportSize
from dotenv import load_dotenv

load_dotenv()


def _extract_origin(url: str) -> str:
    """Extract origin (scheme + netloc) from URL, stripping path."""
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


def _parse_eval_result(raw):
    """Parse page.evaluate result — handles string (JSON) or dict."""
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return raw
    return raw


async def fetch_token(base_url: str, account: str, password: str) -> str:
    """HTTP POST to ERP login API, extract access_token (reference only)."""
    login_url = f"{base_url.rstrip('/')}/auth/login"
    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(
            login_url,
            json={"username": account, "password": password},
            headers={"Content-Type": "application/json"},
        )
        if response.status_code != 200:
            raise RuntimeError(
                f"Token fetch failed: HTTP {response.status_code}: "
                f"{response.text[:200]}"
            )
        data = response.json()
        return data["data"]["access_token"]


async def poc_form_login() -> bool:
    """方案 A: 编程式表单登录验证 (improved event dispatch).

    Sequence:
    1. Load env vars + fetch token (for reference/diagnostic)
    2. Start browser-use BrowserSession
    3. Navigate to ERP /login page
    4. Click "密码登录" tab if present
    5. Fill form with Vue-compatible event dispatch (IMPROVED)
    6. Click login button
    7. Wait for redirect with progressive waits
    8. Extra diagnostics on failure
    """
    erp_base_url = os.getenv("ERP_BASE_URL", "").rstrip("/")
    account = os.getenv("ERP_USERNAME", "")
    password = os.getenv("ERP_PASSWORD", "")

    if not all([erp_base_url, account, password]):
        print("[ERROR] Missing env vars: ERP_BASE_URL, ERP_USERNAME, ERP_PASSWORD")
        return False

    erp_origin = _extract_origin(erp_base_url)

    print("=" * 60)
    print("POC 方案 A: 编程式表单登录 (improved event dispatch)")
    print("=" * 60)
    print(f"ERP_BASE_URL: {erp_base_url}")
    print(f"ERP_ORIGIN:   {erp_origin}")
    print(f"Account:      {account}")
    print()

    # [1] Fetch token (reference only — proves HTTP login works)
    try:
        token = await fetch_token(erp_base_url, account, password)
        print(f"[1] HTTP token fetch OK: {token[:30]}...")
    except Exception as e:
        print(f"[1] HTTP token fetch FAILED: {e}")
        print("[1] Cannot proceed — ERP API unreachable or credentials wrong")
        return False

    # [2] Start browser-use BrowserSession
    browser_args = [
        "--no-sandbox",
        "--disable-gpu",
        "--disable-dev-shm-usage",
        "--disable-software-rasterizer",
        "--disable-extensions",
    ]
    profile = BrowserProfile(
        headless=True,
        args=browser_args,
        viewport=ViewportSize(width=1920, height=1080),
    )
    session = BrowserSession(browser_profile=profile)

    try:
        await session.start()
        print("[2] Browser session started (headless=True)")

        # [3] Navigate to ERP login page
        login_url = f"{erp_origin}/login"
        print(f"\n[3] Navigating to login page: {login_url}")
        await session.navigate_to(login_url)
        await asyncio.sleep(2)

        page = await session.get_current_page()
        if not page:
            print("[3] FAILED: No page available after navigation")
            return False

        current_url = await page.evaluate("() => window.location.href")
        print(f"[3] Current URL: {current_url}")

        # Diagnostic: count visible inputs and buttons
        # All complex objects returned via JSON.stringify for browser-use compat
        page_info = _parse_eval_result(
            await page.evaluate("""() => {
                const inputs = document.querySelectorAll('input');
                const buttons = document.querySelectorAll('button');
                const visibleInputs = [...inputs].filter(i => i.offsetParent !== null);
                return JSON.stringify({
                    totalInputs: inputs.length,
                    visibleInputs: visibleInputs.length,
                    inputDetails: [...inputs].map(i => ({
                        type: i.type || 'text',
                        placeholder: i.placeholder || '',
                        visible: i.offsetParent !== null,
                        name: i.name || '',
                        id: i.id || '',
                    })),
                    totalButtons: buttons.length,
                    buttonTexts: [...buttons].map(b => b.textContent.trim()),
                });
            }""")
        )
        print(f"[3] Page inputs: {page_info['totalInputs']} total, "
              f"{page_info['visibleInputs']} visible")
        for inp in page_info["inputDetails"]:
            print(f"     - type={inp['type']}, placeholder='{inp['placeholder']}', "
                  f"visible={inp['visible']}, name='{inp['name']}', id='{inp['id']}'")
        print(f"[3] Buttons: {page_info['buttonTexts']}")

        # [4] Click "密码登录" tab if present
        clicked_tab = await page.evaluate("""() => {
            const tabs = document.querySelectorAll('div, span, a, li');
            for (const el of tabs) {
                if (el.textContent.trim() === '密码登录') {
                    el.click();
                    return true;
                }
            }
            return false;
        }""")
        if clicked_tab:
            print("[4] Clicked '密码登录' tab")
            await asyncio.sleep(0.5)
        else:
            print("[4] No '密码登录' tab found, proceeding directly")

        # [5] Fill form with IMPROVED Vue-compatible event dispatch
        print("\n[5] Filling form with improved event dispatch...")

        # Fill account input with composition events
        fill_result = _parse_eval_result(
            await page.evaluate("""(account) => {
                const inputs = document.querySelectorAll('input');
                const textInputs = [];
                for (const inp of inputs) {
                    const type = (inp.type || 'text').toLowerCase();
                    if (type === 'password') continue;
                    if (type === 'text' || type === 'tel' || type === 'number') {
                        if (inp.offsetParent !== null) {
                            textInputs.push(inp);
                        }
                    }
                }
                if (textInputs.length === 0) return JSON.stringify({ status: 'no_text_input' });

                const nativeSetter = Object.getOwnPropertyDescriptor(
                    window.HTMLInputElement.prototype, 'value'
                ).set;

                textInputs[0].focus();
                nativeSetter.call(textInputs[0], account);

                textInputs[0].dispatchEvent(new Event('compositionstart', { bubbles: true }));
                textInputs[0].dispatchEvent(new Event('compositionend', { bubbles: true }));
                textInputs[0].dispatchEvent(new Event('input', { bubbles: true }));
                textInputs[0].dispatchEvent(new Event('change', { bubbles: true }));

                return JSON.stringify({
                    status: 'filled',
                    actualValue: textInputs[0].value,
                    inputType: textInputs[0].type || 'text',
                });
            }""", account)
        )
        print(f"[5.1] Account fill: {fill_result}")
        if fill_result.get("status") != "filled":
            print("[5.1] FAILED: Could not find or fill account input")
            return False

        await asyncio.sleep(0.3)

        # Fill password input with same improved pattern
        pwd_result = _parse_eval_result(
            await page.evaluate("""(password) => {
                const inputs = document.querySelectorAll(
                    'input[type="password"], input[placeholder*="密码"]'
                );
                for (const inp of inputs) {
                    if (inp.offsetParent !== null) {
                        const nativeSetter = Object.getOwnPropertyDescriptor(
                            window.HTMLInputElement.prototype, 'value'
                        ).set;

                        inp.focus();
                        nativeSetter.call(inp, password);
                        inp.dispatchEvent(new Event('compositionstart', { bubbles: true }));
                        inp.dispatchEvent(new Event('compositionend', { bubbles: true }));
                        inp.dispatchEvent(new Event('input', { bubbles: true }));
                        inp.dispatchEvent(new Event('change', { bubbles: true }));

                        return JSON.stringify({
                            status: 'filled',
                            actualLength: inp.value.length,
                        });
                    }
                }
                return JSON.stringify({ status: 'no_password_input' });
            }""", password)
        )
        print(f"[5.2] Password fill: {pwd_result}")
        if pwd_result.get("status") != "filled":
            print("[5.2] FAILED: Could not find or fill password input")
            return False

        await asyncio.sleep(0.3)

        # Verify form values after fill
        verify_result = _parse_eval_result(
            await page.evaluate("""() => {
                const inputs = document.querySelectorAll('input');
                const visible = [...inputs].filter(i => i.offsetParent !== null);
                return JSON.stringify(visible.map(i => ({
                    type: i.type || 'text',
                    value: i.value,
                    valueLen: i.value.length,
                })));
            }""")
        )
        print(f"[5.3] Form values after fill: {verify_result}")

        # [6] Click login button
        print("\n[6] Clicking login button...")
        click_result = _parse_eval_result(
            await page.evaluate("""() => {
                const buttons = document.querySelectorAll(
                    'button, div.login-btn, [class*="login-btn"], [class*="loginBtn"]'
                );
                for (const btn of buttons) {
                    const text = btn.textContent.trim();
                    if (text === '登 录' || text === '登录' || text === 'Login') {
                        btn.click();
                        return JSON.stringify({ status: 'clicked', text: text, method: 'click' });
                    }
                }
                for (const btn of buttons) {
                    if (btn.offsetParent !== null) {
                        btn.click();
                        return JSON.stringify({
                            status: 'clicked_fallback',
                            text: btn.textContent.trim(),
                            method: 'click',
                        });
                    }
                }
                return JSON.stringify({ status: 'not_found' });
            }""")
        )
        print(f"[6] Button click result: {click_result}")

        if click_result.get("status") == "not_found":
            print("[6] FAILED: No login button found")
            submit_result = await page.evaluate("""() => {
                const form = document.querySelector('form');
                if (form) {
                    form.dispatchEvent(new Event('submit', {
                        bubbles: true, cancelable: true
                    }));
                    return 'form_submitted';
                }
                return 'no_form';
            }""")
            print(f"[6] Form submit fallback: {submit_result}")

        # [7] Wait for redirect with progressive waits
        print("\n[7] Waiting for redirect...")
        login_ok = False
        cumulative_wait = 0
        for wait_sec in [2, 3, 5]:
            await asyncio.sleep(wait_sec)
            cumulative_wait += wait_sec
            current_url = await page.evaluate("() => window.location.href")
            if "/login" not in current_url:
                print(f"[7] SUCCESS after {cumulative_wait}s: redirected to {current_url}")
                login_ok = True
                break
            print(f"[7] Still on login page after {cumulative_wait}s: {current_url}")

        # [8] Extra diagnostics on failure
        if not login_ok:
            print("\n--- FAILURE DIAGNOSTICS ---")

            # Check for error messages on the page
            error_info = _parse_eval_result(
                await page.evaluate("""() => {
                    const errorEls = document.querySelectorAll(
                        '[class*="error"], [class*="warn"], [class*="alert"], '
                        + '[class*="message"], [class*="toast"]'
                    );
                    const messages = [];
                    for (const el of errorEls) {
                        const text = el.textContent.trim();
                        if (text && text.length < 200) {
                            messages.push(text);
                        }
                    }
                    return JSON.stringify(messages);
                }""")
            )
            print(f"Error messages on page: {error_info}")

            # Check if inputs still have values (Vue may have reset them)
            post_fill_check = _parse_eval_result(
                await page.evaluate("""() => {
                    const inputs = document.querySelectorAll('input');
                    const visible = [...inputs].filter(i => i.offsetParent !== null);
                    return JSON.stringify(visible.map(i => ({
                        type: i.type || 'text',
                        value: i.value,
                        valueLen: i.value.length,
                    })));
                }""")
            )
            print(f"Form values after click: {post_fill_check}")

            # Try alternative: MouseEvent click with full options
            print("\n--- Trying alternative click methods ---")

            alt_click = _parse_eval_result(
                await page.evaluate("""() => {
                    const buttons = document.querySelectorAll('button');
                    for (const btn of buttons) {
                        const text = btn.textContent.trim();
                        if (text === '登 录' || text === '登录') {
                            btn.dispatchEvent(new MouseEvent('click', {
                                bubbles: true,
                                cancelable: true,
                                view: window
                            }));
                            return JSON.stringify({ status: 'mouse_clicked', text: text });
                        }
                    }
                    return JSON.stringify({ status: 'not_found' });
                }""")
            )
            print(f"Alt click (MouseEvent): {alt_click}")

            await asyncio.sleep(3)

            current_url = await page.evaluate("() => window.location.href")
            print(f"URL after alt click: {current_url}")

            if "/login" not in current_url:
                print("Alt click SUCCEEDED!")
                login_ok = True

        # Final verification
        if not login_ok:
            # Last resort: try form submit
            print("\n--- Last resort: form submit ---")
            form_submit = await page.evaluate("""() => {
                const form = document.querySelector('form');
                if (form) {
                    form.dispatchEvent(new Event('submit', {
                        bubbles: true, cancelable: true
                    }));
                    return 'form_submitted';
                }
                const submitBtn = document.querySelector(
                    'button[type="submit"], input[type="submit"]'
                );
                if (submitBtn) {
                    submitBtn.click();
                    return 'submit_btn_clicked: ' + submitBtn.textContent.trim();
                }
                return 'no_form_or_submit';
            }""")
            print(f"Form submit: {form_submit}")

            await asyncio.sleep(3)
            current_url = await page.evaluate("() => window.location.href")
            if "/login" not in current_url:
                print(f"Form submit succeeded: {current_url}")
                login_ok = True

        # Print final results
        final_url = await page.evaluate("() => window.location.href")
        token_check = await page.evaluate(
            "() => window.localStorage.getItem('Admin-Token')"
        )

        print()
        print("=" * 60)
        print("RESULTS")
        print("=" * 60)
        print(f"Final URL:                {final_url}")
        print(
            f"localStorage Admin-Token: "
            f"{'present (' + token_check[:20] + '...)' if token_check else 'MISSING'}"
        )
        print(f"Login status:             {'SUCCESS' if login_ok else 'FAILED'}")
        print("=" * 60)

        return login_ok

    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        import traceback

        traceback.print_exc()
        return False

    finally:
        try:
            await session.stop()
            print("\n[CLEANUP] Browser session stopped")
        except Exception as e:
            print(f"\n[CLEANUP] Error stopping session: {e}")


if __name__ == "__main__":
    result = asyncio.run(poc_form_login())
    exit(0 if result else 1)
