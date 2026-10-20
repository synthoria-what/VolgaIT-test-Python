import allure
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    BASE_URL = "https://practice-automation.com"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    @allure.step("Открыть страницу {path}")
    def open(self, path):
        self.driver.get(self.BASE_URL + path)

    def find(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def wait_hidden(self, locator):
        self.wait.until(EC.invisibility_of_element_located(locator))
