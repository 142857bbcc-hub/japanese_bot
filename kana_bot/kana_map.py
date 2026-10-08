import time
import random
from dataclasses import dataclass
from playwright.sync_api import (
    sync_playwright,
    TimeoutError as PlaywrightTimeoutError,
    Error as PlaywrightError,
)

LOGIN_URL = "https://my-kana-learning-app.web.app/index.html#login-screen"
MAIN_URL = "https://my-kana-learning-app.web.app/index.html#main-menu-screen"

KANA_MAP = {
    "あ": "a",
    "い": "i",
    "う": "u",
    "え": "e",
    "お": "o",
    "か": "ka",
    "き": "ki",
    "く": "ku",
    "け": "ke",
    "こ": "ko",
    "さ": "sa",
    "し": "shi",
    "す": "su",
    "せ": "se",
    "そ": "so",
    "た": "ta",
    "ち": "chi",
    "つ": "tsu",
    "て": "te",
    "と": "to",
    "な": "na",
    "に": "ni",
    "ぬ": "nu",
    "ね": "ne",
    "の": "no",
    "は": "ha",
    "ひ": "hi",
    "ふ": "fu",
    "へ": "he",
    "ほ": "ho",
    "ま": "ma",
    "み": "mi",
    "む": "mu",
    "め": "me",
    "も": "mo",
    "や": "ya",
    "ゆ": "yu",
    "よ": "yo",
    "ら": "ra",
    "り": "ri",
    "る": "ru",
    "れ": "re",
    "ろ": "ro",
    "わ": "wa",
    "を": "wo",
    "ん": "n",
    "が": "ga",
    "ぎ": "gi",
    "ぐ": "gu",
    "げ": "ge",
    "ご": "go",
    "ざ": "za",
    "じ": "ji",
    "ず": "zu",
    "ぜ": "ze",
    "ぞ": "zo",
    "だ": "da",
    "ぢ": "ji",
    "づ": "zu",
    "で": "de",
    "ど": "do",
    "ば": "ba",
    "び": "bi",
    "ぶ": "bu",
    "べ": "be",
    "ぼ": "bo",
    "ぱ": "pa",
    "ぴ": "pi",
    "ぷ": "pu",
    "ぺ": "pe",
    "ぽ": "po",
    "ア": "a",
    "イ": "i",
    "ウ": "u",
    "エ": "e",
    "オ": "o",
    "カ": "ka",
    "キ": "ki",
    "ク": "ku",
    "ケ": "ke",
    "コ": "ko",
    "サ": "sa",
    "シ": "shi",
    "ス": "su",
    "セ": "se",
    "ソ": "so",
    "タ": "ta",
    "チ": "chi",
    "ツ": "tsu",
    "テ": "te",
    "ト": "to",
    "ナ": "na",
    "ニ": "ni",
    "ヌ": "nu",
    "ネ": "ne",
    "ノ": "no",
    "ハ": "ha",
    "ヒ": "hi",
    "フ": "fu",
    "ヘ": "he",
    "ホ": "ho",
    "マ": "ma",
    "ミ": "mi",
    "ム": "mu",
    "メ": "me",
    "モ": "mo",
    "ヤ": "ya",
    "ユ": "yu",
    "ヨ": "yo",
    "ラ": "ra",
    "リ": "ri",
    "ル": "ru",
    "レ": "re",
    "ロ": "ro",
    "ワ": "wa",
    "ヲ": "wo",
    "ン": "n",
    "ガ": "ga",
    "ギ": "gi",
    "グ": "gu",
    "ゲ": "ge",
    "ゴ": "go",
    "ザ": "za",
    "ジ": "ji",
    "ズ": "zu",
    "ゼ": "ze",
    "ゾ": "zo",
    "ダ": "da",
    "ヂ": "ji",
    "ヅ": "zu",
    "デ": "de",
    "ド": "do",
    "バ": "ba",
    "ビ": "bi",
    "ブ": "bu",
    "ベ": "be",
    "ボ": "bo",
    "パ": "pa",
    "ピ": "pi",
    "プ": "pu",
    "ペ": "pe",
    "ポ": "po",
    "きゃ": "kya",
    "きゅ": "kyu",
    "きょ": "kyo",
    "しゃ": "sha",
    "しゅ": "shu",
    "しょ": "sho",
    "ちゃ": "cha",
    "ちゅ": "chu",
    "ちょ": "cho",
    "にゃ": "nya",
    "にゅ": "nyu",
    "にょ": "nyo",
    "ひゃ": "hya",
    "ひゅ": "hyu",
    "ひょ": "hyo",
    "みゃ": "mya",
    "みゅ": "myu",
    "みょ": "myo",
    "りゃ": "rya",
    "りゅ": "ryu",
    "りょ": "ryo",
    "ぎゃ": "gya",
    "ぎゅ": "gyu",
    "ぎょ": "gyo",
    "じゃ": "ja",
    "じゅ": "ju",
    "じょ": "jo",
    "びゃ": "bya",
    "びゅ": "byu",
    "びょ": "byo",
    "ぴゃ": "pya",
    "ぴゅ": "pyu",
    "ぴょ": "pya",
    "キャ": "kya",
    "キュ": "kyu",
    "キョ": "kyo",
    "シャ": "sha",
    "シュ": "shu",
    "ショ": "sho",
    "チャ": "cha",
    "チュ": "chu",
    "チョ": "cho",
    "ニャ": "nya",
    "ニュ": "nyu",
    "ニョ": "nyo",
    "ヒャ": "hya",
    "ヒュ": "hyu",
    "ヒョ": "hyo",
    "ミャ": "mya",
    "ミュ": "myu",
    "ミョ": "myo",
    "リャ": "rya",
    "リュ": "ryu",
    "リョ": "ryo",
    "ギャ": "gya",
    "ギュ": "gyu",
    "ギョ": "gyo",
    "ジャ": "ja",
    "ジュ": "ju",
    "ジョ": "jo",
    "ビャ": "bya",
    "ビュ": "byu",
    "ビョ": "byo",
    "ピャ": "pya",
    "ピュ": "pyu",
    "ピョ": "pya",
    "っ": "tsu",
    "ッ": "tsu",
    "ー": "-",
}

ALL_ROMAJI_VALUES = list(set(KANA_MAP.values()))

BOT_LEVEL_DELAYS_MS = {
    1: (3000, 5000),
    2: (2000, 4000),
    3: (1000, 3000),
    4: (500, 1500),
    5: (300, 400),
}


@dataclass
class Settings:
    level: int
    duration_seconds: float
    correct_rate: int


def prompt_int_in_range(prompt, low, high, default):
    raw = input(prompt).strip()
    if raw == "":
        return default
    try:
        value = int(raw)
    except ValueError:
        print(f"'{raw}' isn't a number — using default {default}.")
        return default
    if value < low or value > high:
        print(f"{value} is out of range ({low}-{high}) — using default {default}.")
        return default
    return value


def prompt_duration_minutes(default_minutes=10):
    raw = input(
        f"Please enter the minutes that the practice should run for (1-10) or leave it blank for default {default_minutes}: "
    ).strip()
    if raw == "":
        return default_minutes * 60
    try:
        minutes = float(raw)
        if minutes <= 0:
            raise ValueError
    except ValueError:
        print(f"'{raw}' isn't valid — using default {default_minutes} minutes.")
        return default_minutes * 60
    return minutes * 60


def get_settings():
    level = prompt_int_in_range(
        "Please enter the level you want to practice (1-5) or leave it blank for default level 5: ",
        1,
        5,
        5,
    )
    duration = prompt_duration_minutes(default_minutes=10)
    correct_rate = prompt_int_in_range(
        "Please enter the correct rate (0-100) or leave it blank for default 100: ",
        0,
        100,
        100,
    )
    return Settings(level=level, duration_seconds=duration, correct_rate=correct_rate)


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


def get_wrong_answer(correct_romaji):
    candidates = [v for v in ALL_ROMAJI_VALUES if v != correct_romaji]
    return random.choice(candidates)


class PracticeSession:
    def __init__(self, page, settings):
        self.page = page
        self.settings = settings
        self.total_questions = 0
        self.correct_questions = 0

    def next_answer(self, correct_romaji):
        self.total_questions += 1
        expected_rate = ((self.correct_questions + 1) / self.total_questions) * 100

        if expected_rate <= self.settings.correct_rate:
            self.correct_questions += 1
            return correct_romaji

        return get_wrong_answer(correct_romaji)

    def undo_last_question(self, was_correct):
        self.total_questions -= 1
        if was_correct:
            self.correct_questions -= 1

    def submit(self, answer):
        self.page.locator("#answer-input").fill(answer, timeout=3000)
        safe_click(self.page.locator("#submit-answer-btn"), "submit answer")
        try:
            confirm_btn = self.page.get_by_role("button", name="確認", exact=False)
            if confirm_btn.is_visible(timeout=100):
                confirm_btn.click(timeout=1000)
        except PlaywrightError:
            pass

    def random_delay(self):
        low, high = BOT_LEVEL_DELAYS_MS[self.settings.level]
        self.page.wait_for_timeout(random.randint(low, high))

    def run(self):
        end_time = time.time() + self.settings.duration_seconds

        while time.time() < end_time:
            if not self.page.context.browser.is_connected():
                print("Browser was closed — stopping.")
                break

            try:
                current_kana = (
                    self.page.locator("#question-display")
                    .inner_text(timeout=3000)
                    .strip()
                )
            except PlaywrightTimeoutError:
                print("Question display not found — retrying.")
                self.page.wait_for_timeout(500)
                continue
            except PlaywrightError as e:
                print(f"Lost connection to the page ({e}) — stopping.")
                break

            correct_romaji = KANA_MAP.get(current_kana)
            if correct_romaji is None:
                print(
                    f"Unrecognized character: '{current_kana}' — waiting before re-checking."
                )
                self.page.wait_for_timeout(500)
                continue

            answer = self.next_answer(correct_romaji)
            was_correct = answer == correct_romaji

            try:
                self.submit(answer)
            except PlaywrightTimeoutError:
                print("Answer input/submit button not found — retrying next loop.")
                self.undo_last_question(was_correct)
            except PlaywrightError as e:
                print(f"Error submitting answer: {e} — retrying next loop.")
                self.undo_last_question(was_correct)

            self.random_delay()


def main():
    settings = get_settings()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(LOGIN_URL)

        login_timeout = 120
        start_time = time.time()

        while time.time() - start_time < login_timeout:
            try:
                welcome_message = page.locator("#welcome-message")
                welcome_text = welcome_message.text_content(timeout=1000)

                if welcome_text and welcome_text.strip():
                    break

                modal = page.locator("#modal")
                if modal.is_visible(timeout=100):
                    modal_message = page.locator("#modal-message").text_content(
                        timeout=1000
                    )

                    if modal_message and "登入失敗" in modal_message:
                        print(f"Google login failed: {modal_message.strip()}")
                        browser.close()
                        raise SystemExit(1)

                page.wait_for_timeout(500)

            except PlaywrightError:
                page.wait_for_timeout(500)

        else:
            print("Google login timed out.")
            browser.close()
            raise SystemExit(1)

        try:
            page.goto(MAIN_URL)
        except PlaywrightError as e:
            print(f"Error navigating to main menu: {e}")
            browser.close()
            raise SystemExit(1)

        if not safe_click(
            page.get_by_role("button", name="開始練習"), "開始練習 (start)"
        ):
            print("Could not open the practice setup screen — exiting.")
            browser.close()
            raise SystemExit(1)

        if not wait_for_selector_visible(
            page, "#question-display", 10 * 60 * 1000, "practice session start"
        ):
            print("Practice session start wasn't detected — exiting.")
            browser.close()
            raise SystemExit(1)

        session = PracticeSession(page, settings)

        try:
            session.run()
        except KeyboardInterrupt:
            print("Interrupted by user — stopping cleanly.")
        except PlaywrightError as e:
            print(f"Unexpected Playwright error: {e}")

        print("Practice session finished. Closing browser in 1 minute...")
        page.wait_for_timeout(60000)
        browser.close()


if __name__ == "__main__":
    main()
