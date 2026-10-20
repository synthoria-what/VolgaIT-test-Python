import allure
import pytest

from pages.modals_page import ModalsPage


@pytest.fixture
def modals(driver):
    page = ModalsPage(driver)
    page.open()
    return page


@pytest.mark.positive
@allure.title("MOD-P01: простое окно открывается и содержит текст")
def test_simple_modal_content(modals):
    modals.open_simple()
    modal = modals.find(modals.SIMPLE)
    assert "Simple Modal" in modal.text
    assert "Hi, I’m a simple modal." in modal.text


@pytest.mark.positive
@allure.title("MOD-P02: простое окно закрывается крестиком")
def test_close_simple_modal(modals):
    modals.open_simple()
    modals.close_simple()
    assert not modals.driver.find_element(*modals.SIMPLE).is_displayed()


@pytest.mark.positive
@allure.title("MOD-P03: простое окно открывается повторно")
def test_reopen_simple_modal(modals):
    modals.open_simple()
    modals.close_simple()
    modals.open_simple()
    assert modals.find(modals.SIMPLE).is_displayed()


@pytest.mark.positive
@allure.title("MOD-P04: окно формы содержит Name, Email и Message")
def test_form_modal_fields(modals):
    modals.open_form()
    assert modals.find(modals.NAME).is_displayed()
    assert modals.find(modals.EMAIL).is_displayed()
    assert modals.find(modals.MESSAGE).is_displayed()


@pytest.mark.positive
@allure.title("MOD-P05: окно формы закрывается крестиком")
def test_close_form_modal(modals):
    modals.open_form()
    modals.close_form()
    assert not modals.driver.find_element(*modals.FORM).is_displayed()


@pytest.mark.positive
@allure.title("MOD-P06: окно формы закрывается по Escape")
def test_close_form_modal_with_escape(modals):
    modals.open_form()
    modals.escape_form()
    assert not modals.driver.find_element(*modals.FORM).is_displayed()


@pytest.mark.positive
@allure.title("MOD-P07: поля формы принимают введённые данные")
def test_fill_form_modal(modals):
    modals.open_form()
    modals.fill_form("Иван Тестов", "tester@example.com", "Проверка формы")
    assert modals.find(modals.NAME).get_attribute("value") == "Иван Тестов"
    assert modals.find(modals.EMAIL).get_attribute("value") == "tester@example.com"
    assert modals.find(modals.MESSAGE).get_attribute("value") == "Проверка формы"


@pytest.mark.negative
@allure.title("MOD-N01: форма без обязательного имени не отправляется")
def test_form_requires_name(modals):
    modals.open_form()
    modals.fill_form("", "tester@example.com", "Проверка обязательного имени")
    modals.submit()
    modals.assert_field_error("name", "This field is required.")


@pytest.mark.negative
@allure.title("MOD-N02: Email без @ вызывает ошибку")
def test_email_without_at_is_invalid(modals):
    modals.open_form()
    modals.fill_form("Иван Тестов", "invalid-email", "Проверка почты")
    modals.submit()
    modals.assert_field_error("email", "Please enter a valid email address")


@pytest.mark.negative
@allure.title("MOD-N03: Email без имени пользователя вызывает ошибку")
def test_email_without_username_is_invalid(modals):
    modals.open_form()
    modals.fill_form("Иван Тестов", "@example.com", "Проверка почты")
    modals.submit()
    modals.assert_field_error("email", "Please enter a valid email address")
