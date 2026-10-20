# Результаты проверки

## Chrome, полный набор

```powershell
.\.venv\Scripts\python.exe -m pytest --headless --junitxml=tmp/results.xml
```

Python 3.12.14, pytest 9.1.1, Selenium 4.51.0, Chrome 155.0.8059.85.

Результат: **31 passed**, время 297,85 секунды.

| Страница | Позитивных | Негативных | Успешно |
| --- | ---: | ---: | ---: |
| Calendars | 7 | 3 | 10 |
| Modals | 7 | 3 | 10 |
| Ads | 7 | 3 | 10 |
| Form Fields | 1 | 0 | 1 |
| Всего | 22 | 9 | 31 |

## Firefox, короткая проверка

```powershell
.\.venv\Scripts\python.exe -m pytest --browser firefox --headless tests/test_calendars.py::test_select_day_in_current_month tests/test_modals.py::test_form_requires_name tests/test_ads.py::test_close_ad tests/test_form_fields.py --alluredir=tmp/firefox-results --clean-alluredir --junitxml=tmp/firefox.xml
```

Результат: **4 passed**, время 95,44 секунды.
Проверены выбор даты, обязательное имя в форме, закрытие рекламы и заполнение
Message списком инструментов. Полный набор из 31 теста в Firefox не запускался.

## Отчёт и скриншоты

В `allure-results` проверены 31 результат со статусом passed.
Собран самостоятельный HTML-отчёт `allure-report/index.html`.
Отчёт открыт в Chrome: отображаются 31 тест и 100% успешных результатов.

Отдельным временным тестом с намеренным падением проверена обработка ошибок:
создаётся PNG в папке `screenshots`, а в Allure прикладываются изображение и
URL страницы. Этот технический тест находится вне основного набора, а его
результаты сохранены отдельно в `tmp/screenshot-results`.

Проверки выполнялись на реальном внешнем сайте, без подмены ответов или элементов.
Успешная отправка валидных контактных форм на сервер в набор не входит;
проверены ввод данных и клиентские ошибки.
