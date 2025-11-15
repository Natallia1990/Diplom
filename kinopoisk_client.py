import requests
import allure
from typing import Dict, List, Optional, Any
from config.settings import Settings, APISettings
from config.test_data import TestData


class KinopoiskAPIClient:
    """Клиент для работы с API Кинопоиска"""

    def __init__(self):
        self.base_url = Settings.API_BASE_URL
        self.token = Settings.API_TOKEN
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "X-API-KEY": self.token
        })

    @allure.step("API: Поиск фильмов по запросу '{query}'")
    def search_movies(self, query: str, page: int = 1, limit: int = 10) -> Dict[str, Any]:
        """
        Выполняет поиск фильмов по названию

        Args:
            query: Поисковый запрос
            page: Номер страницы
            limit: Количество результатов на странице

        Returns:
            Dict: Ответ API с результатами поиска
        """
        url = f"{self.base_url}{APISettings.MOVIE_SEARCH}"
        params = {
            "page": page,
            "limit": limit,
            "query": query
        }

        response = self.session.get(url, params=params)
        response.raise_for_status()

        return response.json()

    @allure.step("API: Получение информации о фильме по ID {movie_id}")
    def get_movie_by_id(self, movie_id: int) -> Dict[str, Any]:
        """
        Получает информацию о фильме по ID

        Args:
            movie_id: ID фильма

        Returns:
            Dict: Информация о фильме
        """
        url = f"{self.base_url}{APISettings.MOVIE}/{movie_id}"

        response = self.session.get(url)
        response.raise_for_status()

        return response.json()

    @allure.step("API: Проверка структуры ответа")
    def validate_movie_response_structure(self, movie_data: Dict[str, Any]) -> bool:
        """
        Проверяет структуру ответа с информацией о фильме

        Args:
            movie_data: Данные о фильме

        Returns:
            bool: True если структура корректна
        """
        required_fields = TestData.MOVIE_RESPONSE_FIELDS
        return all(field in movie_data for field in required_fields)

    @allure.step("API: Проверка наличия результатов поиска")
    def has_search_results(self, search_response: Dict[str, Any]) -> bool:
        """
        Проверяет наличие результатов в ответе поиска

        Args:
            search_response: Ответ от API поиска

        Returns:
            bool: True если есть результаты
        """
        return (search_response.get("docs") and
                len(search_response["docs"]) > 0 and
                search_response.get("total") > 0)

    @allure.step("API: Получение первого результата поиска")
    def get_first_search_result(self, search_response: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Получает первый результат из ответа поиска

        Args:
            search_response: Ответ от API поиска

        Returns:
            Optional[Dict]: Первый результат или None
        """
        if self.has_search_results(search_response):
            return search_response["docs"][0]
        return None
