import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class LogIn(unittest.TestCase):
    def setUp(self):
        # Create a new Chrome session
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(20)
        self.driver.maximize_window()

        # Navigate to ExcelChat's page
        self.driver.get("https://www.got-it.ai/solutions/excel-chat/")

        # Click log in button to open log in form
        test_login_button = self.driver.find_element_by_id("test-login-button")
        test_login_button.click()
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.ID, "modal-login")))

    def getElements(self):
        """
        A helper method to return web elements used in all test cases
        :return: email, password, login-button web elements
        """
        email = self.driver.find_element_by_name("email")
        password = self.driver.find_element_by_name("password")
        login_button = self.driver.find_element_by_id("login-button")
        return email, password, login_button

    def not_logged_in(self, message):
        """
        A helper method for unsuccessful login attempts
        :param message: expected alert message
        :return: 1 if expected alert message appears, raises TimeoutException otherwise
        """
        alert_xpath = "//*[@id='modal-login']/div/div/div[2]/div/div[1]"
        return WebDriverWait(self.driver, 20).until(EC.text_to_be_present_in_element((By.XPATH, alert_xpath), message))

    def test_no_email_no_password(self):
        email, password, login_button = self.getElements()
        login_button.click()
        assert self.not_logged_in("Please enter email address.")

    def test_no_email_with_password(self):
        email, password, login_button = self.getElements()
        login_button.send_keys("123")
        login_button.click()
        assert self.not_logged_in("Please enter email address.")

    def test_invalid_email_no_password(self):
        email, password, login_button = self.getElements()
        email.send_keys("123")
        login_button.click()
        assert self.not_logged_in("You have entered an invalid email address. Please try again.")

    def test_invalid_email_with_password(self):
        email, password, login_button = self.getElements()
        email.send_keys("123@")
        password.send_keys("123")
        login_button.click()
        assert self.not_logged_in("You have entered an invalid email address. Please try again.")

    def test_valid_email_no_password(self):
        email, password, login_button = self.getElements()
        email.send_keys("tran_k1@denison.edu")
        login_button.click()
        assert self.not_logged_in("Please enter password.")

    def test_valid_unregistered_email_with_password(self):
        email, password, login_button = self.getElements()
        email.send_keys("tran_k1@denison.edu")
        password.send_keys("123")
        login_button.click()
        assert self.not_logged_in("The account you've entered doesn't exist.")

    def test_valid_registered_email_with_wrong_password(self):
        email, password, login_button = self.getElements()
        email.send_keys("hakhanhtran99@gmail.com")
        password.send_keys("got1ta!")
        login_button.click()
        assert self.not_logged_in("Invalid email or password.")

    def test_valid_registered_email_with_right_password(self):
        """
        Successful log in attempt
        Expected result: land on homepage
        """
        email, password, login_button = self.getElements()
        email.send_keys("hakhanhtran99@gmail.com")
        password.send_keys("got1tA!")
        login_button.click()
        assert WebDriverWait(self.driver, 20).until(EC.url_to_be("https://www.got-it.ai/solutions/excel-chat/home"))

    def test_forgot_password(self):
        """
        Click forgot password
        Expected result: password recovery form pops up
        """
        forgot_password = self.driver.find_element_by_link_text("Forgot Your Password?")
        forgot_password.click()
        assert WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.ID, "modal-password-recovery")))

    def test_sign_up(self):
        """
        Click forgot password
        Expected result: sign up form pops up
        """
        sign_up = self.driver.find_element_by_link_text("Sign up")
        sign_up.click()
        assert WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.ID, "modal-signup")))

    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main(verbosity=2)
