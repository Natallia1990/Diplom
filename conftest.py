import os
import sys
import pytest
import allure

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Import project modules
try:
    from kinopoisk_client import KinopoiskAPIClient
    from search_page import SearchPage
    from browser_factory import BrowserFactory
    from config import Settings
except ImportError as e:
    print(f"Import error: {e}")

    class Settings:
        UI_BASE_URL = "https://www.kinopoisk.ru"
        BROWSER = "chrome"
        HEADLESS = False
        IMPLICIT_WAIT = 10
        EXPLICIT_WAIT = 30
        PAGE_LOAD_TIMEOUT = 30
        SCREENSHOTS_DIR = "screenshots"
        ALLURE_RESULTS_DIR = "allure-results"


@pytest.fixture(scope="session")
def api_client():
    """API client fixture"""
    try:
        return KinopoiskAPIClient()
    except NameError:
        return None


@pytest.fixture(scope="function")
def driver():
    """WebDriver fixture"""
    driver = None
    try:
        driver = BrowserFactory.create_driver()
        driver.implicitly_wait(Settings.IMPLICIT_WAIT)
        yield driver
    except Exception as e:
        print(f"Driver error: {e}")
        raise
    finally:
        if driver:
            driver.quit()


@pytest.fixture(scope="function")
def search_page(driver):
    """Search page fixture"""
    try:
        page = SearchPage(driver)
        page.open()
        return page
    except Exception as e:
        print(f"Search page error: {e}")
        return None


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Screenshot on test failure"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        if "driver" in item.funcargs:
            driver = item.funcargs["driver"]
            try:
                os.makedirs(Settings.SCREENSHOTS_DIR, exist_ok=True)
                screenshot_name = f"{item.name}.png"
                driver.save_screenshot(
                    f"{Settings.SCREENSHOTS_DIR}/{screenshot_name}")
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name=screenshot_name,
                    attachment_type=allure.attachment_type.PNG
                )
            except Exception as e:
                print(f"Screenshot failed: {e}")


def pytest_configure(config):
    """Pytest configuration"""
    os.makedirs(Settings.SCREENSHOTS_DIR, exist_ok=True)
    os.makedirs(Settings.ALLURE_RESULTS_DIR, exist_ok=True)
