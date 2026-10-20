from pathlib import Path

import allure
import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


def pytest_addoption(parser):
    parser.addoption("--browser", choices=["chrome", "firefox"], default="chrome")
    parser.addoption("--headless", action="store_true", help="Запустить без окна браузера")


@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser")

    with allure.step("Запустить браузер " + browser):
        if browser == "chrome":
            options = webdriver.ChromeOptions()
            if request.config.getoption("--headless"):
                options.add_argument("--headless=new")
            browser_driver = webdriver.Chrome(options=options)
        else:
            options = webdriver.FirefoxOptions()
            if request.config.getoption("--headless"):
                options.add_argument("-headless")
            browser_driver = webdriver.Firefox(options=options)

        # Сохраняем драйвер сразу, чтобы сделать скриншот и при ошибке настройки.
        request.node.browser_driver = browser_driver

    try:
        browser_driver.set_window_size(1440, 1000)
        browser_driver.set_page_load_timeout(45)
        yield browser_driver
    finally:
        browser_driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    result = yield
    report = result.get_result()

    if report.failed:
        browser_driver = getattr(item, "browser_driver", None)
        if browser_driver is None:
            return

        try:
            screenshot = browser_driver.get_screenshot_as_png()
            Path("screenshots").mkdir(exist_ok=True)
            filename = item.name + "_" + report.when + ".png"
            Path("screenshots", filename).write_bytes(screenshot)
            allure.attach(screenshot, name="Ошибка: " + item.name,
                          attachment_type=allure.attachment_type.PNG)
            allure.attach(browser_driver.current_url, name="Адрес страницы",
                          attachment_type=allure.attachment_type.TEXT)
        except WebDriverException as error:
            allure.attach(str(error), name="Не удалось сделать скриншот",
                          attachment_type=allure.attachment_type.TEXT)
