# -Amazon-E-commerce-Platform
Design and develop amazon provides complex e-commerce flows, robust element structures, and real-world testing scenarios including login, search, cart, and checkout functionalities.

🎯 Project Vision
A comprehensive, scalable, and maintainable test automation framework built using Python and Selenium WebDriver to validate critical user journeys on Amazon's e-commerce platform. This framework demonstrates industry-standard practices including Page Object Model (POM), decorator patterns, configuration management, and robust error handling.

📋 Project Summary
Primary Objective
Develop a production-ready test automation framework that can efficiently test Amazon's core functionalities while serving as a learning project for mastering QA automation best practices.
Target Application

Website: Amazon.com E-commerce Platform
Focus Areas: Login, Search, Product Selection, Cart Management, Checkout Flow
Browser Support: Chrome, Firefox, Edge (with headless options)


🏗️ Framework Architecture
Design Patterns Used

Page Object Model (POM) - Separates page elements and actions from test logic
Singleton Pattern - For configuration and driver management
Decorator Pattern - For logging, retry mechanisms, and error handling
Factory Pattern - For driver creation based on browser type

amazon-automation-framework/
├── src/
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── base_page.py
│   │   ├── home_page.py
│   │   ├── login_page.py
│   │   ├── search_results_page.py
│   │   ├── product_details_page.py
│   │   ├── cart_page.py
│   │   └── checkout_page.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config_manager.py
│   │   ├── driver_manager.py
│   │   ├── element_utils.py
│   │   ├── wait_utils.py
│   │   └── test_data_manager.py
│   ├── constants/
│   │   ├── __init__.py
│   │   ├── framework_constants.py
│   │   └── locators.py
│   └── __init__.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_login.py
│   ├── test_search.py
│   ├── test_cart.py
│   └── test_checkout.py
├── config/
│   ├── config.ini
│   └── test_data.json
├── reports/
├── screenshots/
├── logs/
├── requirements.txt
├── pytest.ini
└── README.md

2. Utility Layer (src/utils/)

DriverManager - WebDriver lifecycle management with webdriver-manager integration
ConfigManager - Configuration handling with validation and caching
ElementUtils - Common element interaction utilities
TestDataManager - JSON-based test data management

3. Constants Layer (src/constants/)

FrameworkConstants - Framework-wide constants and settings
Locators - Centralized element locator definitions

4. Test Layer (tests/)

conftest.py - Pytest fixtures and configuration
Test Classes - Organized by functionality (login, search, cart, etc.)
✨ Key Features & Innovations
Advanced Decorator Implementation
python@log_action          # Automatic action logging
@retry_on_exception  # Auto-retry on stale elements
@handle_exceptions   # Graceful error handling
@wait_for_element    # Smart element waiting
def click_element(self, locator):
    # Enhanced click method with all features
Enhanced Error Handling

Retry Mechanisms - Automatic retries for flaky elements
Comprehensive Logging - Detailed execution logs with timestamps
Exception Management - Graceful handling of common Selenium exceptions
Screenshot on Failure - Automatic evidence capture

Smart Configuration Management

Multi-environment Support - Production, Staging, Development
Validation Decorators - Automatic config value validation
Caching System - LRU cache for frequently accessed configs
Hot Reload - Runtime configuration updates

Robust Driver Management

Auto-installation - WebDriver Manager for automatic driver setup
Cross-browser Support - Chrome, Firefox, Edge with consistent API
Headless Options - CI/CD friendly execution modes
Performance Optimization - Optimized browser configurations


🛠️ Technology Stack
Core Technologies

Python 3.8+ - Modern Python with type hints
Selenium WebDriver 4.x - Latest WebDriver features
Pytest - Advanced testing framework with fixtures
WebDriver Manager - Automatic driver management

Supporting Libraries

configparser - Configuration file handling
logging - Comprehensive logging system
functools - Decorator implementations
typing - Type hints for better code documentation
json - Test data management

Development Tools

Git - Version control with branching strategy
pytest-html - HTML test reporting
pytest-xdist - Parallel test execution
allure-pytest - Advanced test reporting

📁 Project Structure
amazon-automation-framework/
├── src/                          # Source code
│   ├── pages/                    # Page Object classes
│   │   ├── base_page.py         # Abstract base with decorators
│   │   ├── home_page.py         # Homepage interactions
│   │   ├── login_page.py        # Authentication flows
│   │   └── ...                  # Other page objects
│   ├── utils/                    # Utility modules
│   │   ├── config_manager.py    # Configuration management
│   │   ├── driver_manager.py    # WebDriver management
│   │   └── element_utils.py     # Element interaction utilities
│   └── constants/                # Constants and configurations
│       ├── framework_constants.py
│       └── locators.py          # Element locators
├── tests/                        # Test modules
│   ├── conftest.py              # Pytest configuration
│   ├── test_login.py            # Login test scenarios
│   └── ...                      # Other test modules
├── config/                       # Configuration files
│   ├── config.ini               # Framework configuration
│   └── test_data.json           # Test data sets
├── reports/                      # Test execution reports
├── screenshots/                  # Test evidence
├── logs/                         # Execution logs
├── requirements.txt              # Python dependencies
└── README.md                     # Project documentation
