# src/pages/home_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
from .search_results_page import SearchResultsPage
from .login_page import LoginPage
from .cart_page import CartPage


class HomePage(BasePage):
    """Amazon Home Page Object Model"""
    
    # Page Element Locators
    SEARCH_BOX = (By.ID, "twotabsearchtextbox")
    SEARCH_BUTTON = (By.ID, "nav-search-submit-button")
    ACCOUNT_LIST_LINK = (By.ID, "nav-link-accountList")
    CART_ICON = (By.ID, "nav-cart")
    AMAZON_LOGO = (By.ID, "nav-logo-sprites")
    SIGN_IN_TEXT = (By.XPATH, "//span[text()='Hello, sign in']")
    
    def __init__(self, driver):
        """Initialize HomePage with WebDriver instance"""
        super().__init__(driver)
    
    # Page Actions
    def search_for_product(self, product_name):
        """
        Search for a product using the search box
        
        Args:
            product_name (str): Name of the product to search for
            
        Returns:
            SearchResultsPage: Instance of search results page
        """
        self.enter_text(self.SEARCH_BOX, product_name)
        self.click_element(self.SEARCH_BUTTON)
        return SearchResultsPage(self.driver)
    
    def click_sign_in(self):
        """
        Click on the sign in link
        
        Returns:
            LoginPage: Instance of login page
        """
        self.click_element(self.ACCOUNT_LIST_LINK)
        return LoginPage(self.driver)
    
    def click_cart(self):
        """
        Click on the cart icon
        
        Returns:
            CartPage: Instance of cart page
        """
        self.click_element(self.CART_ICON)
        return CartPage(self.driver)
    
    def get_search_box_placeholder(self):
        """
        Get the placeholder text from the search box
        
        Returns:
            str: Placeholder text
        """
        search_element = self.find_element(self.SEARCH_BOX)
        return search_element.get_attribute("placeholder")
    
    def is_user_signed_in(self):
        """
        Check if user is currently signed in
        
        Returns:
            bool: True if user is signed in, False otherwise
        """
        sign_in_text = self.get_text(self.SIGN_IN_TEXT)
        return "sign in" not in sign_in_text.lower()
    
    def is_page_displayed(self):
        """
        Implementation of abstract method from BasePage
        Verify that the home page is properly displayed
        
        Returns:
            bool: True if page is displayed correctly, False otherwise
        """
        return (self.is_element_displayed(self.AMAZON_LOGO) and 
                self.is_element_displayed(self.SEARCH_BOX))


# Alternative implementation with properties for lazy element loading
class HomePageWithProperties(BasePage):
    """Alternative implementation using properties for element access"""
    
    def __init__(self, driver):
        super().__init__(driver)
    
    # Properties for lazy element loading
    @property
    def search_box(self):
        return self.find_element((By.ID, "twotabsearchtextbox"))
    
    @property
    def search_button(self):
        return self.find_element((By.ID, "nav-search-submit-button"))
    
    @property
    def account_list_link(self):
        return self.find_element((By.ID, "nav-link-accountList"))
    
    @property
    def cart_icon(self):
        return self.find_element((By.ID, "nav-cart"))
    
    @property
    def amazon_logo(self):
        return self.find_element((By.ID, "nav-logo-sprites"))
    
    @property
    def sign_in_text(self):
        return self.find_element((By.XPATH, "//span[text()='Hello, sign in']"))
    
    # Page Actions using properties
    def search_for_product(self, product_name):
        self.search_box.clear()
        self.search_box.send_keys(product_name)
        self.search_button.click()
        return SearchResultsPage(self.driver)
    
    def click_sign_in(self):
        self.account_list_link.click()
        return LoginPage(self.driver)
    
    def click_cart(self):
        self.cart_icon.click()
        return CartPage(self.driver)
    
    def get_search_box_placeholder(self):
        return self.search_box.get_attribute("placeholder")
    
    def is_user_signed_in(self):
        return "sign in" not in self.sign_in_text.text.lower()
    
    def is_page_displayed(self):
        try:
            return self.amazon_logo.is_displayed() and self.search_box.is_displayed()
        except:
            return False
