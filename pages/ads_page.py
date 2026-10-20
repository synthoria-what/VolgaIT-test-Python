import allure
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.base_page import BasePage


class AdsPage(BasePage):
    AD = (By.ID, "popmake-1272")
    OVERLAY = (By.ID, "pum-1272")
    CLOSE = (By.CSS_SELECTOR, "#popmake-1272 .pum-close")
    LOGO = (By.CSS_SELECTOR, "a.logo")

    def open(self):
        super().open("/ads/")
        self.find((By.TAG_NAME, "h1"))

    @allure.step("Дождаться появления рекламы")
    def wait_for_ad(self):
        return self.find(self.AD)

    @allure.step("Закрыть рекламу крестиком")
    def close_ad(self):
        self.click(self.CLOSE)
        self.wait_hidden(self.AD)

    @allure.step("Закрыть рекламу клавишей Enter на кнопке закрытия")
    def close_with_enter(self):
        self.find(self.CLOSE).send_keys(Keys.ENTER)
        self.wait_hidden(self.AD)

    @allure.step("Нажать Escape в рекламе")
    def press_escape(self):
        self.find(self.CLOSE).send_keys(Keys.ESCAPE)

    @allure.step("Нажать на затемнение вне рекламного окна")
    def click_overlay(self):
        overlay = self.find(self.OVERLAY)
        size = overlay.size
        ActionChains(self.driver).move_to_element_with_offset(
            overlay, -size["width"] // 2 + 10, -size["height"] // 2 + 10
        ).click().perform()
