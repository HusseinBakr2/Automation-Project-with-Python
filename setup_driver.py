import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from login_page_test import LoginPage  # Importing LoginPage

@pytest.fixture(scope="function")
def setup_driver():
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()
    login_page = LoginPage(driver)
    login_page.open("https://www.saucedemo.com/")
    yield driver
    driver.quit()
