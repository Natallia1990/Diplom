from dataclasses import dataclass


@dataclass
class SearchTestData:
    """Тестовые данные для поиска"""
    query: str
    expected_min_results: int
    description: str


@dataclass
class CountrySearchData:
    """Тестовые данные для поиска по стране"""
    country: str
    expected_min_results: int


@dataclass
class DistributorSearchData:
    """Тестовые данные для поиска по прокатчику"""
    distributor: str
    expected_min_results: int


class TestData:
    """Коллекция тестовых данных"""

    # Данные для UI тестов
    UI_SEARCH_QUERIES = [
        SearchTestData("матрица", 1, "Поиск популярного фильма"),
        SearchTestData("тар", 3, "Поиск по частичному совпадению"),
        SearchTestData("аме", 3, "Поиск по частичному совпадению 2"),
        SearchTestData("2023", 1, "Поиск по году"),
        SearchTestData(" ", 10, "Поиск по пробелу")
    ]

    UI_COUNTRY_SEARCH = [
        CountrySearchData("США", 5),
        CountrySearchData("Россия", 3),
        CountrySearchData("Франция", 1)
    ]

    UI_DISTRIBUTOR_SEARCH = [
        DistributorSearchData("WDSSPR", 1),
        DistributorSearchData("Централ Партнершип", 1),
        DistributorSearchData("Disney", 1)
    ]

    # Данные для API тестов
    API_SEARCH_QUERIES = [
        SearchTestData("титаник", 1, "Поиск на кириллице"),
        SearchTestData("Titanic", 1, "Поиск на латинице"),
        SearchTestData("2024", 1, "Поиск по году"),
        SearchTestData(" ", 1, "Поиск по пробелу")
    ]

    # Ожидаемые структуры ответов API
    MOVIE_RESPONSE_FIELDS = [
        "id", "name", "year", "description", "rating", "poster"
    ]
