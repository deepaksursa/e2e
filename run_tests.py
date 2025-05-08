#!/usr/bin/env python3
"""
Simple test runner script for the E2E framework using Playwright directly
This avoids dependency conflicts with pytest-playwright
"""

import sys
from playwright.sync_api import sync_playwright
from config.env import (
    SCREENSHOTS_DIR,
    LOGIN_URL,
    TEST_USERNAME,
    TEST_PASSWORD,
    BROWSER,
    HEADLESS
)

def run_login_test():
    """Run a simple login test using Playwright directly"""
    print("Running login test with Playwright...")
    
    with sync_playwright() as p:
        # Get browser type dynamically
        browser_type = getattr(p, BROWSER)
        browser = browser_type.launch(headless=HEADLESS)
        page = browser.new_page()
        
        try:
            # Navigate to ParaBank
            print("Navigating to ParaBank login page...")
            page.goto(LOGIN_URL)
            
            # Fill in credentials
            print("Entering credentials...")
            page.fill("input[name='username']", TEST_USERNAME)
            page.fill("input[name='password']", TEST_PASSWORD)
            
            # Click login - try a more generic selector
            print("Clicking login button...")
            page.click("input[type='submit']")
            
            # Wait for navigation
            print("Waiting for page to load...")
            page.wait_for_load_state("networkidle")
            
            # Take screenshot
            print("Taking screenshot...")
            page.screenshot(path=SCREENSHOTS_DIR / "login_result.png")
            
            # Verify login success
            print("Verifying login success...")
            print(f"Page title: {page.title()}")
            print(f"Current URL: {page.url}")
            
            if "Log Out" in page.content():
                print("✅ TEST PASSED: Successfully logged in!")
            else:
                print("❌ TEST FAILED: Login unsuccessful")
        except Exception as e:
            print(f"Error during test: {e}")
        finally:
            # Clean up
            print("Closing browser...")
            browser.close()
        
if __name__ == "__main__":
    run_login_test()
    print("Test run complete!") 