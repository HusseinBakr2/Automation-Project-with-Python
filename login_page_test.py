from selenium.webdriver.common.by import By

class LoginPage:
    def __init__(self, driver):
        self.driver = driver

    def open(self, url):
        self.driver.get(url)

    def set_username(self, username):
        self.driver.find_element(By.ID, "user-name").clear()
        self.driver.find_element(By.ID, "user-name").send_keys(username)

    def set_password(self, password):
        self.driver.find_element(By.ID, "password").clear()
        self.driver.find_element(By.ID, "password").send_keys(password)

    def submit(self):
        self.driver.find_element(By.ID, "login-button").click()

    def login(self, username, password):
        self.set_username(username)
        self.set_password(password)
        self.submit()

    def logout(self):
        logout_button = self.driver.find_element(By.ID, "logout_sidebar_link")  # Adjust ID if needed
        logout_button.click()
