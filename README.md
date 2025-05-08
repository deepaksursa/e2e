# ParaBank E2E Test Automation Framework

This project implements an end-to-end automation testing framework using Python, Pytest, and Playwright for testing the ParaBank application.

## Prerequisites

- Python 3.12 or higher
- pip (Python package installer)
- Git

## Project Structure

```
e2e/
├── config/                 # Configuration files
│   ├── env.py             # Environment configuration
│   ├── parabank.json      # ParaBank specific configuration
│   └── dev.json           # Development environment configuration
├── data/                  # Test data files
├── pages/                 # Page Object Models
│   ├── base_page.py       # Base page with common methods
│   ├── parabank_login_page.py # Login page object
│   └── parabank_register_page.py # Registration page object
├── test-result/           # Test execution results
│   ├── screenshots/       # Test screenshots
│   └── html/             # HTML test reports
├── utils/                 # Utility functions
│   ├── api_helpers.py     # API interaction utilities
│   └── data_generator.py  # Test data generation utilities
├── tests/                 # Test files
│   ├── ui/               # UI tests
│   │   ├── test_parabank_login.py # Login tests
│   │   └── test_parabank_register.py # Registration tests
│   └── api/              # API tests
│       ├── test_parabank_api.py # ParaBank API tests
│       └── test_smoke_basic.py # Basic smoke test
├── requirements.txt       # Python dependencies
├── pytest.ini            # Pytest configuration
├── setup.sh              # Automated setup script
├── env_example.txt       # Example environment file
└── README.md             # Project documentation
```

## Environment Configuration

The framework uses environment variables for configuration. You can customize the behavior by:

1. Copy the example environment file:
   ```bash
   cp env_example.txt .env
   ```

2. Modify the `.env` file with your settings:
   ```ini
   # Test Results Directory
   TEST_RESULTS_DIR=test-result

   # Browser Configuration
   BROWSER=chromium  # Options: chromium, firefox, webkit
   HEADLESS=false    # Options: true, false

   # Application URLs
   BASE_URL=https://parabank.parasoft.com/parabank

   # Test Credentials
   TEST_USERNAME=john
   TEST_PASSWORD=demo
   ```

## Current Test Status

The framework currently includes the following test suites:

### API Tests
- ✅ `test_basic_smoke`: Basic API smoke test
- ✅ `test_api_availability`: Verify ParaBank API endpoints are available 
- ✅ `test_accounts_endpoint`: Test accounts endpoint functionality
- ✅ `test_login_api`: Test login functionality via API

### UI Tests
- ✅ `test_successful_login`: Tests successful login with valid credentials
- ✅ `test_invalid_login`: Tests login with invalid credentials
- ✅ `test_logout`: Tests successful logout functionality
- ✅ `test_successful_registration`: Tests new user registration

## Setup Instructions

### Option 1: Automated Setup (Recommended)

1. Make the setup script executable:
   ```bash
   chmod +x setup.sh
   ```

2. **To set up and activate the virtual environment in your current shell (macOS/Linux):**
   ```bash
   source setup.sh
   ```
   - This will run the setup and leave you in the activated virtual environment, so you can immediately run test commands.

   **Alternatively, to just run the setup (any OS):**
   ```bash
   ./setup.sh
   ```
   - This will set up everything, but you will need to activate the virtual environment manually afterwards:
     ```bash
     source e2e_venv/bin/activate  # macOS/Linux
     .\e2e_venv\Scripts\activate  # Windows
     ```
 

The script will:
- Check Python version
- Create and activate virtual environment (if sourced on macOS/Linux)
- Install all dependencies
- Install Playwright and browsers
- Create necessary directories
- Verify installations

### Option 2: Manual Setup

1. Create and activate virtual environment:
   ```bash
   # On macOS/Linux
   python -m venv e2e_venv
   source e2e_venv/bin/activate

   # On Windows
   python -m venv e2e_venv
   .\e2e_venv\Scripts\activate
   ```

2. Upgrade pip:
   ```bash
   pip install --upgrade pip
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Install Playwright and browsers:
   ```bash
   # Install Playwright package
   pip install playwright

   # Install browser binaries
   playwright install

   # Verify installation
   playwright --version
   ```

5. Verify setup:
   ```bash
   # Check Python path
   which python  # Should point to e2e_venv/bin/python

   # Check installed packages
   pip list  # Should show pytest, playwright, and other dependencies
   ```

## Running Tests

### Basic Test Execution

```bash
# Run all tests
python -m pytest

# Run with verbose output
python -m pytest -v

# Run specific test file
python -m pytest tests/ui/test_parabank_login.py
```

### Using Pytest Markers

```bash
# Run only UI tests
python -m pytest -m "ui"

# Run only API tests
python -m pytest -m "api"

# Run tests with specific marker
python -m pytest -m "smoke"
```

### Browser Options

```bash
# Run tests in specific browser
python -m pytest --browser chromium
python -m pytest --browser firefox
python -m pytest --browser webkit
```

### Additional Options

```bash
# Run tests in headless mode
python -m pytest --headless

# Run tests with slower execution (for debugging)
python -m pytest --slow

# Run tests against different environment
python -m pytest --env staging
```

## Test Reports

### HTML Reports

```bash
# Generate HTML report
python -m pytest --html=test-result/html/report.html

# Generate HTML report with screenshots
python -m pytest --html=test-result/html/report.html --self-contained-html
```

### Allure Reports

```bash
# Generate Allure report
python -m pytest --alluredir=test-result/allure-results

# View Allure report (requires Allure to be installed)
allure serve test-result/allure-results
```

## Quick Run Script

For a quick functional test without setting up Pytest, you can use:

```bash
# Run a simple login test with Playwright directly
python run_tests.py
```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'pytest'**
   - Ensure you're in the virtual environment
   - Run `pip install -r requirements.txt` again

2. **Playwright browsers not found**
   - Run `playwright install` to install browsers
   - If issues persist, try `playwright install --force`

3. **Virtual environment issues**
   - Delete the existing virtual environment
   - Create a new one using `python -m venv e2e_venv`
   - Run the setup script again

4. **Permission issues with setup script**
   - Run `chmod +x setup.sh` to make it executable