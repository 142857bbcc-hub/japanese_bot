from dataclasses import dataclass


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


def prompt_yes_no(prompt, default=True):
    suffix = " [Y/n]: " if default else " [y/N]: "
    while True:
        raw = input(prompt + suffix).strip().lower()
        if raw == "":
            return default
        if raw in ("y", "yes"):
            return True
        if raw in ("n", "no"):
            return False
        print("Please answer y or n.")
