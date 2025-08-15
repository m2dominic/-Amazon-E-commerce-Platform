# src/pages/base_page.py
"""
Base page class that contains common functionality for all pages
Enhanced with decorators for better error handling and logging
"""
import time
import functools
from abc import ABC, abstractmethod
from typing import List, Optional, Callable, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from src.constants.framework_constants import FrameworkConstants
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Decorator Functions
def retry_on_exception(max_retries: int = 3, exceptions: tuple = (StaleElementReferenceException,)):
    """
    Decorator to retry function execution on specific exceptions
    
    Args:
        max_retries: Maximum number of retries
        exceptions: Tuple of exceptions to catch and retry
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries:
                        logger.error(f"Function {func.__name__} failed after {max_retries} retries: {e}")
                        raise
                    logger.warning(f"Attempt {attempt + 1} failed for {func.__name__}: {e}. Retrying...")
                    time.sleep(1)
            return None
        return wrapper
    return decorator


def log_action(func: Callable) -> Callable:
    """
    Decorator to log method execution
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        logger.info(f"Executing: {func.__name__}")
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.info(f"Completed: {func.__name__} in {execution_time:.2f}s")
            return result
        except Exception as e:
            execution_time = time.time() - start_time
            logger.error(f"Failed: {func.__name__} after {execution_time:.2f}s - Error: {e}")
            raise
    return wrapper


def handle_exceptions(default_return: Any = None):
    """
    Decorator to handle exceptions gracefully
    
    Args:
        default_return: Value to return if exception occurs
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Exception in {func.__name__}: {e}")
                return default_return
        return wrapper
    return decorator


def wait_for_element(timeout: int = 10):
    """
    Decorator to wait for element before performing action
    
    Args:
        timeout: Wait timeout in seconds
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(self, locator: tuple, *args, **kwargs) -> Any:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.presence_of_element_located(locator))
            return func(self, locator, *args, **kwargs)
        return wrapper
    return decorator


class BasePage(ABC):
    """Base class for all page objects with decorator enhancements"""
    
    def __init__(self, driver: webdriver.Remote):
        """
        Initialize BasePage
        
        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, FrameworkConstants.EXPLICIT_WAIT_TIMEOUT)
        self.actions = ActionChains(driver)
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @log_action
    @retry_on_exception(max_retries=3)
    def click_element(self, locator: tuple) -> None:
        """
        Click on an element after waiting for it to be clickable
        
        Args:
            locator: Tuple containing locator strategy and value
        """
        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            # Scroll to element if needed
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            element.click()
            self.logger.info(f"Successfully clicked element: {locator}")
        except TimeoutException:
            self.logger.error(f"Element not clickable within timeout: {locator}")
            raise TimeoutException(f"Element not clickable: {locator}")
    
    @log_action
    @retry_on_exception(max_retries=2)
    def enter_text(self, locator: tuple, text: str, clear_first: bool = True) -> None:
        """
        Enter text into an input field
        
        Args:
            locator: Tuple containing locator strategy and value
            text: Text to enter
            clear_first: Whether to clear the field first
        """
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            if clear_first:
                element.clear()
            element.send_keys(text)
            self.logger.info(f"Successfully entered text in element: {locator}")
        except TimeoutException:
            self.logger.error(f"Element not visible within timeout: {locator}")
            raise TimeoutException(f"Element not visible: {locator}")
    
    @log_action
    @handle_exceptions(default_return="")
    def get_text(self, locator: tuple) -> str:
        """
        Get text from an element
        
        Args:
            locator: Tuple containing locator strategy and value
            
        Returns:
            Text content of the element
        """
        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            text = element.text
            self.logger.info(f"Retrieved text from element: {locator}")
            return text
        except TimeoutException:
            self.logger.error(f"Element not visible within timeout: {locator}")
            raise TimeoutException(f"Element not visible: {locator}")
    
    @handle_exceptions(default_return="")
    def get_attribute(self, locator: tuple, attribute: str) -> str:
        """
        Get attribute value from an element
        
        Args:
            locator: Tuple containing locator strategy and value
            attribute: Attribute name
            
        Returns:
            Attribute value
        """
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            return element.get_attribute(attribute)
        except TimeoutException:
            raise TimeoutException(f"Element not found: {locator}")
    
    @handle_exceptions(default_return=False)
    def is_element_displayed(self, locator: tuple, timeout: int = 5) -> bool:
        """
        Check if element is displayed
        
        Args:
            locator: Tuple containing locator strategy and value
            timeout: Timeout in seconds
            
        Returns:
            True if element is displayed, False otherwise
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    @handle_exceptions(default_return=False)
    def is_element_present(self, locator: tuple) -> bool:
        """
        Check if element is present in DOM
        
        Args:
            locator: Tuple containing locator strategy and value
            
        Returns:
            True if element is present, False otherwise
        """
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False
    
    @log_action
    def wait_for_element_to_disappear(self, locator: tuple, timeout: int = 10) -> bool:
        """
        Wait for element to disappear from DOM
        
        Args:
            locator: Tuple containing locator strategy and value
            timeout: Timeout in seconds
            
        Returns:
            True if element disappeared, False if still present after timeout
        """
        try:
            wait = WebDriverWait(self.driver, timeout)
            wait.until_not(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    @log_action
    def scroll_to_element(self, locator: tuple) -> None:
        """
        Scroll to an element
        
        Args:
            locator: Tuple containing locator strategy and value
        """
        element = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
    
    @log_action
    def hover_over_element(self, locator: tuple) -> None:
        """
        Hover over an element
        
        Args:
            locator: Tuple containing locator strategy and value
        """
        element = self.wait.until(EC.visibility_of_element_located(locator))
        self.actions.move_to_element(element).perform()
    
    @log_action
    def wait_for_page_to_load(self) -> None:
        """Wait for page to completely load"""
        self.wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
    
    def get_current_url(self) -> str:
        """Get current page URL"""
        return self.driver.current_url
    
    def get_page_title(self) -> str:
        """Get current page title"""
        return self.driver.title
    
    @log_action
    def refresh_page(self) -> None:
        """Refresh the current page"""
        self.driver.refresh()
    
    def navigate_back(self) -> None:
        """Navigate back in browser history"""
        self.driver.back()
    
    def navigate_forward(self) -> None:
        """Navigate forward in browser history"""
        self.driver.forward()
    
    def find_elements(self, locator: tuple) -> List[WebElement]:
        """
        Find multiple elements
        
        Args:
            locator: Tuple containing locator strategy and value
            
        Returns:
            List of WebElements
        """
        return self.driver.find_elements(*locator)
    
    @abstractmethod
    def is_page_displayed(self) -> bool:
        """
        Abstract method to check if page is displayed
        Must be implemented by all page classes
        
        Returns:
            True if page is displayed correctly, False otherwise
        """
        pass
