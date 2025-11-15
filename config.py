import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Настройки проекта"""

    # API настройки
    API_BASE_URL = os.getenv("API_BASE_URL", "https://api.kinopoisk.dev/v1.4")
    API_TOKEN = os.getenv("KINOPOISK_API_TOKEN", "your-api-token-here")

    # UI настройки
    UI_BASE_URL = os.getenv("UI_BASE_URL", "https://www.kinopoisk.ru")
    BROWSER = os.getenv("BROWSER", "chrome").lower()
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    WINDOW_WIDTH = int(os.getenv("WINDOW_WIDTH", "1920"))
    WINDOW_HEIGHT = int(os.getenv("WINDOW_HEIGHT", "1080"))

    # Таймауты
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "10"))
    EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "20"))
    PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))

    # Пути
    SCREENSHOTS_DIR = os.getenv("SCREENSHOTS_DIR", "screenshots")
    ALLURE_RESULTS_DIR = os.getenv("ALLURE_RESULTS_DIR", "allure-results")


class APISettings:
    """Настройки API endpoints"""
    MOVIE_SEARCH = "/movie/search"
    MOVIE = "/movie"


class UISettings:
    """Настройки UI локаторов"""

    # Селекторы поиска
    SEARCH_INPUT = ("xpath", "//input[@name='kp_query']")
    SEARCH_BUTTON = ("xpath", "//button[@type='submit' and contains(@class, 'search')]")
    SEARCH_RESULTS = ("xpath", "//div[contains(@class, 'search_results')]//div[contains(@class, 'element')]")
    MOVIE_TITLE = ("xpath", ".//a[contains(@class, 'name')]")
    MOVIE_YEAR = ("xpath", ".//span[contains(@class, 'year')]")

    # Расширенный поиск
    ADVANCED_SEARCH_BUTTON = ("xpath", "//a[contains(text(), 'расширенный поиск') or contains(@href, 'advanced')]")
    COUNTRY_INPUT = ("xpath", "//input[@name='country']")
    DISTRIBUTOR_INPUT = ("xpath", "//input[@name='distributor']")
    APPLY_FILTERS_BUTTON = ("xpath", "//button[contains(text(), 'Найти') or @type='submit']")

    # Общие элементы
    LOADING_SPINNER = ("xpath", "//div[contains(@class, 'loading') or contains(@class, 'spinner')]")
    ERROR_MESSAGE = ("xpath", "//div[contains(@class, 'error')]")