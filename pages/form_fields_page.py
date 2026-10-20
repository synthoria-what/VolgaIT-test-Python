import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class FormFieldsPage(BasePage):
    TOOLS = (By.XPATH, "//label[normalize-space()='Automation tools']/following-sibling::ul[1]/li")
    MESSAGE = (By.ID, "message")

    def open(self):
        super().open("/form-fields/")
        self.find(self.MESSAGE)

    @allure.step("Получить через Selenium названия Automation tools")
    def get_tools(self):
        self.find(self.TOOLS)
        elements = self.driver.find_elements(*self.TOOLS)
        tools = []
        for element in elements:
            tools.append(element.text)
        return tools

    @allure.step("Заполнить Message списком инструментов через запятую")
    def fill_message(self, tools):
        message = ", ".join(tools)
        self.find(self.MESSAGE).clear()
        self.find(self.MESSAGE).send_keys(message)
