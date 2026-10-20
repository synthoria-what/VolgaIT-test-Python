import allure
import pytest

from pages.form_fields_page import FormFieldsPage


@pytest.mark.positive
@allure.title("FORM-P01: Message содержит Automation tools через запятую")
def test_fill_message_with_automation_tools(driver):
    page = FormFieldsPage(driver)
    page.open()
    tools = page.get_tools()
    assert tools == ["Selenium", "Playwright", "Cypress", "Appium", "Katalon Studio"]

    page.fill_message(tools)

    with allure.step("Проверить значение Message"):
        assert page.find(page.MESSAGE).get_attribute("value") == ", ".join(tools)
