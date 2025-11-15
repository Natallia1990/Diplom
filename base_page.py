from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (TimeoutException,
                                        ElementClickInterceptedException)
from selenium.webdriver.common.keys import Keys
from config import Settings
import allure
from typing import Tuple, List, Any, Optional


class BasePage:
    """Базовый класс для всех страниц с улучшенной обработкой"""

    def __init__(self, driver):
        """
        Инициализация базовой страницы

        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, Settings.EXPLICIT_WAIT)
        self.driver.implicitly_wait(Settings.IMPLICIT_WAIT)
        self.driver.set_page_load_timeout(Settings.PAGE_LOAD_TIMEOUT)

    @allure.step("Поиск элемента {locator}")
    def find_element(
            self, locator: Tuple[str, str],
            timeout: int = None) -> Any:
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

    @allure.step("Поиск видимого элемента {locator}")
    def find_visible_element(
            self, locator: Tuple[str, str],
            timeout: int = None) -> Any:
        """
        Находит видимый элемент

        Args:
            locator: Кортеж (method, локатор)
            timeout: Время ожидания в секундах

        Returns:
            WebElement: Найденный элемент
        """
        wait = WebDriverWait(self.driver, timeout or Settings.EXPLICIT_WAIT)
        by_method, locator_value = locator
        return wait.until(
            EC.visibility_of_element_located(
                (getattr(By, by_method.upper()), locator_value))
        )

    @allure.step("Поиск кликабельного элемента {locator}")
    def find_clickable_element(
            self, locator: Tuple[str, str],
            timeout: int = None) -> Any:
        """
        Находит кликабельный элемент

        Args:
            locator: Кортеж (method, локатор)
            timeout: Время ожидания в секундах

        Returns:
            WebElement: Найденный элемент
        """
        wait = WebDriverWait(self.driver, timeout or Settings.EXPLICIT_WAIT)
        by_method, locator_value = locator
        return wait.until(
            EC.element_to_be_clickable(
                (getattr(By, by_method.upper()), locator_value))
        )

    @allure.step("Поиск элементов {locator}")
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

    @allure.step("Клик по элементу {locator}")
    def click(self, locator: Tuple[str, str], timeout: int = None) -> None:
        """
        Кликает по элементу с обработкой исключений

        Args:
            locator: Кортеж (method, локатор)
            timeout: Время ожидания в секундах
        """
        try:
            element = self.find_clickable_element(locator, timeout)
            element.click()
        except ElementClickInterceptedException:
            element = self.find_element(locator, timeout)
            self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Ввод текста '{text}' в элемент {locator}")
    def send_keys(
            self, locator: Tuple[str, str],
            text: str, clear: bool = True) -> None:
        """
        Вводит текст в поле

        Args:
            locator: Кортеж (method, локатор)
            text: Текст для ввода
            clear: Очищать ли поле перед вводом
        """
        element = self.find_clickable_element(locator)
        if clear:
            element.clear()
        element.send_keys(text)

    @allure.step("Ввод текста с ENTER '{text}' в элемент {locator}")
    def send_keys_with_enter(
            self, locator: Tuple[str, str],
            text: str) -> None:
        """
        Вводит текст и нажимает ENTER

        Args:
            locator: Кортеж (method, локатор)
            text: Текст для ввода
        """
        element = self.find_clickable_element(locator)
        element.clear()
        element.send_keys(text)
        element.send_keys(Keys.ENTER)

    @allure.step("Получение текста элемента {locator}")
    def get_text(self, locator: Tuple[str, str]) -> str:
        """
        Получает текст элемента

        Args:
            locator: Кортеж (method, локатор)

        Returns:
            str: Текст элемента
        """
        element = self.find_element(locator)
        return element.text.strip()

    @allure.step("Проверка наличия элемента {locator}")
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

    @allure.step("Проверка видимости элемента {locator}")
    def is_element_visible(
            self, locator: Tuple[str, str],
            timeout: int = None) -> bool:
        """
        Проверяет видимость элемента

        Args:
            locator: Кортеж (method, локатор)
            timeout: Время ожидания в секундах

        Returns:
            bool: True если элемент видим
        """
        try:
            self.find_visible_element(locator, timeout)
            return True
        except TimeoutException:
            return False

    @allure.step("Ожидание загрузки страницы")
    def wait_for_page_load(self, timeout: int = None) -> None:
        """Ожидает полной загрузки страницы"""
        wait = WebDriverWait(self.driver, timeout or Settings.EXPLICIT_WAIT)
        wait.until(
            lambda driver:
            driver.execute_script("return document.readyState") == "complete"
        )
        self.wait_for_dynamic_content()

    @allure.step("Ожидание динамического контента")
    def wait_for_dynamic_content(self, timeout: int = 5) -> None:
        """
        Ожидает завершения динамической загрузки контента

        Args:
            timeout: Время ожидания в секундах
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script(
                    "return ("
                    "typeof jQuery === 'undefined') || jQuery.active === 0"
                )
            )
        except TimeoutException:
            pass

    @allure.step("Скриншот страницы")
    def take_screenshot(self, name: str) -> None:
        """
        Делает скриншот страницы

        Args:
            name: Имя файла скриншота
        """
        self.driver.save_screenshot(f"{Settings.SCREENSHOTS_DIR}/{name}.png")
        allure.attach(
            self.driver.get_screenshot_as_png(),
            name=name,
            attachment_type=allure.attachment_type.PNG
        )

    @allure.step("Обработка cookie баннера")
    def handle_cookie_banner(self) -> bool:
        """
        Обрабатывает cookie баннер если присутствует

        Returns:
            bool: True если баннер был обработан
        """
        from config import UISettings
        cookie_locator = UISettings.COOKIE_BANNER

        if self.is_element_present(cookie_locator, timeout=5):
            try:
                self.click(cookie_locator)
                self.wait_for_element_to_disappear(cookie_locator, timeout=3)
                return True
            except Exception as e:
                print(f"Не удалось закрыть cookie баннер: {e}")
                return False
        return False

    @allure.step("Ожидание исчезновения элемента")
    def wait_for_element_to_disappear(
            self, locator: Tuple[str, str],
            timeout: int = None) -> None:
        """
        Ожидает пока элемент исчезнет со страницы

        Args:
            locator: Кортеж (method, локатор)
            timeout: Время ожидания в секундах
        """
        wait = WebDriverWait(self.driver, timeout or Settings.EXPLICIT_WAIT)
        by_method, locator_value = locator
        wait.until(
            EC.invisibility_of_element_located(
                (getattr(By, by_method.upper()), locator_value))
        )

    @allure.step("Поиск элемента из списка локаторов")
    def find_element_by_multiple_locators(
            self, locators: List[Tuple[str, str]], timeout: int = None
    ) -> Optional[Any]:
        """
        Пытается найти элемент используя несколько локаторов

        Args:
            locators: Список кортежей (method, локатор)
            timeout: Время ожидания для каждого локатора

        Returns:
            Optional[WebElement]: Найденный элемент или None
        """
        for locator in locators:
            try:
                element = self.find_element(locator, timeout=timeout or 5)
                if element:
                    return element
            except TimeoutException:
                continue
        return None

    @allure.step("Ожидание появления текста в элементе")
    def wait_for_text_in_element(
            self, locator: Tuple[str, str],
            expected_text: str, timeout: int = None) -> bool:
        """
        Ожидает появления определенного текста в элементе

        Args:
            locator: Кортеж (method, локатор)
            expected_text: Ожидаемый текст
            timeout: Время ожидания в секундах

        Returns:
            bool: True если текст появился
        """
        try:
            wait = WebDriverWait(
                self.driver, timeout or Settings.EXPLICIT_WAIT)
            by_method, locator_value = locator
            wait.until(
                EC.text_to_be_present_in_element(
                    (getattr(By,
                             by_method.upper()), locator_value), expected_text
                )
            )
            return True
        except TimeoutException:
            return False

    @allure.step("Ожидание изменения URL")
    def wait_for_url_change(
            self, previous_url: str, timeout: int = None) -> bool:
        """
        Ожидает изменения URL страницы

        Args:
            previous_url: Предыдущий URL для сравнения
            timeout: Время ожидания в секундах

        Returns:
            bool: True если URL изменился
        """
        try:
            wait = WebDriverWait(
                self.driver, timeout or Settings.EXPLICIT_WAIT)
            wait.until(EC.url_changes(previous_url))
            return True
        except TimeoutException:
            return False
