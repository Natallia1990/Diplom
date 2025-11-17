import requests
import allure
from typing import Dict, Any
from config import Settings, APISettings


class KinopoiskAPIClient:
    def __init__(self) -> None:
        self.base_url = Settings.API_BASE_URL
        self.token = Settings.API_TOKEN
        self.session = requests.Session()
        self.session.headers.update({
            "X-API-KEY": self.token
        })
        self.session.verify = False

    @allure.step("Поиск фильмов по запросу: '{query}'")
    def search_movies(
            self, query: str, page: int = 1,
            limit: int = 10) -> Dict[str, Any]:
        """
        Выполняет поиск фильмов по названию

        Args:
            query: Поисковый запрос
            page: Номер страницы
            limit: Количество результатов на странице

        Returns:
            Dict с результатами поиска
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

    @allure.step("Проверка наличия результатов поиска")
    def has_search_results(self, search_response: Dict[str, Any]) -> bool:
        """
        Проверяет наличие результатов в ответе поиска

        Args:
            search_response: Ответ от API поиска

        Returns:
            bool: True если есть результаты
        """
        return search_response.get("docs") and len(search_response["docs"]) > 0
