from playwright.sync_api import sync_playwright, Error as PlaywrightError

from kana_bot.settings import get_settings, prompt_yes_no
from kana_bot.browser import wait_for_login, open_practice
from kana_bot.session import PracticeSession


def run_practice(page, settings):
    if not open_practice(page):
        return False

    session = PracticeSession(page, settings)
    try:
        session.run()
    except KeyboardInterrupt:
        print("Interrupted by user — stopping cleanly.")
    except PlaywrightError as e:
        print(f"Unexpected Playwright error: {e}")

    return page.context.browser.is_connected()


def main():
    settings = get_settings()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        try:
            if not wait_for_login(page):
                raise SystemExit(1)

            while True:
                if not run_practice(page, settings):
                    break
                if not prompt_yes_no("Start a new practice?"):
                    break
                settings = get_settings()
        except KeyboardInterrupt:
            print("Interrupted by user.")
        finally:
            print("Closing browser...")
            if browser.is_connected():
                browser.close()


if __name__ == "__main__":
    main()
