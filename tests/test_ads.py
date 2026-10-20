import allure
import pytest
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.ads_page import AdsPage


@pytest.fixture
def ads(driver):
    page = AdsPage(driver)
    page.open()
    return page


@pytest.mark.positive
@allure.title("ADS-P01: реклама появляется автоматически и содержит текст")
def test_ad_appears_automatically(ads):
    ad = ads.wait_for_ad()
    assert "Hi" in ad.text
    assert "I am an ad." in ad.text


@pytest.mark.positive
@allure.title("ADS-P02: реклама закрывается крестиком")
def test_close_ad(ads):
    ads.wait_for_ad()
    ads.close_ad()
    assert not ads.driver.find_element(*ads.AD).is_displayed()


@pytest.mark.positive
@allure.title("ADS-P03: кнопка закрытия работает с клавиатуры")
def test_close_ad_with_enter(ads):
    ads.wait_for_ad()
    ads.close_with_enter()
    assert not ads.driver.find_element(*ads.AD).is_displayed()


@pytest.mark.positive
@allure.title("ADS-P04: после обновления страницы реклама появляется снова")
def test_ad_appears_after_refresh(ads):
    ads.wait_for_ad()
    ads.close_ad()
    with allure.step("Обновить страницу"):
        ads.driver.refresh()
    assert ads.wait_for_ad().is_displayed()


@pytest.mark.positive
@allure.title("ADS-P05: после закрытия рекламы доступен переход по логотипу")
def test_page_works_after_closing_ad(ads):
    ads.wait_for_ad()
    ads.close_ad()
    with allure.step("Нажать логотип и перейти на главную"):
        ads.click(ads.LOGO)
        ads.wait.until(EC.url_to_be(ads.BASE_URL + "/"))
    assert ads.driver.current_url == ads.BASE_URL + "/"


@pytest.mark.positive
@allure.title("ADS-P06: реклама видна и закрывается в узком окне")
def test_ad_in_narrow_window(ads):
    with allure.step("Установить размер окна 600 на 900"):
        ads.driver.set_window_size(600, 900)
    ads.wait_for_ad()
    close = ads.find(ads.CLOSE)
    viewport_width = ads.driver.execute_script("return window.innerWidth")
    assert close.rect["x"] >= 0
    assert close.rect["x"] + close.rect["width"] <= viewport_width
    ads.close_ad()


@pytest.mark.positive
@allure.title("ADS-P07: закрытая реклама не появляется повторно в течение 6 секунд")
def test_closed_ad_does_not_reappear(ads):
    ads.wait_for_ad()
    ads.close_ad()
    with allure.step("Наблюдать за закрытой рекламой 6 секунд"):
        with pytest.raises(TimeoutException):
            WebDriverWait(ads.driver, 6).until(EC.visibility_of_element_located(ads.AD))
    assert not ads.driver.find_element(*ads.AD).is_displayed()


@pytest.mark.negative
@allure.title("ADS-N01: Escape не закрывает рекламу")
def test_escape_does_not_close_ad(ads):
    ads.wait_for_ad()
    ads.press_escape()
    assert ads.find(ads.AD).is_displayed()


@pytest.mark.negative
@allure.title("ADS-N02: клик по затемнению не закрывает рекламу")
def test_overlay_does_not_close_ad(ads):
    ads.wait_for_ad()
    ads.click_overlay()
    assert ads.find(ads.AD).is_displayed()


@pytest.mark.negative
@allure.title("ADS-N03: реклама блокирует нажатие на логотип за окном")
def test_ad_blocks_background_click(ads):
    ads.wait_for_ad()
    logo = ads.driver.find_element(*ads.LOGO)
    with allure.step("Проверить, что затемнение перехватывает клик по логотипу"):
        with pytest.raises(ElementClickInterceptedException):
            logo.click()
    assert ads.driver.current_url == ads.BASE_URL + "/ads/"
    assert ads.find(ads.AD).is_displayed()
