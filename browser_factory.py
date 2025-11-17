from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from config import Settings


class BrowserFactory:
    @staticmethod
    def create_driver():
        options = ChromeOptions()

        if Settings.HEADLESS:
            options.add_argument("--headless=new")

        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")

        driver = webdriver.Chrome(options=options)
        return driver
