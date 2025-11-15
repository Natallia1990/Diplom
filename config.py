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
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "2"))
    EXPLICIT_WAIT = int(os.getenv("EXPLICIT_WAIT", "10"))
    PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "10"))

    # Пути
    SCREENSHOTS_DIR = os.getenv("SCREENSHOTS_DIR", "screenshots")
    ALLURE_RESULTS_DIR = os.getenv("ALLURE_RESULTS_DIR", "allure-results")


class APISettings:
    """Настройки API endpoints"""
    MOVIE_SEARCH = "/movie/search"
    MOVIE = "/movie"


class UISettings:
    """Настройки UI локаторов для актуальной версии Кинопоиска"""

    # Основные селекторы поиска
    SEARCH_INPUT = ("xpath",
                    "//input[@placeholder='Фильмы, сериалы, персоны']")
    SEARCH_BUTTON = ("xpath",
                     "//button[.//*[contains(@class, 'search')]"
                     "or contains(text(), 'Найти')]")
    SEARCH_BUTTON_ALT = ("xpath", "//button[@type='submit']")

    # Результаты поиска - более гибкие селекторы
    SEARCH_RESULTS = ("xpath",
                      "//div[contains(@class,"
                      "'styles_root')]//a[contains(@href, '/film/')]")
    SEARCH_RESULTS_ALT = ("xpath",
                          "//a[contains(@href, '/film/') and .//h1]")
    MOVIE_TITLE = ("xpath",
                   ".//h1 | .//h2 | .//h3 | .//span[contains("
                   "@class, 'title')]")

    # Альтернативные локаторы для разных версий сайта
    SEARCH_INPUT_ALT1 = ("xpath", "//input[contains(@class, 'search')]")
    SEARCH_INPUT_ALT2 = ("xpath", "//input[@name='kp_query']")

    # Расширенный поиск
    ADVANCED_SEARCH_BUTTON = ("xpath", "//a[contains(@href, 'advanced')]")
    ADVANCED_SEARCH_LINK = ("xpath", "//a[contains(text(), 'расширенный')]")

    # Общие элементы
    LOADING_SPINNER = ("xpath", "//div[contains(@class, 'loading')]")
    COOKIE_BANNER = ("xpath",
                     "//div[contains(@class, 'cookie')]"
                     "//button[contains(text(), 'Принять')]")
