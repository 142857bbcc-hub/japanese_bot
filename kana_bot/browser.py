import time

from playwright.sync_api import (
    TimeoutError as PlaywrightTimeoutError,
    Error as PlaywrightError,
)

from kana_bot.config import (
    LOGIN_URL,
    MAIN_URL,
    LOGIN_TIMEOUT_SECONDS,
    PRACTICE_START_TIMEOUT_MS,
)


def safe_click(locator, description, timeout=5000):
    try:
        locator.click(timeout=timeout)
        return True
    except PlaywrightTimeoutError:
        print(f"Could not find/click '{description}' in time — skipping.")
    except PlaywrightError as e:
        print(f"Error clicking '{description}': {e}")
    return False


def wait_for_selector_visible(page, selector, timeout_ms, description):
    try:
        page.wait_for_selector(selector, state="visible", timeout=timeout_ms)
        return True
    except PlaywrightTimeoutError:
        print(f"Timed out waiting for '{description}'.")
    except PlaywrightError as e:
        print(f"Error waiting for '{description}': {e}")
    return False


def click_confirm_if_present(page):
    try:
        confirm_btn = page.get_by_role("button", name="確認", exact=False)
        if confirm_btn.is_visible(timeout=100):
            confirm_btn.click(timeout=1000)
    except PlaywrightError:
        pass


def wait_for_login(page):
    page.goto(LOGIN_URL)
    start_time = time.time()

    while time.time() - start_time < LOGIN_TIMEOUT_SECONDS:
        try:
            welcome_text = page.locator("#welcome-message").text_content(timeout=1000)
            if welcome_text and welcome_text.strip():
                return True

            if page.locator("#modal").is_visible(timeout=100):
                modal_message = page.locator("#modal-message").text_content(
                    timeout=1000
                )
                if modal_message and "登入失敗" in modal_message:
                    print(f"Google login failed: {modal_message.strip()}")
                    return False

            page.wait_for_timeout(500)
        except PlaywrightError:
            page.wait_for_timeout(500)

    print("Google login timed out.")
    return False


def open_practice(page):
    try:
        page.goto(MAIN_URL)
    except PlaywrightError as e:
        print(f"Error navigating to main menu: {e}")
        return False

    if not safe_click(page.get_by_role("button", name="開始練習"), "開始練習 (start)"):
        print("Could not open the practice setup screen.")
        return False

    print("Choose your practice options in the browser and start the practice.")
    if not wait_for_selector_visible(
        page, "#question-display", PRACTICE_START_TIMEOUT_MS, "practice session start"
    ):
        print("Practice session start wasn't detected.")
        return False

    return True


def exit_practice(page):
    if not safe_click(
        page.get_by_role("button", name="暫停並退出"), "暫停並退出 (pause and exit)"
    ):
        return False
    click_confirm_if_present(page)
    return True
