# src/tests/base_test.py
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from utils.config_manager import ConfigManager
from utils.driver_manager import DriverManager
from utils.test_data_manager import TestDataManager
from pages.home_page import HomePage


class BaseTest:
    """Base test class providing common setup and teardown functionality"""
    
    # Class-level attributes
    config_manager = None
    test_data_manager = None
    
    @classmethod
    def setup_class(cls):
        """
        Set up class-level resources (equivalent to @BeforeClass in TestNG)
        Called once before all test methods in the class
        """
        cls.config_manager = ConfigManager.get_instance()
        cls.test_data_manager = TestDataManager.get_instance()
    
    def setup_method(self, method):
        """
        Set up method-level resources (equivalent to @BeforeMethod in TestNG)
        Called before each test method
        
        Args:
            method: The test method that's about to be executed
        """
        browser = self.config_manager.get_browser()
        DriverManager.set_driver(browser)
        
        self.driver = DriverManager.get_driver()
        self.driver.get(self.config_manager.get_base_url())
        
        self.home_page = HomePage(self.driver)
    
    def teardown_method(self, method):
        """
        Clean up method-level resources (equivalent to @AfterMethod in TestNG)
        Called after each test method
        
        Args:
            method: The test method that was just executed
        """
        DriverManager.quit_driver()
    
    @classmethod
    def teardown_class(cls):
        """
        Clean up class-level resources (equivalent to @AfterClass in TestNG)
        Called once after all test methods in the class
        """
        # Add any class-level cleanup if needed
        pass


# Alternative implementation using pytest fixtures
@pytest.fixture(scope="session")
def config_manager():
    """Session-scoped fixture for ConfigManager"""
    return ConfigManager.get_instance()


@pytest.fixture(scope="session")
def test_data_manager():
    """Session-scoped fixture for TestDataManager"""
    return TestDataManager.get_instance()


@pytest.fixture(scope="function")
def driver_setup(config_manager):
    """Function-scoped fixture for WebDriver setup and teardown"""
    browser = config_manager.get_browser()
    DriverManager.set_driver(browser)
    
    driver = DriverManager.get_driver()
    driver.get(config_manager.get_base_url())
    
    yield driver
    
    DriverManager.quit_driver()


@pytest.fixture(scope="function")
def home_page(driver_setup):
    """Function-scoped fixture for HomePage instance"""
    return HomePage(driver_setup)


# Alternative BaseTest class using fixtures
class BaseTestWithFixtures:
    """Alternative base test implementation using pytest fixtures"""
    
    def test_setup(self, driver_setup, config_manager, test_data_manager, home_page):
        """
        Setup method that uses fixtures
        This method should be called by test methods that need these resources
        """
        self.driver = driver_setup
        self.config_manager = config_manager
        self.test_data_manager = test_data_manager
        self.home_page = home_page


# Enhanced BaseTest with additional utilities
class EnhancedBaseTest(BaseTest):
    """Enhanced base test class with additional utility methods"""
    
    def setup_method(self, method):
        """Enhanced setup with additional configuration options"""
        super().setup_method(method)
        
        # Set implicit wait
        implicit_wait = self.config_manager.get_implicit_wait()
        self.driver.implicitly_wait(implicit_wait)
        
        # Set window size if configured
        window_size = self.config_manager.get_window_size()
        if window_size:
            self.driver.set_window_size(*window_size)
        elif self.config_manager.is_maximized():
            self.driver.maximize_window()
    
    def take_screenshot(self, test_name=None):
        """
        Take a screenshot for debugging purposes
        
        Args:
            test_name (str): Name of the test for screenshot filename
            
        Returns:
            str: Path to the saved screenshot
        """
        import os
        from datetime import datetime
        
        if not test_name:
            test_name = "screenshot"
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_dir = "screenshots"
        
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
        
        screenshot_path = f"{screenshot_dir}/{test_name}_{timestamp}.png"
        self.driver.save_screenshot(screenshot_path)
        return screenshot_path
    
    def wait_for_page_load(self, timeout=30):
        """
        Wait for page to fully load
        
        Args:
            timeout (int): Maximum time to wait in seconds
        """
        from selenium.webdriver.support.ui import WebDriverWait
        
        WebDriverWait(self.driver, timeout).until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
    
    def get_current_url(self):
        """Get the current URL of the page"""
        return self.driver.current_url
    
    def get_page_title(self):
        """Get the title of the current page"""
        return self.driver.title
    
    def teardown_method(self, method):
        """Enhanced teardown with screenshot on failure"""
        # Take screenshot if test failed
        if hasattr(self, '_outcome') and self._outcome.errors:
            test_name = method.__name__
            screenshot_path = self.take_screenshot(f"failed_{test_name}")
            print(f"Test failed. Screenshot saved: {screenshot_path}")
        
        super().teardown_method(method)


# Pytest configuration for parallel execution and reporting
def pytest_configure(config):
    """Pytest configuration hook"""
    # Add custom markers
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )


# Pytest hooks for enhanced reporting
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test outcomes for screenshot functionality"""
    if call.when == "call":
        # Store the outcome in the test instance if it's a BaseTest
        if hasattr(item.instance, 'teardown_method'):
            item.instance._outcome = call


# Example usage in conftest.py
# This would typically go in a conftest.py file
pytest_plugins = [
    "pytest_html",  # For HTML reports
    "pytest_xdist",  # For parallel execution
]


# Command line options (would go in conftest.py)
def pytest_addoption(parser):
    """Add custom command line options"""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests on: chrome, firefox, edge"
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run tests in headless mode"
    )
    parser.addoption(
        "--env",
        action="store",
        default="qa",
        help="Environment to run tests against: dev, qa, staging, prod"
    )
