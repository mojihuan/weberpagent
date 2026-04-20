"""POC: Verify page.evaluate localStorage injection works for ERP SPA login.

方案 C — page.evaluate() 在浏览器上下文中直接写 localStorage + 导航到 SPA 首页。

Prerequisites: ERP_BASE_URL, ERP_USERNAME, ERP_PASSWORD in .env
Usage: .venv/bin/python backend/tests/poc/poc_localstorage_inject.py
"""

import asyncio
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


async def fetch_token(base_url: str, account: str, password: str) -> str:
    """HTTP POST to ERP login API, extract access_token."""
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


async def poc_localstorage_inject() -> bool:
    """方案 C: page.evaluate localStorage 注入验证。

    Sequence:
    1. Load env vars
    2. Fetch token via HTTP POST
    3. Start browser-use BrowserSession
    4. Navigate to same-origin lightweight page (favicon.ico / robots.txt / login)
    5. Write localStorage via page.evaluate (arrow function format)
    6. Navigate to SPA /index
    7. Verify login state (no /login redirect)
    """
    erp_base_url = os.getenv("ERP_BASE_URL", "").rstrip("/")
    account = os.getenv("ERP_USERNAME", "")
    password = os.getenv("ERP_PASSWORD", "")

    if not all([erp_base_url, account, password]):
        print("[ERROR] Missing env vars: ERP_BASE_URL, ERP_USERNAME, ERP_PASSWORD")
        return False

    erp_origin = _extract_origin(erp_base_url)

    print("=" * 60)
    print("POC 方案 C: page.evaluate localStorage 注入")
    print("=" * 60)
    print(f"ERP_BASE_URL: {erp_base_url}")
    print(f"ERP_ORIGIN:   {erp_origin}")
    print(f"Account:      {account}")
    print()

    # [1] Fetch token via HTTP
    try:
        token = await fetch_token(erp_base_url, account, password)
        print(f"[1] Token fetched: {token[:30]}...")
    except Exception as e:
        print(f"[1] FAILED: {e}")
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

        # [3] Navigate to same-origin lightweight page
        # Try favicon.ico first, then robots.txt, then /login as last resort
        lightweight_candidates = [
            f"{erp_origin}/favicon.ico",
            f"{erp_origin}/robots.txt",
            f"{erp_origin}/login",
        ]

        nav_success = False
        for i, url in enumerate(lightweight_candidates):
            candidate_name = url.split("/")[-1] or "login"
            print(f"\n[3.{i + 1}] Trying same-origin page: {url}")
            try:
                await session.navigate_to(url)
                await asyncio.sleep(1)

                page = await session.get_current_page()
                if not page:
                    print(f"[3.{i + 1}] No page available after navigation")
                    continue

                current_url = await page.evaluate("() => window.location.href")
                print(f"[3.{i + 1}] Current URL: {current_url}")

                # Check if we are on the ERP origin (same-origin)
                if current_url.startswith(erp_origin):
                    print(
                        f"[3.{i + 1}] Same-origin context established "
                        f"via {candidate_name}"
                    )
                    nav_success = True
                    break
                else:
                    print(
                        f"[3.{i + 1}] URL not on ERP origin, "
                        f"trying next candidate..."
                    )
            except Exception as e:
                print(f"[3.{i + 1}] Navigation error: {e}")
                continue

        if not nav_success:
            print("[3] FAILED: Could not establish same-origin context")
            return False

        # [4] Write localStorage via page.evaluate (arrow function format)
        page = await session.get_current_page()
        try:
            result = await page.evaluate(
                "(token) => {"
                "  window.localStorage.setItem('Admin-Token', token);"
                "  window.localStorage.setItem('Admin-Expires-In', '720');"
                "  return window.localStorage.getItem('Admin-Token');"
                "}",
                token,
            )
            if result and len(result) > 10:
                print(f"[4] localStorage set successfully: {result[:30]}...")
            else:
                print(f"[4] FAILED: localStorage set returned: {result}")
                return False
        except Exception as e:
            print(f"[4] FAILED: page.evaluate error: {e}")
            return False

        # Verify Admin-Expires-In was also set
        expires_check = await page.evaluate(
            "() => window.localStorage.getItem('Admin-Expires-In')"
        )
        print(f"[4] Admin-Expires-In: {expires_check}")

        # [5] Navigate to SPA /index
        print(f"\n[5] Navigating to SPA index: {erp_origin}/index")
        await session.navigate_to(f"{erp_origin}/index")
        await asyncio.sleep(3)

        # [6] Verify login state
        page = await session.get_current_page()
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
        login_ok = "/login" not in final_url
        print(f"Login status:             {'SUCCESS' if login_ok else 'FAILED'}")
        print("=" * 60)

        if not login_ok:
            # Extra diagnostics for failure
            print()
            print("--- FAILURE DIAGNOSTICS ---")
            print(f"URL contains /login: {('/login' in final_url)}")
            print(f"Token in localStorage: {(token_check is not None)}")

            # Check if there's a redirect parameter
            if "redirect=" in final_url:
                print(
                    "SPA redirected with redirect param — "
                    "router guard triggered before store saw token"
                )

            # Check page title for more info
            try:
                title = await page.evaluate("() => document.title")
                print(f"Page title: {title}")
            except Exception:
                pass

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
    result = asyncio.run(poc_localstorage_inject())
    exit(0 if result else 1)
