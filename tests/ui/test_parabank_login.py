import pytest
import allure
from pages.parabank_login_page import ParaBankLoginPage

@allure.feature("ParaBank")
@allure.story("Authentication")
class TestParaBankLogin:
    """Test suite for ParaBank login functionality"""
    
    @allure.title("User can login with valid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    def test_successful_login(self, page, config):
        """Verify that a user can login with valid credentials"""
        # Initialize page object
        login_page = ParaBankLoginPage(page)
        
        # Navigate to login page
        login_page.navigate()
        
        # Get user credentials from config
        username = config['users']['default']['username']
        password = config['users']['default']['password']
        
        # Perform login with valid credentials
        login_page.login(username, password)
        
        # Take screenshot for report
        login_page.take_screenshot("successful_login")
        
        # Verify login was successful
        assert "Accounts Overview" in page.title(), "User not redirected to accounts page after login"
        assert page.locator("a:text('Log Out')").is_visible(), "Log Out link not visible after login"
    
    @allure.title("User cannot login with invalid credentials")
    @allure.severity(allure.severity_level.NORMAL)
    def test_invalid_login(self, page):
        """Verify that a user cannot login with invalid credentials"""
        # Initialize page object
        login_page = ParaBankLoginPage(page)
        
        # Navigate to login page
        login_page.navigate()
        
        # Attempt login with invalid credentials
        login_page.login("invalid_user", "invalid_password")
        
        # Take screenshot for report
        login_page.take_screenshot("invalid_login")
        
        # Verify error message is displayed
        error_message = login_page.get_error_message()
        assert error_message is not None, "No error message displayed for invalid login"
        
        # Check for any of the possible error messages - ParaBank can show different messages
        possible_error_texts = [
            "could not be verified",
            "invalid username",
            "invalid password",
            "username and password are required",
            "error logging in"
        ]
        
        is_error_message_valid = any(text.lower() in error_message.lower() for text in possible_error_texts)
        assert is_error_message_valid, f"Unexpected error message: {error_message}"
        
        # Verify user remains on login page
        assert login_page.is_login_form_visible(), "Login form not visible after failed login"
    
    @allure.title("User can log out successfully")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_logout(self, page, config):
        """Verify that a logged-in user can successfully log out"""
        # Initialize page object
        login_page = ParaBankLoginPage(page)
        
        # Navigate to login page
        login_page.navigate()
        
        # Get user credentials from config
        username = config['users']['default']['username']
        password = config['users']['default']['password']
        
        # Perform login
        login_page.login(username, password)
        
        # Verify login was successful
        assert page.locator("a:text('Log Out')").is_visible(), "Login failed, Log Out link not visible"
        
        # Perform logout
        page.locator("a:text('Log Out')").click()
        login_page.wait_for_network_idle()
        
        # Take screenshot for report
        login_page.take_screenshot("logout_completed")
        
        # Verify logout was successful
        assert login_page.is_login_form_visible(), "Login form not visible after logout"
        assert "Log In" in page.content(), "Log In button not visible after logout" 