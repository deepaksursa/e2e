import os
from pathlib import Path

# Base project directory
BASE_DIR = Path(__file__).parent.parent

# Test results directory
TEST_RESULTS_DIR = os.getenv('TEST_RESULTS_DIR', BASE_DIR / 'test-result')

# Screenshots directory
SCREENSHOTS_DIR = TEST_RESULTS_DIR / 'screenshots'

# HTML reports directory
HTML_REPORTS_DIR = TEST_RESULTS_DIR / 'html'

# Allure results directory
ALLURE_RESULTS_DIR = TEST_RESULTS_DIR / 'allure-results'

# Create directories if they don't exist
for directory in [TEST_RESULTS_DIR, SCREENSHOTS_DIR, HTML_REPORTS_DIR, ALLURE_RESULTS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Browser configuration
BROWSER = os.getenv('BROWSER', 'chromium')
HEADLESS = os.getenv('HEADLESS', 'false').lower() == 'true'

# Application URLs
BASE_URL = os.getenv('BASE_URL', 'https://parabank.parasoft.com/parabank')
LOGIN_URL = f"{BASE_URL}/index.htm"

# Test credentials
TEST_USERNAME = os.getenv('TEST_USERNAME', 'john')
TEST_PASSWORD = os.getenv('TEST_PASSWORD', 'demo') 