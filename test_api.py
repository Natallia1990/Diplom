import pytest
import allure
import urllib3
from typing import Dict, Any
from kinopoisk_client import KinopoiskAPIClient

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@allure.epic("API Tests")
class TestKinopoiskAPI:

    @allure.story("Поиск по различным запросам")
    @pytest.mark.parametrize("query", ["титаник", "Titanic", "2024", " "])
    def test_search_by_different_queries(
            self, api_client: KinopoiskAPIClient, query: str) -> None:
        """
        Тестирование поиска фильмов по различным типам запросов

        Args:
            api_client: Клиент API
            query: Поисковый запрос
        """
        response: Dict[str, Any] = api_client.search_movies(
            query=query, limit=1)

        assert api_client.has_search_results(response)

        movie: Dict[str, Any] = response["docs"][0]
        assert "name" in movie
        assert "year" in movie

    @allure.story("Поиск с пагинацией")
    def test_search_pagination(self, api_client: KinopoiskAPIClient) -> None:
        """Тестирование пагинации в поиске"""
        page1_response: Dict[str, Any] = api_client.search_movies(
            query="фильм", page=1, limit=5)
        page2_response: Dict[str, Any] = api_client.search_movies(
            query="фильм", page=2, limit=5)

        page1_docs: int = len(page1_response.get("docs", []))
        page2_docs: int = len(page2_response.get("docs", []))

        assert page1_docs > 0
        assert page2_docs > 0
