pytest                    # запуск всех тестов
pytest --durations=5      # показать 5 самых медленных тестов
pytest --setup-plan       # порядок выполнения setup/teardown
pytest --fixtures         # список доступных фикстур
pytest --markers          # список зарегистрированных маркеров
pytest --co               # структура тестов без запуска
pytest test_user_api.py   # запуск одного файла
pytest -v                 # подробный вывод
pytest -q                 # краткий режим
pytest -x                 # остановка на первом упавшем тесте
pytest -k create_user     # запуск по имени (подстрока)
pytest -m slow            # запуск всех тестов, где марка slow
