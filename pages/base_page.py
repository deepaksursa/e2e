import allure
import logging
import os
from typing import Any, Dict, List, Optional, Union
from playwright.sync_api import Page, Locator, TimeoutError as PlaywrightTimeoutError
from config.env import SCREENSHOTS_DIR

# Set up logging
logger = logging.getLogger(__name__)

class BasePage:
    """
    Base Page Object Model class providing common methods for all pages
    """
    
    def __init__(self, page: Page):
        self.page = page
    
    @allure.step("Navigate to URL: {url}")
    def navigate(self, url: str) -> None:
        """Navigate to a specific URL"""
        logger.info(f"Navigating to {url}")
        self.page.goto(url)
    
    @allure.step("Wait for page load complete")
    def wait_for_page_load(self) -> None:
        """Wait for page to be fully loaded"""
        self.page.wait_for_load_state("networkidle")
        logger.info("Page fully loaded")
    
    @allure.step("Get element: {selector}")
    def get_element(self, selector: str) -> Locator:
        """Get an element by CSS or XPath selector"""
        logger.debug(f"Getting element with selector: {selector}")
        return self.page.locator(selector)
    
    @allure.step("Click element: {selector}")
    def click(self, selector: str, force: bool = False, 
              timeout: int = 10000) -> None:
        """Click on an element"""
        logger.info(f"Clicking element: {selector}")
        element = self.get_element(selector)
        element.wait_for(state="visible", timeout=timeout)
        element.click(force=force)
    
    @allure.step("Fill input: {selector} with text: {text}")
    def fill_text(self, selector: str, text: str, timeout: int = 10000) -> None:
        """Fill text in an input field"""
        logger.info(f"Filling '{text}' in {selector}")
        element = self.get_element(selector)
        element.wait_for(state="visible", timeout=timeout)
        element.fill(text)
    
    @allure.step("Get text from element: {selector}")
    def get_text(self, selector: str, timeout: int = 10000) -> str:
        """Get text from an element"""
        logger.info(f"Getting text from element: {selector}")
        element = self.get_element(selector)
        element.wait_for(state="visible", timeout=timeout)
        return element.text_content() or ""
    
    @allure.step("Check if element exists: {selector}")
    def is_element_visible(self, selector: str, timeout: int = 5000) -> bool:
        """Check if element is visible on the page"""
        logger.info(f"Checking if element is visible: {selector}")
        try:
            element = self.get_element(selector)
            return element.is_visible(timeout=timeout)
        except PlaywrightTimeoutError:
            return False
    
    @allure.step("Wait for element: {selector}")
    def wait_for_element(self, selector: str, state: str = "visible", 
                         timeout: int = 10000) -> Locator:
        """Wait for an element to be in a specific state"""
        logger.info(f"Waiting for element {selector} to be {state}")
        element = self.get_element(selector)
        element.wait_for(state=state, timeout=timeout)
        return element
    
    @allure.step("Select option: {value} from dropdown: {selector}")
    def select_option(self, selector: str, value: str, timeout: int = 10000) -> None:
        """Select an option from a dropdown by value"""
        logger.info(f"Selecting option '{value}' from dropdown {selector}")
        element = self.get_element(selector)
        element.wait_for(state="visible", timeout=timeout)
        element.select_option(value=value)
    
    @allure.step("Get all text from elements: {selector}")
    def get_elements_text(self, selector: str) -> List[str]:
        """Get text from all matching elements"""
        logger.info(f"Getting text from all elements matching: {selector}")
        elements = self.page.locator(selector).all()
        return [element.text_content() or "" for element in elements]
    
    @allure.step("Take screenshot: {name}")
    def take_screenshot(self, name: str = "screenshot") -> bytes:
        """Take a screenshot and attach to Allure report"""
        logger.info(f"Taking screenshot: {name}")
        screenshot_path = SCREENSHOTS_DIR / f"{name}.png"
        screenshot = self.page.screenshot(path=screenshot_path)
        allure.attach(screenshot, name=name, attachment_type=allure.attachment_type.PNG)
        return screenshot
    
    @allure.step("Scroll element into view: {selector}")
    def scroll_into_view(self, selector: str, timeout: int = 10000) -> None:
        """Scroll element into view"""
        logger.info(f"Scrolling element into view: {selector}")
        element = self.get_element(selector)
        element.wait_for(state="attached", timeout=timeout)
        element.scroll_into_view_if_needed()
    
    @allure.step("Hover over element: {selector}")
    def hover(self, selector: str, timeout: int = 10000) -> None:
        """Hover over an element"""
        logger.info(f"Hovering over element: {selector}")
        element = self.get_element(selector)
        element.wait_for(state="visible", timeout=timeout)
        element.hover()
    
    @allure.step("Check/uncheck checkbox: {selector} to state: {check}")
    def set_checkbox(self, selector: str, check: bool = True, 
                     timeout: int = 10000) -> None:
        """Check or uncheck a checkbox"""
        state = "check" if check else "uncheck"
        logger.info(f"{state.capitalize()}ing checkbox: {selector}")
        element = self.get_element(selector)
        element.wait_for(state="visible", timeout=timeout)
        
        if check:
            element.check()
        else:
            element.uncheck()
    
    @allure.step("Get attribute: {attribute} from element: {selector}")
    def get_attribute(self, selector: str, attribute: str, 
                      timeout: int = 10000) -> Optional[str]:
        """Get attribute value from an element"""
        logger.info(f"Getting attribute '{attribute}' from element: {selector}")
        element = self.get_element(selector)
        element.wait_for(state="attached", timeout=timeout)
        return element.get_attribute(attribute)
    
    @allure.step("Press key: {key}")
    def press_key(self, key: str) -> None:
        """Press a key on the keyboard"""
        logger.info(f"Pressing key: {key}")
        self.page.keyboard.press(key)
    
    @allure.step("Execute JavaScript: {script}")
    def execute_script(self, script: str, arg: Any = None) -> Any:
        """Execute JavaScript in the browser context"""
        logger.info("Executing JavaScript")
        return self.page.evaluate(script, arg)
    
    @allure.step("Wait for network idle")
    def wait_for_network_idle(self) -> None:
        """Wait for network to be idle (no requests for 500ms)"""
        logger.info("Waiting for network to be idle")
        self.page.wait_for_load_state("networkidle")
    
    @allure.step("Reload page")
    def reload_page(self) -> None:
        """Reload the current page"""
        logger.info("Reloading page")
        self.page.reload() 