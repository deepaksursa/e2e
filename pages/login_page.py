import allure
import logging
from pages.base_page import BasePage

logger = logging.getLogger(__name__)

class LoginPage(BasePage):
    """Page object for the Login page"""
    
    # Element locators
    USERNAME_INPUT = "input[name='username']"
    PASSWORD_INPUT = "input[name='password']"
    LOGIN_BUTTON = "input[type='submit'][value='Log In']"
    ERROR_MESSAGE = ".error"
    FORGOT_LOGIN_INFO_LINK = "a[href*='lookup.htm']"
    REGISTER_LINK = "a[href*='register.htm']"
    LOGOUT_LINK = "a[href*='logout.htm']"
    ACCOUNTS_OVERVIEW_TITLE = "#rightPanel h1"
    
    @allure.step("Navigate to login page")
    def navigate(self):
        """Navigate to the login page"""
        logger.info("Navigating to login page")
        self.page.goto("https://parabank.parasoft.com/parabank/index.htm")
        self.wait_for_page_load()
        assert self.is_login_form_visible(), "Login page did not load correctly"
    
    @allure.step("Login with username: {username}")
    def login(self, username, password):
        """
        Login with the provided username and password
        
        Args:
            username: The username to use
            password: The password to use
        """
        logger.info(f"Logging in with username: {username}")
        self.fill_text(self.USERNAME_INPUT, username)
        self.fill_text(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BUTTON)
        self.wait_for_network_idle()
    
    @allure.step("Get login error message")
    def get_error_message(self):
        """Get the error message displayed on failed login"""
        if self.is_element_visible(self.ERROR_MESSAGE):
            error_text = self.get_text(self.ERROR_MESSAGE)
            logger.info(f"Found login error message: {error_text}")
            return error_text
        logger.warning("No error message found on login page")
        return None
    
    @allure.step("Click forgot login info link")
    def click_forgot_login_info(self):
        """Click the forgot login info link"""
        logger.info("Clicking forgot login info link")
        self.click(self.FORGOT_LOGIN_INFO_LINK)
        self.wait_for_network_idle()
    
    @allure.step("Navigate to registration page")
    def navigate_to_register(self):
        """Navigate to the registration page from login page"""
        logger.info("Navigating to registration page")
        self.click(self.REGISTER_LINK)
        self.wait_for_network_idle()
    
    @allure.step("Check if login form is visible")
    def is_login_form_visible(self):
        """Check if login form is visible on the page"""
        form_visible = (
            self.is_element_visible(self.USERNAME_INPUT) and 
            self.is_element_visible(self.PASSWORD_INPUT) and
            self.is_element_visible(self.LOGIN_BUTTON)
        )
        logger.info(f"Login form visibility check: {form_visible}")
        return form_visible
    
    @allure.step("Check if user is logged in")
    def is_user_logged_in(self):
        """Check if the user is currently logged in"""
        logged_in = self.is_element_visible(self.LOGOUT_LINK)
        logger.info(f"User logged in check: {logged_in}")
        return logged_in
    
    @allure.step("Log out user")
    def logout(self):
        """Log out the current user"""
        if self.is_user_logged_in():
            logger.info("Logging out user")
            self.click(self.LOGOUT_LINK)
            self.wait_for_network_idle()
            assert self.is_login_form_visible(), "Logout failed - login form not visible after logout"
            return True
        logger.warning("Cannot logout - user is not logged in")
        return False
    
    @allure.step("Verify accounts overview page")
    def verify_accounts_overview(self):
        """Verify that the accounts overview page is displayed"""
        is_on_accounts_page = self.is_element_visible(self.ACCOUNTS_OVERVIEW_TITLE)
        if is_on_accounts_page:
            title = self.get_text(self.ACCOUNTS_OVERVIEW_TITLE)
            logger.info(f"Accounts overview page visible with title: {title}")
            return "Accounts Overview" in title
        logger.warning("Accounts overview page not visible")
        return False 