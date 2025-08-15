# src/utils/driver_manager.py
"""
WebDriver management utility
"""
import os
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from src.constants.framework_constants import FrameworkConstants


class DriverManager:
    """Manages WebDriver instances"""
    
    _driver: Optional[webdriver.Remote] = None
    
    @staticmethod
    def get_driver(browser_name: str = "chrome", headless: bool = False) -> webdriver.Remote:
        """
        Get WebDriver instance
        
        Args:
            browser_name: Browser name (chrome, firefox, edge)
            headless: Whether to run in headless mode
            
        Returns:
            WebDriver instance
        """
        if DriverManager._driver is None:
            DriverManager._driver = DriverManager._create_driver(browser_name, headless)
        return DriverManager._driver
    
    @staticmethod
    def _create_driver(browser_name: str, headless: bool) -> webdriver.Remote:
        """
        Create WebDriver instance based on browser name
        
        Args:
            browser_name: Browser name
            headless: Whether to run headlessly
            
        Returns:
            WebDriver instance
        """
        browser_name = browser_name.lower()
        
        if browser_name == FrameworkConstants.CHROME_BROWSER:
            return DriverManager._create_chrome_driver(headless)
        elif browser_name == FrameworkConstants.FIREFOX_BROWSER:
            return DriverManager._create_firefox_driver(headless)
        elif browser_name == FrameworkConstants.EDGE_BROWSER:
            return DriverManager._create_edge_driver(headless)
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")
    
    @staticmethod
    def _create_chrome_driver(headless: bool) -> webdriver.Chrome:
        """Create Chrome WebDriver"""
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-extensions")
        
        if headless:
            options.add_argument("--headless")
        
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        
        # Set timeouts
        driver.implicitly_wait(FrameworkConstants.IMPLICIT_WAIT_TIMEOUT)
        driver.set_page_load_timeout(FrameworkConstants.PAGE_LOAD_TIMEOUT)
        
        return driver
    
    @staticmethod
    def _create_firefox_driver(headless: bool) -> webdriver.Firefox:
        """Create Firefox WebDriver"""
        options = FirefoxOptions()
        
        if headless:
            options.add_argument("--headless")
        
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
        driver.maximize_window()
        
        # Set timeouts
        driver.implicitly_wait(FrameworkConstants.IMPLICIT_WAIT_TIMEOUT)
        driver.set_page_load_timeout(FrameworkConstants.PAGE_LOAD_TIMEOUT)
        
        return driver
    
    @staticmethod
    def _create_edge_driver(headless: bool) -> webdriver.Edge:
        """Create Edge WebDriver"""
        options = EdgeOptions()
        options.add_argument("--start-maximized")
        
        if headless:
            options.add_argument("--headless")
        
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
        
        # Set timeouts
        driver.implicitly_wait(FrameworkConstants.IMPLICIT_WAIT_TIMEOUT)
        driver.set_page_load_timeout(FrameworkConstants.PAGE_LOAD_TIMEOUT)
        
        return driver
    
    @staticmethod
    def quit_driver() -> None:
        """Quit the WebDriver instance"""
        if DriverManager._driver:
            DriverManager._driver.quit()
            DriverManager._driver = None
