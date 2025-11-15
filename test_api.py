import pytest
import allure
from kinopoisk_client import KinopoiskAPIClient
from test_data import TestData


@allure.epic("API Tests")
@allure.feature("Поиск фильмов через API")
class TestKinopoiskAPI:
    """Тесты API Кинопоиска"""

    @allure.story("Поиск по различным запросам")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("test_data", TestData.API_SEARCH_QUERIES)
    def test_search_by_different_queries(
            self, api_client: KinopoiskAPIClient, test_data):
        """
        Тестирование поиска фильмов по различным типам запросов

        Args:
            api_client: Клиент API
            test_data: Данные для теста
        """
        with allure.step(f"Выполнение поиска по запросу: '{test_data.query}'"):
            response = api_client.search_movies(
                query=test_data.query,
                limit=test_data.expected_min_results
            )

        with allure.step("Проверка статус кода ответа"):
            assert response is not None

        with allure.step("Проверка наличия результатов"):
            has_results = api_client.has_search_results(response)
            assert has_results, (f"По запросу"
                                 f"'{test_data.query}' должны быть результаты")

        with allure.step("Проверка структуры ответа"):
            first_movie = api_client.get_first_search_result(response)
            assert first_movie is not None, (
                "Должен быть хотя бы один результат")

            is_valid_structure = api_client.validate_movie_response_structure(
                first_movie)
            assert is_valid_structure, (
                "Структура ответа должна содержать все необходимые поля")

    @allure.story("Поиск с пагинацией")
    @allure.severity(allure.severity_level.NORMAL)
    def test_search_pagination(self, api_client: KinopoiskAPIClient):
        """Тестирование пагинации в поиске"""
        query = "фильм"

        with allure.step("Поиск на первой странице"):
            page1_response = api_client.search_movies(
                query=query, page=1, limit=5)
            page1_total = page1_response.get("total", 0)
            page1_docs = len(page1_response.get("docs", []))

        with allure.step("Проверка что есть результаты для пагинации"):
            assert page1_total > 5, ("Должно быть достаточно результатов"
                                     "для тестирования пагинации")

        with allure.step("Поиск на второй странице"):
            page2_response = api_client.search_movies(
                query=query, page=2, limit=5)
            page2_docs = len(page2_response.get("docs", []))

        with allure.step("Проверка что страницы возвращают результаты"):
            assert page1_docs > 0, ("Первая страница"
                                    "должна содержать результаты")
            assert page2_docs > 0, ("Вторая страница"
                                    "должна содержать результаты")
