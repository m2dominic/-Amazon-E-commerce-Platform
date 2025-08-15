# src/utils/config_manager.py
"""
Configuration management utility with decorators and validation
"""
import os
import configparser
from typing import Any, Optional
from functools import wraps, lru_cache
from src.constants.framework_constants import FrameworkConstants
import logging

logger = logging.getLogger(__name__)


def validate_config(validation_func):
    """
    Decorator to validate configuration values
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            if validation_func:
                if not validation_func(result):
                    raise ValueError(f"Invalid configuration value: {result}")
            return result
        return wrapper
    return decorator


def cache_config(func):
    """
    Decorator to cache configuration values
    """
    @wraps(func)
    @lru_cache(maxsize=128)
    def wrapper(self, *args, **kwargs):
        return func(self, *args, **kwargs)
    return wrapper


class ConfigManager:
    """Enhanced configuration manager with validation and caching"""
    
    _instance: Optional['ConfigManager'] = None
    _config: Optional[configparser.ConfigParser] = None
    
    def __new__(cls) -> 'ConfigManager':
        """Singleton implementation"""
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self) -> None:
        """Initialize configuration"""
        self._config = configparser.ConfigParser()
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from file"""
        config_path = FrameworkConstants.CONFIG_FILE_PATH
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        try:
            self._config.read(config_path)
            logger.info(f"Configuration loaded from: {config_path}")
        except Exception as e:
            raise Exception(f"Failed to load configuration: {e}")
    
    def get_property(self, section: str, key: str, fallback: Any = None) -> str:
        """
        Get property value from configuration
        
        Args:
            section: Configuration section
            key: Property key
            fallback: Default value if key not found
            
        Returns:
            Property value
        """
        try:
            return self._config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            if fallback is not None:
                logger.warning(f"Using fallback value for {section}.{key}: {fallback}")
                return str(fallback)
            raise KeyError(f"Property '{section}.{key}' not found in configuration")
    
    def get_boolean(self, section: str, key: str, fallback: bool = False) -> bool:
        """Get boolean property"""
        try:
            return self._config.getboolean(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return fallback
    
    def get_int(self, section: str, key: str, fallback: int = 0) -> int:
        """Get integer property"""
        try:
            return self._config.getint(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return fallback
    
    def get_float(self, section: str, key: str, fallback: float = 0.0) -> float:
        """Get float property"""
        try:
            return self._config.getfloat(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            return fallback
    
    # Browser Configuration
    @cache_config
    @validate_config(lambda x: x.lower() in ['chrome', 'firefox', 'edge', 'safari'])
    def get_browser(self) -> str:
        """Get browser name"""
        return self.get_property('BROWSER', 'browser', 'chrome')
    
    @cache_config
    def is_headless(self) -> bool:
        """Check if browser should run in headless mode"""
        return self.get_boolean('BROWSER', 'headless', False)
    
    # URL Configuration
    @cache_config
    @validate_config(lambda x: x.startswith('http'))
    def get_base_url(self) -> str:
        """Get base URL"""
        return self.get_property('URLS', 'base_url')
    
    @cache_config
    def get_login_url(self) -> str:
        """Get login URL"""
        return self.get_property('URLS', 'login_url')
    
    # Credentials
    @cache_config
    def get_test_email(self) -> str:
        """Get test email"""
        return self.get_property('CREDENTIALS', 'test_email')
    
    @cache_config
    def get_test_password(self) -> str:
        """Get test password"""
        return self.get_property('CREDENTIALS', 'test_password')
    
    @cache_config
    def get_invalid_email(self) -> str:
        """Get invalid email for negative testing"""
        return self.get_property('CREDENTIALS', 'invalid_email')
    
    # Timeout Configuration
    @cache_config
    @validate_config(lambda x: x > 0)
    def get_explicit_wait_timeout(self) -> int:
        """Get explicit wait timeout"""
        return self.get_int('TIMEOUTS', 'explicit_wait_timeout', 10)
    
    @cache_config
    def get_page_load_timeout(self) -> int:
        """Get page load timeout"""
        return self.get_int('TIMEOUTS', 'page_load_timeout', 30)
    
    @cache_config
    def get_implicit_wait_timeout(self) -> int:
        """Get implicit wait timeout"""
        return self.get_int('TIMEOUTS', 'implicit_wait_timeout', 5)
    
    # Reporting Configuration
    @cache_config
    def should_generate_reports(self) -> bool:
        """Check if reports should be generated"""
        return self.get_boolean('REPORTING', 'generate_reports', True)
    
    @cache_config
    def should_take_screenshot_on_failure(self) -> bool:
        """Check if screenshots should be taken on failure"""
        return self.get_boolean('REPORTING', 'screenshot_on_failure', True)
    
    @cache_config
    def should_take_screenshot_on_pass(self) -> bool:
        """Check if screenshots should be taken on pass"""
        return self.get_boolean('REPORTING', 'screenshot_on_pass', False)
    
    # Execution Configuration
    @cache_config
    def get_thread_count(self) -> int:
        """Get thread count for parallel execution"""
        return self.get_int('EXECUTION', 'thread_count', 1)
    
    @cache_config
    def get_retry_count(self) -> int:
        """Get retry count for failed tests"""
        return self.get_int('EXECUTION', 'retry_failed_tests', 0)
    
    # Amazon Specific Configuration
    @cache_config
    def get_search_product(self) -> str:
        """Get search product for testing"""
        return self.get_property('AMAZON_TEST_DATA', 'search_product', 'laptop')
    
    @cache_config
    def get_search_category(self) -> str:
        """Get search category"""
        return self.get_property('AMAZON_TEST_DATA', 'search_category', 'Electronics')
    
    @cache_config
    def get_min_price(self) -> int:
        """Get minimum price filter"""
        return self.get_int('AMAZON_TEST_DATA', 'min_price', 0)
    
    @cache_config
    def get_max_price(self) -> int:
        """Get maximum price filter"""
        return self.get_int('AMAZON_TEST_DATA', 'max_price', 10000)
    
    def reload_config(self) -> None:
        """Reload configuration from file"""
        self._load_config()
        # Clear cache
        for method_name in dir(self):
            method = getattr(self, method_name)
            if hasattr(method, 'cache_clear'):
                method.cache_clear()
        logger.info("Configuration reloaded and cache cleared")


# Singleton instance
config_manager = ConfigManager()
```product=laptop
search.category=Electronics
min.price=100
max.price=2000
