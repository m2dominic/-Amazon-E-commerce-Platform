# src/pages/login_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from .base_page import BasePage
from .home_page import HomePage


class LoginPage(BasePage):
    """Amazon Login Page Object Model"""
    
    # Page Element Locators
    EMAIL_FIELD = (By.ID, "ap_email")
    CONTINUE_BUTTON = (By.ID, "continue")
    PASSWORD_FIELD = (By.ID, "ap_password")
    SIGN_IN_BUTTON = (By.ID, "signInSubmit")
    ERROR_MESSAGE = (By.XPATH, "//div[@id='auth-error-message-box']")
    SIGN_IN_HEADER = (By.XPATH, "//h1[text()='Sign in']")
    
    def __init__(self, driver):
        """Initialize LoginPage with WebDriver instance"""
        super().__init__(driver)
    
    # Page Actions
    def enter_email(self, email):
        """
        Enter email address in the email field
        
        Args:
            email (str): Email address to enter
        """
        self.enter_text(self.EMAIL_FIELD, email)
    
    def click_continue(self):
        """Click the continue button after entering email"""
        self.click_element(self.CONTINUE_BUTTON)
    
    def enter_password(self, password):
        """
        Enter password in the password field
        
        Args:
            password (str): Password to enter
        """
        self.enter_text(self.PASSWORD_FIELD, password)
    
    def click_sign_in(self):
        """
        Click the sign in button and return HomePage instance
        
        Returns:
            HomePage: Instance of the home page after successful login
        """
        self.click_element(self.SIGN_IN_BUTTON)
        return HomePage(self.driver)
    
    def login_with_credentials(self, email, password):
        """
        Complete login flow with email and password
        
        Args:
            email (str): Email address for login
            password (str): Password for login
            
        Returns:
            HomePage: Instance of home page after login attempt
        """
        self.enter_email(email)
        self.click_continue()
        self.enter_password(password)
        return self.click_sign_in()
    
    def get_error_message(self):
        """
        Get the error message text if displayed
        
        Returns:
            str: Error message text, empty string if not found
        """
        try:
            return self.get_text(self.ERROR_MESSAGE)
        except (TimeoutException, NoSuchElementException):
            return ""
    
    def is_error_message_displayed(self):
        """
        Check if error message is displayed on the page
        
        Returns:
            bool: True if error message is visible, False otherwise
        """
        return self.is_element_displayed(self.ERROR_MESSAGE)
    
    def is_page_displayed(self):
        """
        Implementation of abstract method from BasePage
        Verify that the login page is properly displayed
        
        Returns:
            bool: True if page is displayed correctly, False otherwise
        """
        return (self.is_element_displayed(self.SIGN_IN_HEADER) and 
                self.is_element_displayed(self.EMAIL_FIELD))
    
    # Additional utility methods for enhanced functionality
    def wait_for_password_field(self, timeout=10):
        """
        Wait for password field to appear (after clicking continue)
        
        Args:
            timeout (int): Maximum time to wait in seconds
            
        Returns:
            bool: True if password field appears, False if timeout
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(self.PASSWORD_FIELD)
            )
            return True
        except TimeoutException:
            return False
    
    def is_email_step_displayed(self):
        """
        Check if we're on the email input step
        
        Returns:
            bool: True if email field is visible and continue button is present
        """
        return (self.is_element_displayed(self.EMAIL_FIELD) and 
                self.is_element_displayed(self.CONTINUE_BUTTON))
    
    def is_password_step_displayed(self):
        """
        Check if we're on the password input step
        
        Returns:
            bool: True if password field is visible and sign in button is present
        """
        return (self.is_element_displayed(self.PASSWORD_FIELD) and 
                self.is_element_displayed(self.SIGN_IN_BUTTON))


# Alternative implementation with properties for direct element access
class LoginPageWithProperties(BasePage):
    """Alternative implementation using properties for element access"""
    
    def __init__(self, driver):
        super().__init__(driver)
    
    # Properties for lazy element loading
    @property
    def email_field(self):
        return self.find_element((By.ID, "ap_email"))
    
    @property
    def continue_button(self):
        return self.find_element((By.ID, "continue"))
    
    @property
    def password_field(self):
        return self.find_element((By.ID, "ap_password"))
    
    @property
    def sign_in_button(self):
        return self.find_element((By.ID, "signInSubmit"))
    
    @property
    def error_message(self):
        return self.find_element((By.XPATH, "//div[@id='auth-error-message-box']"))
    
    @property
    def sign_in_header(self):
        return self.find_element((By.XPATH, "//h1[text()='Sign in']"))
    
    # Page Actions using properties
    def enter_email(self, email):
        self.email_field.clear()
        self.email_field.send_keys(email)
    
    def click_continue(self):
        self.continue_button.click()
    
    def enter_password(self, password):
        self.password_field.clear()
        self.password_field.send_keys(password)
    
    def click_sign_in(self):
        self.sign_in_button.click()
        return HomePage(self.driver)
    
    def login_with_credentials(self, email, password):
        self.enter_email(email)
        self.click_continue()
        # Wait for password field to load
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "ap_password"))
        )
        self.enter_password(password)
        return self.click_sign_in()
    
    def get_error_message(self):
        try:
            return self.error_message.text
        except:
            return ""
    
    def is_error_message_displayed(self):
        try:
            return self.error_message.is_displayed()
        except:
            return False
    
    def is_page_displayed(self):
        try:
            return (self.sign_in_header.is_displayed() and 
                    self.email_field.is_displayed())
        except:
            return False
