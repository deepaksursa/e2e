import os
import json
import pytest
import allure
from pathlib import Path
from typing import Dict, Any, Generator
from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright
from dotenv import load_dotenv, find_dotenv
from config.env import TEST_RESULTS_DIR, SCREENSHOTS_DIR

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Read configuration based on environment
def read_config(env: str = None) -> Dict[str, Any]:
    """
    Read configuration file based on environment
    Default to 'dev' if no environment is specified
    """
    if env is None:
        env = os.getenv("TEST_ENV", "dev")
    
    # First try parabank.json for ParaBank-specific tests
    parabank_config_path = Path(__file__).parent / "config" / "parabank.json"
    if parabank_config_path.exists():
        with open(parabank_config_path, "r") as f:
            return json.load(f)
    
    # Fall back to environment-specific config
    config_path = Path(__file__).parent / "config" / f"{env}.json"
    
    if not config_path.exists():
        pytest.fail(f"Configuration file for environment '{env}' not found at {config_path}")
    
    with open(config_path, "r") as f:
        return json.load(f)

# Pytest command line options
def pytest_addoption(parser):
    parser.addoption("--browser_name", action="store", default="chromium", help="Browser to run tests with (chromium, firefox, webkit)")
    parser.addoption("--headless", action="store_true", default=False, help="Run browser in headless mode")
    parser.addoption("--slow-mo", action="store", default=100, type=int, help="Slow down browser execution in milliseconds")
    parser.addoption("--env", action="store", default="dev", help="Environment to run tests against (dev, qa, staging, prod)")

# Fixtures for configuration
@pytest.fixture(scope="session")
def config(request):
    """Fixture to load environment configuration"""
    env = request.config.getoption("--env")
    return read_config(env)

@pytest.fixture(scope="session")
def base_url(config):
    """Get base URL from config"""
    return config.get("baseUrl", "http://localhost:3000")

# Fixtures for Playwright setup
@pytest.fixture(scope="session")
def browser_type_launch_args(request):
    """Configure browser launch arguments"""
    return {
        "headless": request.config.getoption("--headless", False),
        "slow_mo": 100,
        "timeout": 30000,  # 30 seconds
    }

@pytest.fixture(scope="session")
def browser_context_args(request, base_url):
    """Configure browser context arguments"""
    videos_dir = TEST_RESULTS_DIR / "videos"
    videos_dir.mkdir(exist_ok=True)
    
    return {
        "ignore_https_errors": True,
        "viewport": {"width": 1366, "height": 768},
        "base_url": base_url,
        "record_video_dir": str(videos_dir) if os.getenv("RECORD_VIDEO", "false").lower() == "true" else None,
    }

@pytest.fixture(scope="function")
def page(context: BrowserContext, request) -> Generator[Page, None, None]:
    """Create a new page for each test function"""
    page = context.new_page()
    
    # Add event listener for console messages
    page.on("console", lambda msg: print(f"[Browser Console] {msg.text}"))
    
    # Attach Allure step for navigation
    old_goto = page.goto
    def goto_with_allure(url, **kwargs):
        allure.attach(f"Navigating to: {url}", name="Navigation", attachment_type=allure.attachment_type.TEXT)
        return old_goto(url, **kwargs)
    page.goto = goto_with_allure
    
    # Modify screenshot method to also attach to Allure
    old_screenshot = page.screenshot
    def screenshot_with_allure(**kwargs):
        screenshot_bytes = old_screenshot(**kwargs)
        allure.attach(screenshot_bytes, name="Screenshot", attachment_type=allure.attachment_type.PNG)
        return screenshot_bytes
    page.screenshot = screenshot_with_allure
    
    yield page

# Hook to capture test outcome
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshots on test failure and attach to Allure report"""
    outcome = yield
    report = outcome.get_result()
    
    # Set report attribute for test outcome
    setattr(item, f"rep_{report.when}", report)
    
    # Check if test failed and we're in the call phase
    if report.when == "call" and report.failed:
        try:
            # Try to get page fixture
            page = item.funcargs.get("page")
            if page:
                # Take screenshot and attach to report
                screenshot = page.screenshot()
                allure.attach(
                    screenshot,
                    name="screenshot_on_failure",
                    attachment_type=allure.attachment_type.PNG
                )
                
                # Save screenshot to file
                screenshot_path = SCREENSHOTS_DIR / f"{item.name}.png"
                with open(screenshot_path, "wb") as f:
                    f.write(screenshot)
                    
        except Exception as e:
            print(f"Failed to take screenshot: {e}")

# Fixtures for test data
@pytest.fixture(scope="function")
def test_data(request):
    """Load test data from a JSON file with the same name as the test module"""
    test_module = request.module.__name__
    module_name = test_module.split(".")[-1]
    data_path = Path(__file__).parent / "data" / f"{module_name}.json"
    
    if data_path.exists():
        with open(data_path, "r") as f:
            return json.load(f)
    return {} 