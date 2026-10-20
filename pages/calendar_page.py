import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class CalendarPage(BasePage):
    DATE = (By.CSS_SELECTOR, "input.date")
    CALENDAR = (By.CSS_SELECTOR, ".dp-cal")
    MONTH = (By.CSS_SELECTOR, ".dp-cal-month")
    YEAR = (By.CSS_SELECTOR, ".dp-cal-year")
    NEXT = (By.CSS_SELECTOR, ".dp-next")
    PREVIOUS = (By.CSS_SELECTOR, ".dp-prev")

    def open(self):
        super().open("/calendars/")
        self.find(self.DATE)

    @allure.step("Открыть календарь")
    def open_calendar(self):
        self.click(self.DATE)
        self.find(self.CALENDAR)

    def displayed_month(self):
        months = ["January", "February", "March", "April", "May", "June",
                  "July", "August", "September", "October", "November", "December"]
        month = months.index(self.find(self.MONTH).text) + 1
        year = int(self.find(self.YEAR).text)
        return year, month

    @allure.step("Перейти к следующему месяцу")
    def next_month(self):
        old_month = self.find(self.MONTH)
        self.click(self.NEXT)
        self.wait.until(EC.staleness_of(old_month))
        self.find(self.MONTH)

    @allure.step("Перейти к предыдущему месяцу")
    def previous_month(self):
        old_month = self.find(self.MONTH)
        self.click(self.PREVIOUS)
        self.wait.until(EC.staleness_of(old_month))
        self.find(self.MONTH)

    @allure.step("Выбрать день {day} текущего месяца")
    def select_day(self, day):
        locator = (By.XPATH, "//button[contains(@class, 'dp-day') "
                   "and not(contains(@class, 'dp-edge-day')) and text()='" + str(day) + "']")
        self.click(locator)
        self.wait_hidden(self.CALENDAR)

    @allure.step("Ввести дату {value}")
    def enter_date(self, value):
        field = self.find(self.DATE)
        field.click()
        field.send_keys(Keys.CONTROL, "a")
        field.send_keys(value)
        field.send_keys(Keys.TAB)

    @allure.step("Очистить дату")
    def clear_date(self):
        field = self.find(self.DATE)
        field.click()
        field.send_keys(Keys.CONTROL, "a")
        field.send_keys(Keys.BACKSPACE)
        field.send_keys(Keys.TAB)

    def value(self):
        return self.find(self.DATE).get_attribute("value")

    @allure.step("Проверить ошибку ввода даты")
    def assert_invalid_date(self):
        self.wait.until(EC.element_attribute_to_include(self.DATE, "aria-invalid"))
        assert self.find(self.DATE).get_attribute("aria-invalid") == "true"
        error = self.find((By.CSS_SELECTOR, ".grunion-field-date-wrap .contact-form__input-error"))
        assert error.text.strip() != ""
