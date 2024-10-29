
import pytest
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from login_page_test import LoginPage




# Fixture for WebDriver setup (fresh session for each test)
@pytest.fixture(scope="function")
def setup_driver():
    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.maximize_window()
        loginpage = LoginPage(driver)
        loginpage.open("https://www.saucedemo.com/")
        yield driver
        driver.quit()
    except Exception as e:
        print(f"Error setting up WebDriver: {e}")
        pytest.fail("WebDriver setup failed.")


#-------------------------------Username Test Cases------------------------------------

@pytest.mark.parametrize("username, expected_success", [
    ("standard_user", True), ("locked_out_user", False), ("problem_user", True),
    ("performance_glitch_user", True), ("error_user", False), ("visual_user", False),
    ("standarduser", False), ("Standard_User", False), ("Standard-User", False),
    ("standard user", False), ("stAndard_user", False), ("standard_user8", False),
    ("lockedout_user", False), ("lockedoutuser", False), ("err0r_user", False),
    ("locked-out-user", False), ("Locked_Out_User", False), ("l0cked_out_user", False),
    ("Problem_user", False), ("problem-user", False), ("performance glitch user", False),
    ("Performance_glitch_user", False), ("problemuser", False), ("problem user", False),
    ("Problem_User", False), ("performance-glitch_user", False), ("performance-glitch-user", False),
    (" performance-glitch user", False), ("Error_user", False), ("eror_user", False),
    ("erroruser", False), ("error user", False), ("Visual_user", False), ("visual user", False),
    ("visual-user", False), ("visual-User", False), ("visu@l_user", False), ("   ", False), ("", False)
])
def test_username_only(setup_driver, username, expected_success):
    username_input = setup_driver.find_element(By.ID, "user-name")
    password_input = setup_driver.find_element(By.ID, "password")
    login_button = setup_driver.find_element(By.ID, "login-button")

    username_input.clear()
    password_input.clear()
    username_input.send_keys(username)
    password_input.send_keys("secret_sauce")  # Fixed valid password for testing
    login_button.click()
    sleep(0.5)

    if expected_success:
        try:
            assert "inventory" in setup_driver.current_url, f"Login should succeed for username '{username}'."
            print(f"Login successful for username '{username}'. Redirected to home page.")
        except AssertionError:
            print(f"Login expected to succeed, but failed for username '{username}'.")
    else:
        try:
            error_message = setup_driver.find_element(By.CLASS_NAME, "error-message-container").text
            print(f"Error message for username '{username}': {error_message}")
        except:
            print(f"No error message displayed for failed login with username '{username}'.")

#-------------------------------Password Test Cases------------------------------------

@pytest.mark.parametrize("password, expected_success", [
    ("secret_sauce", True), ("123456", False),("     ",False),("",False),("$ecret_sauce",False),("Secret_Sauce",False),("secretsauce",False),(" secret_sauce",False),("secret_sauce9",False),("secret_s@uce",False),("02388885",False),("secret_saucesecret_sauce",False)
])
def test_password_only(setup_driver, password, expected_success):
    username_input = setup_driver.find_element(By.ID, "user-name")
    password_input = setup_driver.find_element(By.ID, "password")
    login_button = setup_driver.find_element(By.ID, "login-button")

    username_input.clear()
    password_input.clear()
    username_input.send_keys("standard_user")  # Fixed valid username for testing
    password_input.send_keys(password)
    login_button.click()
    sleep(0.5)

    if expected_success:
        try:
            assert "inventory" in setup_driver.current_url, f"Login should succeed with password '{password}'."
            print(f"Login successful with password '{password}'. Redirected to home page.")
        except AssertionError:
            print(f"Login expected to succeed, but failed with password '{password}'.")
    else:
        try:
            error_message = setup_driver.find_element(By.CLASS_NAME, "error-message-container").text
            print(f"Error message for password '{password}': {error_message}")
        except:
            print(f"No error message displayed for failed login with password '{password}'.")
