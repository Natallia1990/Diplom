class TestData:
    # Тестовые запросы
    TEST_CASES = [
        {
            "id": 1,
            "name": "Поиск по названию на кириллице",
            "query": "титаник",
            "expected_status": 200,
            "should_contain_result": True
        },
        {
            "id": 2,
            "name": "Поиск по названию на латинице",
            "query": "Titanik",
            "expected_status": 200,
            "should_contain_result": True
        },
        {
            "id": 3,
            "name": "Поиск по названию с цифрами",
            "query": "2025",
            "expected_status": 200,
            "should_contain_result": True
        },
        {
            "id": 4,
            "name": "Поиск по пробелу",
            "query": " ",
            "expected_status": 200,
            "should_contain_result": True
        },
        {
            "id": 5,
            "name": "Пустой поиск",
            "query": None,
            "expected_status": 200,
            "should_contain_result": True
        },
        {
            "id": 6,
            "name": "Поиск без токена",
            "query": "Титаник",
            "expected_status": 401,
            "should_contain_result": False,
            "use_token": False,
            "expected_message": "В запросе не указан токен!"
        },
        {
            "id": 7,
            "name": "Поиск с неактуальным токеном",
            "query": "Титаник",
            "expected_status": 401,
            "should_contain_result": False,
            "token": "invalid",
            "expected_message": "Переданный токен некорректен!"
        },
        {
            "id": 8,
            "name": "Поиск с некорректным методом",
            "query": "Титаник",
            "expected_status": 404,
            "should_contain_result": False,
            "method": "POST"
        }
    ]
