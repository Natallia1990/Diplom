from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from config import Settings
import allure


class BrowserFactory:
    """Фабрика для создания WebDriver"""

    @staticmethod
    @allure.step("Инициализация WebDriver для {browser}")
    def create_driver(browser: str = None,
                      headless: bool = None) -> webdriver.Remote:
        """
        Создает экземпляр WebDriver

        Args:
            browser: Тип браузера (chrome, firefox, edge)
            headless: Режим без графического интерфейса

        Returns:
            webdriver.Remote: Экземпляр WebDriver
        """
        browser = browser or Settings.BROWSER
        headless = headless if headless is not None else Settings.HEADLESS

        if browser == "chrome":
            return BrowserFactory._create_chrome_driver(headless)
        elif browser == "firefox":
            return BrowserFactory._create_firefox_driver(headless)
        elif browser == "edge":
            return BrowserFactory._create_edge_driver(headless)
        else:
            raise ValueError(f"Неподдерживаемый браузер: {browser}")

    @staticmethod
    def _create_chrome_driver(headless: bool) -> webdriver.Chrome:
        """Создает Chrome WebDriver"""
        options = ChromeOptions()

        if headless:
            options.add_argument("--headless=new")

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument(f"--window-size={Settings.WINDOW_WIDTH},"
                             f"{Settings.WINDOW_HEIGHT}")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches",
                                        ["enable-automation"])
        options.add_experimental_option('useAutomationExtension',
                                        False)

        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        driver.execute_script("Object.defineProperty(navigator,"
                              "'webdriver', {get: () => undefined})")

        return driver

    @staticmethod
    def _create_firefox_driver(headless: bool) -> webdriver.Firefox:
        """Создает Firefox WebDriver"""
        options = FirefoxOptions()

        if headless:
            options.add_argument("--headless")

        options.add_argument("--width=1920")
        options.add_argument("--height=1080")

        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)

        driver.set_window_size(Settings.WINDOW_WIDTH, Settings.WINDOW_HEIGHT)
        return driver

    @staticmethod
    def _create_edge_driver(headless: bool) -> webdriver.Edge:
        """Создает Edge WebDriver"""
        options = EdgeOptions()

        if headless:
            options.add_argument("--headless")

        options.add_argument(f"--window-size={Settings.WINDOW_WIDTH},"
                             f"{Settings.WINDOW_HEIGHT}")

        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)

        return driver
