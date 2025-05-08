import allure
import logging
from pages.base_page import BasePage

logger = logging.getLogger(__name__)

class ParaBankRegisterPage(BasePage):
    """Page object for the ParaBank Registration page"""
    
    # Element locators
    FIRST_NAME_INPUT = "input[id='customer.firstName']"
    LAST_NAME_INPUT = "input[id='customer.lastName']"
    ADDRESS_INPUT = "input[id='customer.address.street']"
    CITY_INPUT = "input[id='customer.address.city']"
    STATE_INPUT = "input[id='customer.address.state']"
    ZIP_CODE_INPUT = "input[id='customer.address.zipCode']"
    PHONE_INPUT = "input[id='customer.phoneNumber']"
    SSN_INPUT = "input[id='customer.ssn']"
    USERNAME_INPUT = "input[id='customer.username']"
    PASSWORD_INPUT = "input[id='customer.password']"
    CONFIRM_PASSWORD_INPUT = "input[id='repeatedPassword']"
    REGISTER_BUTTON = "input[type='submit'][value='Register']"
    ERROR_MESSAGE = ".error"
    SUCCESS_MESSAGE = "#rightPanel p"
    
    @allure.step("Navigate to ParaBank registration page")
    def navigate(self):
        """Navigate to the ParaBank registration page"""
        logger.info("Navigating to ParaBank registration page")
        self.page.goto("https://parabank.parasoft.com/parabank/register.htm")
        self.wait_for_page_load()
        # Verify we're on the registration page
        if not self.is_registration_form_visible():
            raise Exception("Failed to load registration page")
    
    @allure.step("Register a new user")
    def register_user(self, user_data):
        """
        Register a new user with the provided data
        
        Args:
            user_data: Dictionary containing user registration data
        """
        logger.info(f"Registering new user with username: {user_data.get('username', '')}")
        
        # Fill in personal information
        self.fill_text(self.FIRST_NAME_INPUT, user_data.get('firstName', ''))
        self.fill_text(self.LAST_NAME_INPUT, user_data.get('lastName', ''))
        self.fill_text(self.ADDRESS_INPUT, user_data.get('address', ''))
        self.fill_text(self.CITY_INPUT, user_data.get('city', ''))
        self.fill_text(self.STATE_INPUT, user_data.get('state', ''))
        self.fill_text(self.ZIP_CODE_INPUT, user_data.get('zipCode', ''))
        self.fill_text(self.PHONE_INPUT, user_data.get('phone', ''))
        self.fill_text(self.SSN_INPUT, user_data.get('ssn', ''))
        
        # Fill in account information
        self.fill_text(self.USERNAME_INPUT, user_data.get('username', ''))
        self.fill_text(self.PASSWORD_INPUT, user_data.get('password', ''))
        self.fill_text(self.CONFIRM_PASSWORD_INPUT, user_data.get('confirm', ''))
        
        # Submit registration form
        logger.info("Clicking register button")
        self.click(self.REGISTER_BUTTON)
        self.wait_for_network_idle()
        
        # Check for any error messages
        error_message = self.get_error_message()
        if error_message:
            logger.error(f"Registration error: {error_message}")
            return False
        
        # Check for success message
        success_message = self.get_success_message()
        logger.info(f"Registration result: {success_message}")
        return success_message is not None and "created successfully" in success_message.lower()
    
    @allure.step("Get registration error message")
    def get_error_message(self):
        """Get the error message displayed on failed registration"""
        if self.is_element_visible(self.ERROR_MESSAGE):
            error_text = self.get_text(self.ERROR_MESSAGE)
            logger.info(f"Found error message: {error_text}")
            return error_text
        return None
    
    @allure.step("Get registration success message")
    def get_success_message(self):
        """Get the success message displayed on successful registration"""
        if self.is_element_visible(self.SUCCESS_MESSAGE):
            success_text = self.get_text(self.SUCCESS_MESSAGE)
            logger.info(f"Found success message: {success_text}")
            return success_text
        logger.warning("Success message not found")
        return None
    
    @allure.step("Check if registration was successful")
    def is_registration_successful(self):
        """Check if registration was successful by looking for success message"""
        # After successful registration, user is redirected to welcome page
        success_text = self.get_success_message()
        if success_text:
            logger.info(f"Registration success check: {success_text}")
            return "created successfully" in success_text.lower()
        logger.warning("Registration success check failed: No success message found")
        return False
    
    @allure.step("Check if registration form is visible")
    def is_registration_form_visible(self):
        """Check if registration form is visible on the page"""
        form_visible = (
            self.is_element_visible(self.FIRST_NAME_INPUT) and
            self.is_element_visible(self.LAST_NAME_INPUT) and
            self.is_element_visible(self.REGISTER_BUTTON)
        )
        logger.info(f"Registration form visibility check: {form_visible}")
        return form_visible 