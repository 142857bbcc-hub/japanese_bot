LOGIN_URL = "https://my-kana-learning-app.web.app/index.html#login-screen"
MAIN_URL = "https://my-kana-learning-app.web.app/index.html#main-menu-screen"

LOGIN_TIMEOUT_SECONDS = 120
PRACTICE_START_TIMEOUT_MS = 10 * 60 * 1000
APP_PRACTICE_LIMIT_SECONDS = 10 * 60

BOT_LEVEL_DELAYS_MS = {
    1: (3000, 5000),
    2: (2000, 4000),
    3: (1000, 3000),
    4: (500, 1500),
    5: (300, 400),
}
