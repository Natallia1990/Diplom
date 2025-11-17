import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    API_BASE_URL = os.getenv("API_BASE_URL", "https://api.kinopoisk.dev/v1.4")
    API_TOKEN = os.getenv("KINOPOISK_API_TOKEN", "your-api-token-here")
    UI_BASE_URL = os.getenv("UI_BASE_URL", "https://www.kinopoisk.ru")
    HEADLESS = os.getenv("HEADLESS", "true") == "true"
    EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "10"))


class APISettings:
    MOVIE_SEARCH = "/movie/search"


class UISettings:
    SEARCH_INPUT = ("xpath", "//input[@name='kp_query']")
    SEARCH_BUTTON = ("xpath", "//button[@type='submit']")
    SEARCH_RESULTS = ("xpath", "//a[contains(@href, '/film/')]")
