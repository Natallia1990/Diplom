import unittest
import time
from api_client import KinopoiskAPIClient
from test_data import TestData
from config import Config


class TestKinopoiskAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api_client = KinopoiskAPIClient()
        cls.test_cases = TestData.TEST_CASES

    def run_test_case(self, test_case):
        """
        Запуск отдельного тестового случая
        """
        print(f"\n{'=' * 60}")
        print(f"Running Test {test_case['id']}: {test_case['name']}")
        print(f"{'=' * 60}")

        # Подготовка параметров
        token = test_case.get("token", "valid")
        if token == "invalid":
            token = Config.INVALID_TOKEN
        elif token is None:
            token = None
        else:
            token = Config.VALID_TOKEN

        method = test_case.get("method", "GET")

        # Отправка запроса
        start_time = time.time()
        response = self.api_client.search_movies(
            query=test_case.get("query"),
            token=token,
            method=method
        )
        response_time = time.time() - start_time

        # Проверка что ответ получен
        self.assertIsNotNone(response, "Response should not be None")

        # Валидация ответа
        validation_results = self.api_client.validate_response(
            response, test_case["expected_status"], test_case
        )

        # Вывод результатов
        print(f"Request URL: {response.url}")
        print(f"Response Time: {response_time:.2f}s")
        print(f"Status Code: {response.status_code} (expected: {test_case['expected_status']})")

        all_passed = True
        for result in validation_results:
            status = "PASSED" if result["passed"] else "FAILED"
            print(f"  {result['check']}: {status}")
            if not result["passed"]:
                print(f"    Expected: {result['expected']}")
                print(f"    Actual: {result['actual']}")
                all_passed = False

        # Assertions для unittest
        self.assertEqual(response.status_code, test_case["expected_status"],
                         f"Status code should be {test_case['expected_status']}")

        if test_case["expected_status"] == 200 and test_case["should_contain_result"]:
            data = response.json()
            self.assertIn("docs", data, "Response should contain 'docs' field")
            self.assertGreater(len(data["docs"]), 0, "Response should contain at least one movie")

        print(f"Test Result: {'PASSED' if all_passed else 'FAILED'}")
        return all_passed

    def test_01_cyrillic_search(self):
        """Тест 1: Поиск по названию на кириллице"""
        test_case = self.test_cases[0]
        self.run_test_case(test_case)

    def test_02_latin_search(self):
        """Тест 2: Поиск по названию на латинице"""
        test_case = self.test_cases[1]
        self.run_test_case(test_case)

    def test_03_numeric_search(self):
        """Тест 3: Поиск по названию с цифрами"""
        test_case = self.test_cases[2]
        self.run_test_case(test_case)

    def test_04_space_search(self):
        """Тест 4: Поиск по пробелу"""
        test_case = self.test_cases[3]
        self.run_test_case(test_case)

    def test_05_empty_search(self):
        """Тест 5: Пустой поиск"""
        test_case = self.test_cases[4]
        self.run_test_case(test_case)

    def test_06_no_token_search(self):
        """Тест 6: Поиск без токена"""
        test_case = self.test_cases[5]
        self.run_test_case(test_case)

    def test_07_invalid_token_search(self):
        """Тест 7: Поиск с неактуальным токеном"""
        test_case = self.test_cases[6]
        self.run_test_case(test_case)

    def test_08_wrong_method_search(self):
        """Тест 8: Поиск с некорректным методом"""
        test_case = self.test_cases[7]
        self.run_test_case(test_case)

    def test_all_cases_in_sequence(self):
        """Запуск всех тестов последовательно"""
        print("Running all test cases in sequence...")
        passed_count = 0

        for test_case in self.test_cases:
            try:
                if self.run_test_case(test_case):
                    passed_count += 1
                # Небольшая пауза между запросами чтобы не превысить лимиты API
                time.sleep(0.5)
            except Exception as e:
                print(f"Test {test_case['id']} failed with exception: {e}")

        print(f"\n{'=' * 60}")
        print(f"FINAL RESULTS: {passed_count}/{len(self.test_cases)} tests passed")
        print(f"{'=' * 60}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
