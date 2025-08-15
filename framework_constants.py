# src/constants/framework_constants.py
"""
Framework constants for the Amazon automation project
"""

class FrameworkConstants:
    """Constants used throughout the framework"""
    
    # URLs
    BASE_URL = "https://www.amazon.com"
    LOGIN_URL = f"{BASE_URL}/ap/signin"
    
    # Timeouts
    EXPLICIT_WAIT_TIMEOUT = 10
    PAGE_LOAD_TIMEOUT = 30
    IMPLICIT_WAIT_TIMEOUT = 5
    
    # File Paths
    CONFIG_FILE_PATH = "config/config.ini"
    TEST_DATA_PATH = "config/test_data.json"
    SCREENSHOT_PATH = "screenshots/"
    LOG_PATH = "logs/"
    
    # Browser Options
    CHROME_BROWSER = "chrome"
    FIREFOX_BROWSER = "firefox"
    EDGE_BROWSER = "edge"
    SAFARI_BROWSER = "safari"
    
    # Test Data
    DEFAULT_TIMEOUT = 10
    RETRY_COUNT = 3
