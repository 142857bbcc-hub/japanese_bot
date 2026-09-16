import re
import time
import random
from playwright.sync_api import (
    sync_playwright,
    TimeoutError as PlaywrightTimeoutError,
    Error as PlaywrightError,
)

login_url = "https://my-kana-learning-app.web.app/index.html#login-screen"
main_url = "https://my-kana-learning-app.web.app/index.html#main-menu-screen"

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

bot_level = [[3000, 5000], [2000, 4000], [1000, 3000], [500, 1500], [300, 400]]


def get_valid_level(default=5):
    raw = input(
        "Please enter the level you want to practice (1-5) or leave it blank for default level 5: "
    ).strip()
    if raw == "":
        return default
    try:
        level = int(raw)
    except ValueError:
        print(f"'{raw}' isn't a number — using default level {default}.")
        return default
    if level < 1 or level > 5:
        print(f"{level} is out of range (1-5) — using default level {default}.")
        return default
    return level


def get_valid_correct_rate(default=100):
    raw = input(
        f"Please enter the correct rate (0-100) or leave it blank for default {default}: "
    ).strip()
    if raw == "":
        return default
    try:
        rate = int(raw)
        if rate < 0 or rate > 100:
            raise ValueError
    except ValueError:
        print(f"'{raw}' isn't valid — using default correct rate {default}.")
        return default
    return rate


def get_valid_duration(default_minutes=10):
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


def safe_click(locator, description, timeout=5000):
    try:
        locator.click(timeout=timeout)
        return True
    except PlaywrightTimeoutError:
        print(f"Could not find/click '{description}' in time — skipping.")
    except PlaywrightError as e:
        print(f"Error clicking '{description}': {e}")
    return False


def wait_for_url_contains(page, fragment, timeout_ms, description):
    try:
        page.wait_for_url(re.compile(re.escape(fragment)), timeout=timeout_ms)
        return True
    except PlaywrightTimeoutError:
        print(f"Timed out waiting for '{description}'.")
    except PlaywrightError as e:
        print(f"Error waiting for '{description}': {e}")
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


if __name__ == "__main__":
    level = get_valid_level(default=5)
    duration = get_valid_duration(default_minutes=10)
    correct_rate = get_valid_correct_rate(default=100)

    total_questions = 0
    correct_questions = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(login_url)

        input(
            "Complete the Google login in the opened window. Press Enter here once you're signed in and ready to go to the main menu..."
        )

        try:
            page.goto(main_url)
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

        print(
            "Choose your test range in the browser window, then press 開始練習 there. The script will detect it automatically and start answering."
        )
        if not wait_for_selector_visible(
            page, "#question-display", 10 * 60 * 1000, "practice session start"
        ):
            print("Practice session start wasn't detected — exiting.")
            browser.close()
            raise SystemExit(1)

        end_time = time.time() + duration

        try:
            while time.time() < end_time:
                if not browser.is_connected():
                    print("Browser was closed — stopping.")
                    break

                try:
                    current_kana = (
                        page.locator("#question-display")
                        .inner_text(timeout=3000)
                        .strip()
                    )
                    correct_romaji = KANA_MAP.get(current_kana)
                except PlaywrightTimeoutError:
                    print("Question display not found — retrying.")
                    page.wait_for_timeout(500)
                    continue
                except PlaywrightError as e:
                    print(f"Lost connection to the page ({e}) — stopping.")
                    break

                if correct_romaji:
                    total_questions += 1
                    expected_rate = ((correct_questions + 1) / total_questions) * 100

                    if expected_rate <= correct_rate:
                        answer_to_send = correct_romaji
                        correct_questions += 1
                        is_this_turn_correct = True
                    else:
                        answer_to_send = get_wrong_answer(correct_romaji)
                        is_this_turn_correct = False

                    current_actual_rate = (correct_questions / total_questions) * 100

                    try:
                        page.locator("#answer-input").fill(answer_to_send, timeout=3000)
                        safe_click(page.locator("#submit-answer-btn"), "submit answer")

                        try:
                            confirm_btn = page.get_by_role(
                                "button", name="確認", exact=False
                            )
                            if confirm_btn.is_visible(timeout=100):
                                confirm_btn.click(timeout=1000)
                        except PlaywrightError:
                            pass

                    except PlaywrightTimeoutError:
                        print(
                            "Answer input/submit button not found — retrying next loop."
                        )
                        total_questions -= 1
                        if is_this_turn_correct:
                            correct_questions -= 1
                    except PlaywrightError as e:
                        print(f"Error submitting answer: {e} — retrying next loop.")
                        total_questions -= 1
                        if is_this_turn_correct:
                            correct_questions -= 1

                    random_delay = random.randint(*bot_level[level - 1])
                    page.wait_for_timeout(random_delay)
                else:
                    print(
                        f"Unrecognized character: '{current_kana}' — waiting before re-checking."
                    )
                    page.wait_for_timeout(500)

        except KeyboardInterrupt:
            print("Interrupted by user — stopping cleanly.")
        except PlaywrightError as e:
            print(f"Unexpected Playwright error: {e}")

        print("Practice session finished. Closing browser in 1 minute...")
        page.wait_for_timeout(60000)
        browser.close()
