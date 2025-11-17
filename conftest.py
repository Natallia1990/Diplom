import pytest
import os
import sys
from kinopoisk_client import KinopoiskAPIClient
from search_page import SearchPage
from browser_factory import BrowserFactory

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


@pytest.fixture(scope="session")
def api_client():
    return KinopoiskAPIClient()


@pytest.fixture(scope="function")
def driver():
    driver = BrowserFactory.create_driver()
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def search_page(driver):
    page = SearchPage(driver)
    page.open()
    return page
