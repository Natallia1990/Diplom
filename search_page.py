from selenium.webdriver.common.keys import Keys
from base_page import BasePage
from config import UISettings, Settings
import allure
from typing import Any


class SearchPage(BasePage):
    def __init__(self, driver: Any) -> None:
        super().__init__(driver)

    @allure.step("Открытие главной страницы")
    def open(self) -> None:
        """Открывает главную страницу Кинопоиска"""
        self.driver.get(Settings.UI_BASE_URL)
        self.wait_for_page_load()

    @allure.step("Проверка отображения поля поиска")
    def is_search_input_displayed(self) -> bool:
        """
        Проверяет отображение поля ввода поиска

        Returns:
            bool: True если поле отображается
        """
        return self.is_element_present(UISettings.SEARCH_INPUT)

    @allure.step("Выполнение поиска по запросу: '{query}'")
    def perform_search(self, query: str) -> None:
        """
        Выполняет поиск по заданному запросу

        Args:
            query: Поисковый запрос
        """
        self.send_keys(UISettings.SEARCH_INPUT, query)
        search_input = self.find_element(UISettings.SEARCH_INPUT)
        search_input.send_keys(Keys.ENTER)
        self.wait_for_page_load()

    @allure.step("Получение количества результатов поиска")
    def get_search_results_count(self) -> int:
        """
        Получает количество найденных результатов

        Returns:
            int: Количество результатов
        """
        results = self.find_elements(UISettings.SEARCH_RESULTS)
        return len(results)

    @allure.step("Проверка наличия результатов с текстом: '{text}'")
    def has_results_with_text(self, text: str) -> bool:
        """
        Проверяет наличие результатов с указанным текстом

        Args:
            text: Текст для поиска в результатах

        Returns:
            bool: True если есть совпадения
        """
        results = self.find_elements(UISettings.SEARCH_RESULTS)
        search_text = text.lower()

        for result in results:
            if search_text in result.text.lower():
                return True
        return False
