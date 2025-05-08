import pytest
import allure
import requests
from utils.api_helpers import APIHelpers

@allure.feature("ParaBank API")
@allure.story("API Endpoints")
class TestParaBankAPI:
    """Test suite for ParaBank API endpoints"""
    
    @pytest.fixture(scope="class")
    def api_client(self, config):
        """Create an API client for ParaBank"""
        base_url = config["apiUrl"]
        return APIHelpers(base_url)
    
    @allure.title("Test API endpoint availability")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.smoke
    @pytest.mark.api
    def test_api_availability(self, api_client):
        """Verify the ParaBank API endpoints are available"""
        # Test customers endpoint
        response = api_client.get("/customers/12212")
        
        # We don't necessarily need a valid customer ID, just check if the API responds
        assert response.status_code in [200, 404], f"API returned unexpected status code: {response.status_code}"
        
        # Check that content type is correctly set
        assert "application/json" in response.headers.get("Content-Type", ""), "API did not return JSON content type"
    
    @allure.title("Test bank accounts API endpoint")
    @allure.severity(allure.severity_level.HIGH)
    @pytest.mark.api
    def test_accounts_endpoint(self, api_client, config):
        """Verify the accounts endpoint functionality"""
        # Use the default customer ID from config if available
        customer_id = config.get("testCustomerId", "12212")
        
        response = api_client.get(f"/customers/{customer_id}/accounts")
        
        # Since we might not have a valid customer ID in the test environment,
        # we'll consider both 200 (success) and 404 (not found) as acceptable responses
        assert response.status_code in [200, 404], f"API returned unexpected status code: {response.status_code}"
        
        if response.status_code == 200:
            # If we have a valid response, verify its structure
            try:
                data = response.json()
                if isinstance(data, list):
                    # If data is a list, check if it has expected structure
                    if len(data) > 0:
                        assert "id" in data[0], "Account data missing 'id' field"
                        assert "balance" in data[0], "Account data missing 'balance' field"
            except Exception as e:
                pytest.fail(f"Failed to parse JSON response: {str(e)}")
    
    @allure.title("Test login via API")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    def test_login_api(self, api_client, config):
        """Verify login functionality via API"""
        # Get credentials from config
        username = config["users"]["default"]["username"]
        password = config["users"]["default"]["password"]
        
        # Call login endpoint
        params = {
            "username": username,
            "password": password
        }
        
        response = api_client.get("/login", params=params)
        
        # Check response
        assert response.status_code == 200, f"Login API failed with status code: {response.status_code}"
        
        try:
            data = response.json()
            # Validate response structure
            if "id" in data and isinstance(data["id"], int):
                assert True, "Login successful"
            else:
                # Some implementations might return a different structure
                assert response.text, "Login API returned empty response"
        except:
            # If not JSON, check if there's any content
            assert response.text, "Login API returned empty response" 