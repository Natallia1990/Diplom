import pytest
import allure
from search_page import SearchPage


@allure.epic("UI Tests")
class TestKinopoiskUI:

    @allure.story("Отображение поля поиска")
    def test_search_input_displayed(self, search_page: SearchPage) -> None:
        """Поле ввода поискового запроса отображается корректно"""
        is_displayed: bool = search_page.is_search_input_displayed()
        assert is_displayed, ("Поле ввода поиска"
                              "должно отображаться на странице")

    @allure.story("Базовый поиск")
    def test_basic_search_functionality(self, search_page: SearchPage) -> None:
        """Тест базового поиска"""
        search_page.perform_search("матрица")

        results_count: int = search_page.get_search_results_count()
        assert results_count > 0, "Поиск должен возвращать результаты"

        has_relevant_results: bool = (search_page.
                                      has_results_with_text("матриц"))
        assert has_relevant_results, "Должны быть релевантные результаты"

    @allure.story("Поиск по частичному совпадению")
    @pytest.mark.parametrize("query", ["тар", "аме"])
    def test_partial_match_search(self,
                                  search_page: SearchPage, query: str) -> None:
        """Поиск работает по частичному совпадению"""
        search_page.perform_search(query)

        results_count: int = search_page.get_search_results_count()
        assert results_count > 0, (f"По запросу"
                                   f"'{query}' должны быть результаты")

    @allure.story("Поиск популярного фильма")
    def test_popular_movie_search(self, search_page: SearchPage) -> None:
        """Тест поиска популярного фильма"""
        search_page.perform_search("Титаник")

        results_count: int = search_page.get_search_results_count()
        assert results_count > 0, "Должны быть результаты для 'Титаник'"
