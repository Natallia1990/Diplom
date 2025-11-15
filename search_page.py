from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from base_page import BasePage
from config import UISettings, Settings
import allure
from typing import List
from selenium.common.exceptions import TimeoutException


class SearchPage(BasePage):
    """Page Object для страницы поиска Кинопоиска с улучшенной обработкой"""

    def __init__(self, driver):
        super().__init__(driver)
        self.search_inputs = [
            UISettings.SEARCH_INPUT,
            UISettings.SEARCH_INPUT_ALT1,
            UISettings.SEARCH_INPUT_ALT2
        ]
        self.search_buttons = [
            UISettings.SEARCH_BUTTON,
            UISettings.SEARCH_BUTTON_ALT
        ]
        self.search_results_locators = [
            UISettings.SEARCH_RESULTS,
            UISettings.SEARCH_RESULTS_ALT
        ]

    @allure.step("Открытие главной страницы")
    def open(self) -> None:
        """
        Открывает главную страницу Кинопоиска
        """
        self.driver.get(Settings.UI_BASE_URL)
        self.wait_for_page_load()

        self.handle_cookie_banner()

        self.wait_for_page_fully_loaded()

    @allure.step("Ожидание полной загрузки страницы")
    def wait_for_page_fully_loaded(self, timeout: int = 5) -> None:
        """
        Ожидает полной загрузки страницы и появления основных элементов

        Args:
            timeout: Время ожидания в секундах
        """
        self.wait_for_page_load()

        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: any(
                    self.is_element_present(locator, timeout=1)
                    for locator in self.search_inputs
                )
            )
        except TimeoutException:
            print(
                "Предупреждение: поле поиска не появилось в течение таймаута")

    @allure.step("Проверка отображения поля поиска")
    def is_search_input_displayed(self) -> bool:
        """
        Проверяет отображение поля ввода поиска

        Returns:
            bool: True если поле отображается и доступно
        """
        search_input = (self.
                        find_element_by_multiple_locators(self.
                                                          search_inputs))
        if not search_input:
            return False

        return search_input.is_displayed() and search_input.is_enabled()

    @allure.step("Выполнение поиска по запросу: '{query}'")
    def perform_search(self, query: str, use_enter: bool = True) -> None:
        """
        Выполняет поиск по заданному запросу

        Args:
            query: Поисковый запрос
            use_enter: Использовать ли ENTER для поиска
        """
        search_input = (self.
                        find_element_by_multiple_locators
                        (self.search_inputs))
        if not search_input:
            raise Exception("Не удалось найти поле поиска")

        search_input.clear()
        search_input.send_keys(query)

        self.wait_for_text_input(search_input, query)

        if use_enter:
            search_input.send_keys(Keys.ENTER)
        else:
            search_button = self.find_element_by_multiple_locators(
                self.search_buttons, timeout=5
            )
            if search_button:
                self.click_element_safe(search_button)
            else:
                search_input.send_keys(Keys.ENTER)

        self.wait_for_search_results()

    @allure.step("Ожидание ввода текста")
    def wait_for_text_input(self,
                            element,
                            expected_text: str, timeout: int = 5) -> None:
        """
        Ожидает пока в элементе появится ожидаемый текст

        Args:
            element: WebElement
            expected_text: Ожидаемый текст
            timeout: Время ожидания в секундах
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: element.get_attribute('value') == expected_text
            )
        except TimeoutException:
            print(
                f"Предупреждение: текст '{expected_text}'"
                f"не ввелся за {timeout} секунд")

    @allure.step("Ожидание результатов поиска")
    def wait_for_search_results(self, timeout: int = 5) -> None:
        """
        Ожидает появления результатов поиска

        Args:
            timeout: Время ожидания в секундах
        """
        self.wait_for_page_load()

        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: any(
                    len(self.find_elements(locator, timeout=1)) > 0
                    for locator in self.search_results_locators
                ) or self.is_no_results_message_present()
            )
        except TimeoutException:
            print(
                "Предупреждение:"
                "результаты поиска не появились в течение таймаута")

    @allure.step("Проверка наличия сообщения об отсутствии результатов")
    def is_no_results_message_present(self) -> bool:
        """
        Проверяет есть ли сообщение об отсутствии результатов

        Returns:
            bool: True если есть сообщение "ничего не найдено" или подобное
        """
        no_results_phrases = [
            "ничего не найдено",
            "не найдено",
            "no results",
            "ничего не нашлось"
        ]

        page_text = self.driver.page_source.lower()
        return any(phrase in page_text for phrase in no_results_phrases)

    @allure.step("Безопасный клик по элементу")
    def click_element_safe(self, element) -> None:
        """
        Безопасный клик по элементу с обработкой исключений

        Args:
            element: WebElement для клика
        """
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)

    @allure.step("Получение количества результатов поиска")
    def get_search_results_count(self) -> int:
        """
        Получает количество найденных результатов

        Returns:
            int: Количество результатов
        """
        try:
            # Пробуем разные локаторы для результатов
            for locator in self.search_results_locators:
                try:
                    results = self.find_elements(locator, timeout=5)
                    if results:
                        print(
                            f"Найдено результатов по локатору {locator}:"
                            f"{len(results)}"
                        )
                        return len(results)
                except TimeoutException:
                    continue

            film_links = self.driver.find_elements(
                By.XPATH, "//a[contains(@href, '/film/')]"
            )
            print(f"Найдено ссылок на фильмы: {len(film_links)}")
            return len(film_links)

        except Exception as e:
            print(f"Ошибка при подсчете результатов: {e}")
            return 0

    @allure.step("Получение заголовков результатов поиска")
    def get_search_results_titles(self) -> List[str]:
        """
        Получает заголовки всех найденных результатов

        Returns:
            List[str]: Список заголовков в нижнем регистре
        """
        titles = []
        try:
            for locator in self.search_results_locators:
                try:
                    results = self.find_elements(locator, timeout=5)
                    print(
                        f"Найдено элементов по локатору {locator}:"
                        f"{len(results)}")

                    for i, result in enumerate(results):
                        try:
                            title_text = result.text
                            if title_text and len(title_text.strip()) > 0:
                                print(f"Результат {i}: '{title_text}'")
                                titles.append(title_text.lower())
                            else:
                                inner_texts = result.find_elements(
                                    By.XPATH, ".//*[text()]"
                                )
                                for inner in inner_texts:
                                    inner_text = inner.text.strip()
                                    if inner_text:
                                        print(
                                            f"Результат {i} (вложенный):"
                                            f"'{inner_text}'")
                                        titles.append(inner_text.lower())
                        except Exception as inner_error:
                            print(
                                f"Ошибка при обработке результата {i}:"
                                f"{inner_error}")
                            continue

                    if titles:
                        break
                except TimeoutException:
                    continue

            if not titles:
                print("Пробуем альтернативный поиск заголовков...")
                title_elements = self.driver.find_elements(
                    By.XPATH,
                    "//h1 | //h2 | //h3 | //h4 |"
                    "//div[contains(@class, 'title')]"
                )
                for i, element in enumerate(title_elements):
                    text = element.text.strip()
                    if text and len(text) > 1:
                        print(f"Альтернативный заголовок {i}: '{text}'")
                        titles.append(text.lower())

        except Exception as e:
            print(f"Ошибка при получении заголовков: {e}")

        print(f"Всего собрано заголовков: {len(titles)}")
        return titles

    @allure.step("Проверка наличия результатов с текстом '{text}'")
    def has_results_with_text(self, text: str) -> bool:
        """
        Проверяет наличие результатов с указанным текстом

        Args:
            text: Текст для поиска в результатах

        Returns:
            bool: True если есть совпадения
        """
        titles = self.get_search_results_titles()
        search_text = text.lower()
        print(f"Ищем текст '{search_text}' в {len(titles)} заголовках")

        for i, title in enumerate(titles):
            if search_text in title:
                print(f"Найдено совпадение в заголовке {i}: '{title}'")
                return True

        print(f"Текст '{search_text}' не найден ни в одном заголовке")
        return False

    @allure.step("Получение текущего URL")
    def get_current_url(self) -> str:
        """
        Получает текущий URL страницы

        Returns:
            str: Текущий URL
        """
        return self.driver.current_url

    @allure.step("Проверка что мы на странице результатов поиска")
    def is_on_search_results_page(self) -> bool:
        """
        Проверяет что мы находимся на странице результатов поиска

        Returns:
            bool: True если это страница результатов
        """
        current_url = self.get_current_url()
        is_search_page = (
                'search' in current_url.lower() or
                'query' in current_url.lower()
        )
        print(f"Текущий URL: {current_url}")
        print(f"Это страница результатов: {is_search_page}")
        return is_search_page

    @allure.step("Получение HTML страницы для отладки")
    def get_page_html_debug(self) -> str:
        """
        Получает HTML страницы для отладки

        Returns:
            str: HTML страницы
        """
        return self.driver.page_source

    @allure.step("Поиск элементов содержащих текст '{text}'")
    def find_elements_containing_text(self, text: str) -> List[str]:
        """
        Находит все элементы содержащие указанный текст

        Args:
            text: Текст для поиска

        Returns:
            List[str]: Список текстов элементов
        """
        elements = self.driver.find_elements(
            By.XPATH, f"//*[contains(text(), '{text}')]"
        )
        found_texts = []
        for element in elements:
            element_text = element.text.strip()
            if element_text:
                found_texts.append(element_text)
        return found_texts
