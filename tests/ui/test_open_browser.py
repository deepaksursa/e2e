import pytest
from playwright.sync_api import sync_playwright

class TestMultiBrowser:
    """Test suite for multi-browser testing"""
    
    def test_launch_multiple_browsers(self):
        """Test opening multiple browsers simultaneously"""
        p = sync_playwright().start()
        try:
            # Launch Chrome
            try:
                chrome = p.chromium.launch(channel="chrome", headless=False)
                chrome_page = chrome.new_page()
                chrome_page.goto("https://www.google.com")
                chrome_page.wait_for_timeout(1000)
                assert "Google" in chrome_page.title(), "Chrome failed to load Google"
                chrome_page.screenshot(path="test-result/screenshots/chrome-screenshot.png")
                chrome.close()
            except Exception as e:
                print(f"Chrome test skipped: {str(e)}")
            
            # Launch Edge
            try:
                edge = p.chromium.launch(channel="msedge", headless=False)
                edge_page = edge.new_page()
                edge_page.goto("https://www.bing.com")
                edge_page.wait_for_timeout(1000)
                assert "Bing" in edge_page.title(), "Edge failed to load Bing"
                edge_page.screenshot(path="test-result/screenshots/edge-screenshot.png")
                edge.close()
            except Exception as e:
                print(f"Edge test skipped: {str(e)}")
            
            # Launch Firefox
            firefox = p.firefox.launch(headless=False)
            firefox_page = firefox.new_page()
            firefox_page.goto("https://www.mozilla.org")
            firefox_page.wait_for_timeout(1000)
            assert "Mozilla" in firefox_page.title(), "Firefox failed to load Mozilla"
            firefox_page.screenshot(path="test-result/screenshots/firefox-screenshot.png")
            firefox.close()
            
            # Launch Safari (WebKit)
            webkit = p.webkit.launch(headless=False)
            webkit_page = webkit.new_page()
            webkit_page.goto("https://www.apple.com")
            webkit_page.wait_for_timeout(1000)
            assert "Apple" in webkit_page.title(), "WebKit failed to load Apple"
            webkit_page.screenshot(path="test-result/screenshots/webkit-screenshot.png")
            webkit.close()
        finally:
            p.stop()

if __name__ == "__main__":
    pytest.main()
  

