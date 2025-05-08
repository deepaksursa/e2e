import os
import sys
import pytest
import allure
import uuid
import random
from pathlib import Path
from pages.parabank_register_page import ParaBankRegisterPage
from utils.data_generator import DataGenerator
from config.env import SCREENSHOTS_DIR

# Add the project root to Python path
project_root = str(Path(__file__).parent.parent.parent.parent)
if project_root not in sys.path:
    sys.path.append(project_root)

@allure.feature("ParaBank Registration")
@allure.story("User Registration")
class TestParaBankRegister:
    """Test cases for ParaBank registration functionality"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page):
        """Setup for each test"""
        self.register_page = ParaBankRegisterPage(page)
        self.register_page.navigate()
    
    @allure.title("Test successful user registration")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_successful_registration(self, page, config):
        """Test that a user can successfully register with valid data"""
        try:
            # Generate test user data
            if 'users' in config and 'new_user' in config['users']:
                # Use config data if available
                user_data = dict(config['users']['new_user'])
                user_data['username'] = f"testuser_{uuid.uuid4().hex[:8]}"
            else:
                # Generate random test data if no config data
                password = DataGenerator.random_password()
                user_data = {
                    'firstName': DataGenerator.random_first_name(),
                    'lastName': DataGenerator.random_last_name(),
                    'address': DataGenerator.random_address()['street'],
                    'city': DataGenerator.random_address()['city'],
                    'state': DataGenerator.random_address()['state'],
                    'zipCode': DataGenerator.random_address()['zip'],
                    'phone': DataGenerator.random_phone_number(),
                    'ssn': ''.join([str(random.randint(0, 9)) for _ in range(9)]),
                    'username': f"testuser_{DataGenerator.random_uuid()[:8]}",
                    'password': password,
                    'confirm': password
                }
            
            # Attempt registration
            registration_successful = self.register_page.register_user(user_data)
            
            # Take screenshot for report
            self.register_page.take_screenshot("successful_registration")
            
            # Verify registration was successful
            assert registration_successful, "Registration should be successful with valid data"
            assert self.register_page.is_registration_successful(), "Should show success message after registration"
            
        except Exception as e:
            # Take screenshot on failure
            failure_screenshot_path = SCREENSHOTS_DIR / f"registration_failure_{uuid.uuid4().hex[:8]}.png"
            page.screenshot(path=failure_screenshot_path)
            raise Exception(f"Registration test failed: {str(e)}") 