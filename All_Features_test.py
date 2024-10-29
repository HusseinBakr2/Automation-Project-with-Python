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
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.maximize_window()
    login_page = LoginPage(driver)
    login_page.open("https://www.saucedemo.com/")
    yield driver
    driver.quit()

# Helper function for login using the LoginPage class
def login_user(driver, username="standard_user", password="secret_sauce"):
    login_page = LoginPage(driver)
    login_page.login(username, password)
    sleep(1)
    assert "inventory" in driver.current_url, "Login failed. User was not redirected to inventory page."

# Test Scenario 1: Add items to cart
def test_add_items_to_cart(setup_driver):
    login_user(setup_driver)
    items = setup_driver.find_elements(By.CLASS_NAME, "inventory_item")
    for item in items[:3]:  # Adding two items for this test
        item.find_element(By.CLASS_NAME, "btn_inventory").click()
    cart_badge = setup_driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
    assert cart_badge == "3", "Failed to add items to cart."
    sleep(2)
# Test Scenario 2: Add items to cart and then remove
def test_add_and_remove_items_from_cart(setup_driver):
    login_user(setup_driver)
    items_to_add = setup_driver.find_elements(By.CLASS_NAME, "inventory_item")[:3]
    for item in items_to_add:
        add_button = item.find_element(By.CLASS_NAME, "btn_inventory")
        add_button.click()
    sleep(1)
    cart_count = setup_driver.find_element(By.CLASS_NAME, "shopping_cart_badge").text
    assert cart_count == str(
        len(items_to_add)), f"Expected {len(items_to_add)} items in the cart, but found {cart_count}."

    for item in items_to_add:
        remove_button = item.find_element(By.CLASS_NAME, "btn_inventory")
        remove_button.click()

    sleep(1)
    cart_icon = setup_driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    cart_icon.click()
    cart_items = setup_driver.find_elements(By.CLASS_NAME, "cart_item")
    assert len(cart_items) == 0, "Expected cart to be empty after removal, but items are still present."

    sleep(2)

# Test Scenario 3: View Product Details
def test_view_product_details(setup_driver):
    login_user(setup_driver)
    first_item = setup_driver.find_element(By.CLASS_NAME, "inventory_item_name")
    first_item_name = first_item.text
    first_item.click()
    detail_name = setup_driver.find_element(By.CLASS_NAME, "inventory_details_name").text
    assert first_item_name == detail_name, "Product detail name does not match the item clicked."
    sleep(2)

# Test Scenario 4: Use filter successfully
def test_use_filter(setup_driver):
    login_user(setup_driver)
    filter_dropdown = setup_driver.find_element(By.CLASS_NAME, "product_sort_container")
    filter_dropdown.click()
    filter_options = setup_driver.find_elements(By.TAG_NAME, "option")
    filter_options[2].click()  # Apply a filter (e.g., Price (low to high))
    sleep(1)
    assert "inventory" in setup_driver.current_url, "Filter application failed."
    sleep(2)
        #  Sorting Items by Name (A to Z)
def test_sort_items_by_name_za(setup_driver):
    login_user(setup_driver)
    filter_dropdown = setup_driver.find_element(By.CLASS_NAME, "product_sort_container")
    filter_dropdown.click()
    filter_dropdown.find_element(By.XPATH, "//option[text()='Name (Z to A)']").click()
    items = setup_driver.find_elements(By.CLASS_NAME, "inventory_item_name")
    sorted_items = sorted((item.text for item in items), reverse=True)
    assert [item.text for item in items] == sorted_items, "Items are not sorted by Name (Z to A)."
    sleep(2)
        #Sorting Items by Price (High to Low)
def test_sort_items_by_price_high_to_low(setup_driver):
    login_user(setup_driver)
    filter_dropdown = setup_driver.find_element(By.CLASS_NAME, "product_sort_container")
    filter_dropdown.click()
    filter_dropdown.find_element(By.XPATH, "//option[text()='Price (high to low)']").click()
    prices = setup_driver.find_elements(By.CLASS_NAME, "inventory_item_price")
    sorted_prices = sorted([float(price.text[1:]) for price in prices], reverse=True)
    assert [float(price.text[1:]) for price in prices] == sorted_prices, "Items are not sorted by Price (high to low)."


# Sorting Items by Price (Low to High)
def test_sort_items_by_price_low_to_high(setup_driver):
    login_user(setup_driver)  # Make sure user is logged in
    filter_dropdown = setup_driver.find_element(By.CLASS_NAME, "product_sort_container")
    filter_dropdown.click()
    filter_dropdown.find_element(By.XPATH, "//option[text()='Price (low to high)']").click()

    items = setup_driver.find_elements(By.CLASS_NAME, "inventory_item_price")
    displayed_prices = [float(item.text.replace("$", "")) for item in items]
    sorted_prices = sorted(displayed_prices)
    assert displayed_prices == sorted_prices, "Items are not sorted by Price (Low to High)."

    sleep(2)


# Test Scenario 5: Go to cart and remove items
def test_remove_items_from_cart_in_cart_page(setup_driver):
    login_user(setup_driver)
    items = setup_driver.find_elements(By.CLASS_NAME, "inventory_item")
    for item in items[:2]:
        item.find_element(By.CLASS_NAME, "btn_inventory").click()
    setup_driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    remove_buttons = setup_driver.find_elements(By.CLASS_NAME, "cart_button")
    sleep(1)
    for remove_button in remove_buttons:
        remove_button.click()
    assert not setup_driver.find_elements(By.CLASS_NAME, "shopping_cart_badge"), "Items were not removed from cart."
    sleep(2)
# Test Scenario 6: Buy an item successfully
def test_buy_item_successfully(setup_driver):
    login_user(setup_driver)
    setup_driver.find_element(By.CLASS_NAME, "btn_inventory").click()  # Add first item
    setup_driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    setup_driver.find_element(By.CLASS_NAME, "checkout_button").click()
    sleep(1)
    # Fill checkout information
    setup_driver.find_element(By.ID, "first-name").send_keys("Test")
    setup_driver.find_element(By.ID, "last-name").send_keys("User")
    setup_driver.find_element(By.ID, "postal-code").send_keys("12345")
    setup_driver.find_element(By.ID, "continue").click()
    sleep(1)
    # Finish purchase
    setup_driver.find_element(By.ID, "finish").click()
    complete_text = setup_driver.find_element(By.CLASS_NAME, "complete-header").text
    assert complete_text == "Thank you for your order!", "Purchase process failed."
    sleep(2)


# Test Scenario 7: Log out after logging in
def test_logout(setup_driver):
    login_user(setup_driver)
    setup_driver.find_element(By.ID, "react-burger-menu-btn").click()
    sleep(1)
    setup_driver.find_element(By.ID, "logout_sidebar_link").click()
    assert "saucedemo" in setup_driver.current_url, "Logout failed. User was not redirected to login page."
    sleep(2)
# Test Scenario 8: Attempt to purchase without adding items to cart
def test_empty_cart_purchase_attempt(setup_driver):
    login_user(setup_driver)
    setup_driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    assert not setup_driver.find_elements(By.CLASS_NAME, "cart_item"), "Cart is not empty, but should be."

    try:
        checkout_button = setup_driver.find_element(By.ID, "checkout")
        checkout_button.click()

        # If able to proceed, we attempt to fill in checkout details
        setup_driver.find_element(By.ID, "first-name").send_keys("Test")
        setup_driver.find_element(By.ID, "last-name").send_keys("User")
        setup_driver.find_element(By.ID, "postal-code").send_keys("12345")
        setup_driver.find_element(By.ID, "continue").click()

        # This step should not succeed; if it does, we have an issue.
        setup_driver.find_element(By.ID, "finish").click()
        complete_text = setup_driver.find_element(By.CLASS_NAME, "complete-header").text
        assert complete_text != "Thank you for your order!", "Unexpectedly completed a purchase with an empty cart."

    except:
        print("Checkout is not allowed with an empty cart as expected.")

    sleep(2)






