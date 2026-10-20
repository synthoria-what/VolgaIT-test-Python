import allure
import pytest

from pages.calendar_page import CalendarPage


@pytest.fixture
def calendar(driver):
    page = CalendarPage(driver)
    page.open()
    return page


@pytest.mark.positive
@allure.title("CAL-P01: календарь открывается при нажатии на поле")
def test_calendar_opens(calendar):
    calendar.open_calendar()
    assert calendar.find(calendar.CALENDAR).is_displayed()
    assert calendar.value() == ""


@pytest.mark.positive
@allure.title("CAL-P02: выбор дня текущего месяца")
def test_select_day_in_current_month(calendar):
    calendar.open_calendar()
    year, month = calendar.displayed_month()
    calendar.select_day(15)
    assert calendar.value() == f"{year}-{month:02d}-15"


@pytest.mark.positive
@allure.title("CAL-P03: переход вперёд и выбор дня")
def test_select_day_in_next_month(calendar):
    calendar.open_calendar()
    year, month = calendar.displayed_month()
    if month == 12:
        year = year + 1
        month = 1
    else:
        month = month + 1
    calendar.next_month()
    assert calendar.displayed_month() == (year, month)
    calendar.select_day(15)
    assert calendar.value() == f"{year}-{month:02d}-15"


@pytest.mark.positive
@allure.title("CAL-P04: переход назад и выбор дня")
def test_select_day_in_previous_month(calendar):
    calendar.open_calendar()
    year, month = calendar.displayed_month()
    if month == 1:
        year = year - 1
        month = 12
    else:
        month = month - 1
    calendar.previous_month()
    assert calendar.displayed_month() == (year, month)
    calendar.select_day(15)
    assert calendar.value() == f"{year}-{month:02d}-15"


@pytest.mark.positive
@allure.title("CAL-P05: ручной ввод правильной даты")
def test_enter_valid_date(calendar):
    calendar.enter_date("2026-10-20")
    assert calendar.value() == "2026-10-20"
    assert calendar.find(calendar.DATE).get_attribute("aria-invalid") != "true"


@pytest.mark.positive
@allure.title("CAL-P06: ручной ввод 29 февраля високосного года")
def test_enter_leap_year_date(calendar):
    calendar.enter_date("2028-02-29")
    assert calendar.value() == "2028-02-29"
    assert calendar.find(calendar.DATE).get_attribute("aria-invalid") != "true"


@pytest.mark.positive
@allure.title("CAL-P07: очистка выбранной даты")
def test_clear_date(calendar):
    calendar.enter_date("2026-10-20")
    calendar.clear_date()
    assert calendar.value() == ""
    assert calendar.find(calendar.DATE).get_attribute("aria-invalid") != "true"


@pytest.mark.negative
@allure.title("CAL-N01: текст вместо даты вызывает ошибку")
def test_text_is_not_a_date(calendar):
    calendar.enter_date("not-a-date")
    calendar.assert_invalid_date()


@pytest.mark.negative
@allure.title("CAL-N02: 30 февраля вызывает ошибку")
def test_nonexistent_date_is_invalid(calendar):
    calendar.enter_date("2026-02-30")
    calendar.assert_invalid_date()


@pytest.mark.negative
@allure.title("CAL-N03: формат ДД/ММ/ГГГГ вызывает ошибку")
def test_wrong_date_format_is_invalid(calendar):
    calendar.enter_date("20/10/2026")
    calendar.assert_invalid_date()
