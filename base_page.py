from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config import Settings
import allure
from typing import Tuple, List, Any


class BasePage:
    def __init__(self, driver: Any) -> None:
        self.driver = driver
        self.wait = WebDriverWait(driver, Settings.EXPLICIT_WAIT)

    @allure.step("Поиск элемента: {locator}")
    def find_element(self,
                     locator: Tuple[str, str], timeout: int = None) -> Any:
        """
        Находит элемент с ожиданием

        Args:
            locator: Кортеж (method, локатор)
            timeout: Время ожидания в секундах

        Returns:
            WebElement: Найденный элемент
        """
        wait = WebDriverWait(self.driver, timeout or Settings.EXPLICIT_WAIT)
        by_method, locator_value = locator
        return wait.until(
            EC.presence_of_element_located(
                (getattr(By, by_method.upper()), locator_value))
        )

    @allure.step("Поиск всех элементов: {locator}")
    def find_elements(
            self, locator: Tuple[str, str],
            timeout: int = None) -> List[Any]:
        """
        Находит все элементы с ожиданием

        Args:
            locator: Кортеж (method, локатор)
            timeout: Время ожидания в секундах

        Returns:
            List[WebElement]: Список найденных элементов
        """
        wait = WebDriverWait(self.driver, timeout or Settings.EXPLICIT_WAIT)
        by_method, locator_value = locator
        return wait.until(
            EC.presence_of_all_elements_located(
                (getattr(By, by_method.upper()), locator_value))
        )

    @allure.step("Клик по элементу: {locator}")
    def click(self, locator: Tuple[str, str], timeout: int = None) -> None:
        """
        Кликает по элементу

        Args:
            locator: Кортеж (method, локатор)
            timeout: Время ожидания в секундах
        """
        element = self.find_element(locator, timeout)
        element.click()

    @allure.step("Ввод текста: '{text}' в элемент {locator}")
    def send_keys(self, locator: Tuple[str, str], text: str) -> None:
        """
        Вводит текст в поле

        Args:
            locator: Кортеж (method, локатор)
            text: Текст для ввода
        """
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    @allure.step("Проверка наличия элемента: {locator}")
    def is_element_present(
            self, locator: Tuple[str, str],
            timeout: int = None) -> bool:
        """
        Проверяет наличие элемента на странице

        Args:
            locator: Кортеж (method, локатор)
            timeout: Время ожидания в секундах

        Returns:
            bool: True если элемент присутствует
        """
        try:
            self.find_element(locator, timeout)
            return True
        except TimeoutException:
            return False

    @allure.step("Ожидание загрузки страницы")
    def wait_for_page_load(self) -> None:
        """Ожидает полной загрузки страницы"""
        self.wait.until(
            lambda driver: driver.execute_script(
                "return document.readyState") == "complete"
        )
