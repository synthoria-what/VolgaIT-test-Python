import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class ModalsPage(BasePage):
    SIMPLE = (By.ID, "popmake-1318")
    FORM = (By.ID, "popmake-674")
    NAME = (By.CSS_SELECTOR, "#popmake-674 input.name")
    EMAIL = (By.CSS_SELECTOR, "#popmake-674 input.email")
    MESSAGE = (By.CSS_SELECTOR, "#popmake-674 textarea.textarea")

    def open(self):
        super().open("/modals/")
        self.find((By.ID, "simpleModal"))

    @allure.step("Открыть простое модальное окно")
    def open_simple(self):
        self.click((By.ID, "simpleModal"))
        self.find(self.SIMPLE)

    @allure.step("Закрыть простое окно крестиком")
    def close_simple(self):
        self.click((By.CSS_SELECTOR, "#popmake-1318 .pum-close"))
        self.wait_hidden(self.SIMPLE)

    @allure.step("Открыть окно с формой")
    def open_form(self):
        self.click((By.ID, "formModal"))
        self.find(self.FORM)
        self.find(self.NAME)

    @allure.step("Закрыть окно с формой крестиком")
    def close_form(self):
        self.click((By.CSS_SELECTOR, "#popmake-674 .pum-close"))
        self.wait_hidden(self.FORM)

    @allure.step("Закрыть окно с формой клавишей Escape")
    def escape_form(self):
        self.find(self.NAME).send_keys(Keys.ESCAPE)
        self.wait_hidden(self.FORM)

    @allure.step("Заполнить форму: имя {name}, почта {email}")
    def fill_form(self, name, email, message):
        self.find(self.NAME).send_keys(name)
        self.find(self.EMAIL).send_keys(email)
        self.find(self.MESSAGE).send_keys(message)

    @allure.step("Нажать Submit")
    def submit(self):
        self.click((By.CSS_SELECTOR, "#popmake-674 button[type=submit]"))

    @allure.step("Проверить ошибку поля {field_name}")
    def assert_field_error(self, field_name, expected_text):
        if field_name == "name":
            locator = self.NAME
            error = (By.CSS_SELECTOR, "#popmake-674 .grunion-field-name-wrap .contact-form__input-error")
        else:
            locator = self.EMAIL
            error = (By.CSS_SELECTOR, "#popmake-674 .grunion-field-email-wrap .contact-form__input-error")

        self.wait.until(EC.text_to_be_present_in_element(error, expected_text))
        assert self.find(locator).get_attribute("aria-invalid") == "true"
        assert self.find(self.FORM).is_displayed()
        form = self.driver.find_element(By.CSS_SELECTOR, "#popmake-674 form")
        assert "submission-success" not in form.get_attribute("class")
