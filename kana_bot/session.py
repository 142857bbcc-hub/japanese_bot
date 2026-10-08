import time
import random

from playwright.sync_api import (
    TimeoutError as PlaywrightTimeoutError,
    Error as PlaywrightError,
)

from kana_bot.config import BOT_LEVEL_DELAYS_MS
from kana_bot.kana_map import KANA_MAP, ALL_ROMAJI_VALUES
from kana_bot.browser import safe_click, click_confirm_if_present


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
        click_confirm_if_present(self.page)

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

        print(
            f"Practice finished: {self.correct_questions}/{self.total_questions} answered correctly."
        )
