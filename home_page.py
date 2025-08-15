# src/tests/test_home_page.py
import pytest
from pages.search_results_page import SearchResultsPage
from pages.login_page import LoginPage
from .base_test import BaseTest


class TestHomePage(BaseTest):
    """Test cases for Amazon Home Page functionality"""
    
    @pytest.mark.smoke
    @pytest.mark.order(1)
    def test_home_page_load(self):
        """Test that the home page loads and displays properly"""
        assert self.home_page.is_page_displayed(), "Home page is not displayed properly"
    
    @pytest.mark.smoke
    @pytest.mark.order(2)
    def test_search_functionality(self):
        """Test the search functionality on home page"""
        search_term = self.test_data_manager.get_search_keyword(0)
        search_page = self.home_page.search_for_product(search_term)
        
        assert search_page.is_page_displayed(), "Search results page not displayed"
        assert isinstance(search_page, SearchResultsPage), "Expected SearchResultsPage instance"
    
    @pytest.mark.regression
    @pytest.mark.order(3)
    def test_navigate_to_login(self):
        """Test navigation to login page from home page"""
        login_page = self.home_page.click_sign_in()
        
        assert login_page.is_page_displayed(), "Login page not displayed"
        assert isinstance(login_page, LoginPage), "Expected LoginPage instance"


# Alternative implementation using pytest fixtures instead of inheritance
class TestHomePageWithFixtures:
    """Alternative test class using pytest fixtures"""
    
    @pytest.mark.smoke
    def test_home_page_load(self, home_page):
        """Test that the home page loads and displays properly"""
        assert home_page.is_page_displayed(), "Home page is not displayed properly"
    
    @pytest.mark.smoke
    def test_search_functionality(self, home_page, test_data_manager):
        """Test the search functionality on home page"""
        search_term = test_data_manager.get_search_keyword(0)
        search_page = home_page.search_for_product(search_term)
        
        assert search_page.is_page_displayed(), "Search results page not displayed"
        assert isinstance(search_page, SearchResultsPage), "Expected SearchResultsPage instance"
    
    @pytest.mark.regression
    def test_navigate_to_login(self, home_page):
        """Test navigation to login page from home page"""
        login_page = home_page.click_sign_in()
        
        assert login_page.is_page_displayed(), "Login page not displayed"
        assert isinstance(login_page, LoginPage), "Expected LoginPage instance"


# Enhanced test class with additional validations and data-driven tests
class TestHomePageEnhanced(BaseTest):
    """Enhanced test cases with additional functionality"""
    
    @pytest.mark.smoke
    @pytest.mark.parametrize("expected_element", [
        "search_box", "amazon_logo", "cart_icon", "account_list_link"
    ])
    def test_home_page_elements_displayed(self, expected_element):
        """
        Test that individual home page elements are displayed
        
        Args:
            expected_element (str): The element to check for display
        """
        element_locator = getattr(self.home_page, expected_element.upper())
        assert self.home_page.is_element_displayed(element_locator), \
            f"{expected_element} is not displayed on home page"
    
    @pytest.mark.regression
    @pytest.mark.parametrize("search_index", [0, 1, 2])
    def test_search_with_multiple_terms(self, search_index):
        """
        Test search functionality with multiple search terms
        
        Args:
            search_index (int): Index of search term to use
        """
        search_term = self.test_data_manager.get_search_keyword(search_index)
        search_page = self.home_page.search_for_product(search_term)
        
        assert search_page.is_page_displayed(), \
            f"Search results page not displayed for term: {search_term}"
        
        # Additional validation - check if search term appears in results
        current_url = self.get_current_url()
        assert search_term.replace(" ", "+") in current_url or \
               search_term.replace(" ", "%20") in current_url, \
            f"Search term '{search_term}' not found in URL: {current_url}"
    
    @pytest.mark.smoke
    def test_search_box_placeholder(self):
        """Test that search box has appropriate placeholder text"""
        placeholder_text = self.home_page.get_search_box_placeholder()
        
        assert placeholder_text is not None, "Search box placeholder is None"
        assert len(placeholder_text) > 0, "Search box placeholder is empty"
        # Common Amazon search placeholders
        expected_phrases = ["Search Amazon", "search", "What are you looking for"]
        assert any(phrase.lower() in placeholder_text.lower() for phrase in expected_phrases), \
            f"Unexpected placeholder text: {placeholder_text}"
    
    @pytest.mark.regression
    def test_user_sign_in_status(self):
        """Test checking user sign-in status"""
        # Should initially be signed out
        assert not self.home_page.is_user_signed_in(), \
            "User appears to be signed in when they should be signed out"
    
    @pytest.mark.smoke
    def test_page_title(self):
        """Test that page title is correct"""
        page_title = self.get_page_title()
        expected_title_keywords = ["Amazon", "Online Shopping"]
        
        assert any(keyword in page_title for keyword in expected_title_keywords), \
            f"Page title doesn't contain expected keywords. Actual title: {page_title}"
    
    @pytest.mark.regression
    def test_cart_navigation(self):
        """Test navigation to cart page"""
        from pages.cart_page import CartPage
        
        cart_page = self.home_page.click_cart()
        
        assert cart_page.is_page_displayed(), "Cart page not displayed"
        assert isinstance(cart_page, CartPage), "Expected CartPage instance"
    
    @pytest.mark.slow
    def test_search_with_empty_string(self):
        """Test search functionality with empty search term"""
        # This test might behave differently depending on Amazon's implementation
        search_page = self.home_page.search_for_product("")
        
        # Amazon might redirect to a different page or show an error
        # Adjust assertion based on expected behavior
        current_url = self.get_current_url()
        assert "amazon" in current_url.lower(), \
            "Should stay on Amazon domain even with empty search"
    
    @pytest.mark.regression
    def test_multiple_page_interactions(self):
        """Test multiple interactions on home page"""
        # Test search box interaction
        search_term = self.test_data_manager.get_search_keyword(0)
        
        # Verify we can interact with search box
        self.home_page.enter_text(self.home_page.SEARCH_BOX, search_term)
        
        # Clear and try different term
        search_element = self.home_page.find_element(self.home_page.SEARCH_BOX)
        search_element.clear()
        
        # Search with different term
        different_term = self.test_data_manager.get_search_keyword(1)
        search_page = self.home_page.search_for_product(different_term)
        
        assert search_page.is_page_displayed(), \
            "Search results page not displayed after multiple interactions"


# Test class with custom fixtures and setup
class TestHomePageWithCustomSetup:
    """Test class demonstrating custom setup and fixtures"""
    
    @pytest.fixture(autouse=True)
    def setup_test_data(self, test_data_manager):
        """Auto-use fixture to set up test data for each test"""
        self.search_keywords = [
            test_data_manager.get_search_keyword(i) for i in range(3)
        ]
    
    def test_home_page_with_custom_setup(self, home_page):
        """Test using custom setup fixture"""
        assert home_page.is_page_displayed(), "Home page not displayed"
        
        # Use the search keywords set up in fixture
        for keyword in self.search_keywords[:1]:  # Test with first keyword
            search_page = home_page.search_for_product(keyword)
            assert search_page.is_page_displayed(), \
                f"Search failed for keyword: {keyword}"
            break  # Only test one to avoid multiple page navigations


# Pytest markers and configuration for this test file
pytestmark = [
    pytest.mark.homepage,  # Custom marker for all tests in this file
    pytest.mark.usefixtures("driver_setup")  # Ensure driver setup for all tests
]


# Custom pytest fixtures specific to home page tests
@pytest.fixture(scope="function")
def search_terms(test_data_manager):
    """Fixture providing multiple search terms for testing"""
    return [
        test_data_manager.get_search_keyword(i) for i in range(5)
    ]


@pytest.fixture(scope="function") 
def logged_out_home_page(home_page):
    """Fixture ensuring we start with a logged-out home page"""
    # Add any logout logic here if needed
    # For now, just return the home page
    return home_page
