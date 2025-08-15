# src/utils/element_utils.py
"""
Utility functions for element interactions
"""
from typing import List
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class ElementUtils:
    """Utility functions for common element operations"""
    
    @staticmethod
    def select_dropdown_by_visible_text(dropdown_element: WebElement, text: str) -> None:
        """
        Select dropdown option by visible text
        
        Args:
            dropdown_element: Dropdown WebElement
            text: Visible text to select
        """
        select = Select(dropdown_element)
        select.select_by_visible_text(text)
    
    @staticmethod
    def select_dropdown_by_value(dropdown_element: WebElement, value: str) -> None:
        """
        Select dropdown option by value
        
        Args:
            dropdown_element: Dropdown WebElement
            value: Value to select
        """
        select = Select(dropdown_element)
        select.select_by_value(value)
    
    @staticmethod
    def select_dropdown_by_index(dropdown_element: WebElement, index: int) -> None:
        """
        Select dropdown option by index
        
        Args:
            dropdown_element: Dropdown WebElement
            index: Index to select
        """
        select = Select(dropdown_element)
        select.select_by_index(index)
    
    @staticmethod
    def get_all_dropdown_options(dropdown_element: WebElement) -> List[WebElement]:
        """
        Get all dropdown options
        
        Args:
            dropdown_element: Dropdown WebElement
            
        Returns:
            List of option WebElements
        """
        select = Select(dropdown_element)
        return select.options
    
    @staticmethod
    def get_selected_dropdown_option(dropdown_element: WebElement) -> WebElement:
        """
        Get currently selected dropdown option
        
        Args:
            dropdown_element: Dropdown WebElement
            
        Returns:
            Selected option WebElement
        """
        select = Select(dropdown_element)
        return select.first_selected_option
    
    @staticmethod
    def wait_for_element_to_be_visible(driver, locator: tuple, timeout: int = 10) -> WebElement:
        """
        Wait for element to be visible
        
        Args:
            driver: WebDriver instance
            locator: Element locator tuple
            timeout: Timeout in seconds
            
        Returns:
            Visible WebElement
        """
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.visibility_of_element_located(locator))
    
    @staticmethod
    def wait_for_element_to_be_clickable(driver, locator: tuple, timeout: int = 10) -> WebElement:
        """
        Wait for element to be clickable
        
        Args:
            driver: WebDriver instance
            locator: Element locator tuple
            timeout: Timeout in seconds
            
        Returns:
            Clickable WebElement
        """
        wait = WebDriverWait(driver, timeout)
        return wait.until(EC.element_to_be_clickable(locator))
    
    @staticmethod
    def is_element_enabled(element: WebElement) -> bool:
        """
        Check if element is enabled
        
        Args:
            element: WebElement
            
        Returns:
            True if enabled, False otherwise
        """
        return element.is_enabled()
    
    @staticmethod
    def is_element_selected(element: WebElement) -> bool:
        """
        Check if element is selected
        
        Args:
            element: WebElement
            
        Returns:
            True if selected, False otherwise
        """
        return element.is_selected()
```;

import java.time.Duration;

public final class DriverManager {
    
    private static ThreadLocal<WebDriver> driverThreadLocal = new ThreadLocal<>();
    
    private DriverManager() {}
    
    public static void setDriver(String browserName) {
        WebDriver driver;
        
        switch (browserName.toLowerCase()) {
            case "chrome":
                ChromeOptions chromeOptions = new ChromeOptions();
                chromeOptions.addArguments("--start-maximized");
                chromeOptions.addArguments("--disable-notifications");
                driver = new ChromeDriver(chromeOptions);
                break;
                
            case "firefox":
                driver = new FirefoxDriver();
                break;
                
            case "edge":
                driver = new EdgeDriver();
                break;
                
            default:
                throw new IllegalArgumentException("Browser not supported: " + browserName);
        }
        
        driver.manage().timeouts().pageLoadTimeout(Duration.ofSeconds(FrameworkConstants.PAGE_LOAD_TIMEOUT));
        driver.manage().timeouts().implicitlyWait(Duration.ofSeconds(FrameworkConstants.IMPLICIT_WAIT_TIMEOUT));
        
        driverThreadLocal.set(driver);
    }
    
    public static WebDriver getDriver() {
        return driverThreadLocal.get();
    }
    
    public static void quitDriver() {
        if (driverThreadLocal.get() != null) {
            driverThreadLocal.get().quit();
            driverThreadLocal.remove();
        }
    }
}
