import json
import logging
import requests
from typing import Dict, Any, Optional, Union
from requests.exceptions import RequestException
import allure

logger = logging.getLogger(__name__)

class APIHelpers:
    """
    Utility class for API interactions
    """
    
    def __init__(self, base_url: str, headers: Optional[Dict[str, str]] = None):
        """
        Initialize the API helper with base URL and optional headers
        
        Args:
            base_url: Base URL for API requests
            headers: Optional headers to include in all requests
        """
        self.base_url = base_url
        self.session = requests.Session()
        
        # Set default headers
        default_headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Merge default headers with provided headers
        if headers:
            default_headers.update(headers)
        
        self.session.headers.update(default_headers)
    
    def update_headers(self, headers: Dict[str, str]) -> None:
        """
        Update session headers
        
        Args:
            headers: Headers to update or add
        """
        self.session.headers.update(headers)
    
    def set_auth_token(self, token: str) -> None:
        """
        Set authentication token in headers
        
        Args:
            token: Authentication token
        """
        self.session.headers.update({"Authorization": f"Bearer {token}"})
    
    @allure.step("API GET: {endpoint}")
    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """
        Perform GET request
        
        Args:
            endpoint: API endpoint (will be appended to base_url)
            params: Optional query parameters
            headers: Optional additional headers
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        logger.info(f"Making GET request to {url}")
        
        try:
            response = self.session.get(url, params=params, headers=headers)
            self._log_response(response)
            return response
        except RequestException as e:
            logger.error(f"GET request to {url} failed: {str(e)}")
            raise
    
    @allure.step("API POST: {endpoint}")
    def post(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
             json_data: Optional[Dict[str, Any]] = None,
             params: Optional[Dict[str, Any]] = None,
             headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """
        Perform POST request
        
        Args:
            endpoint: API endpoint (will be appended to base_url)
            data: Optional form data
            json_data: Optional JSON data
            params: Optional query parameters
            headers: Optional additional headers
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        logger.info(f"Making POST request to {url}")
        
        try:
            response = self.session.post(url, data=data, json=json_data, 
                                        params=params, headers=headers)
            self._log_response(response)
            return response
        except RequestException as e:
            logger.error(f"POST request to {url} failed: {str(e)}")
            raise
    
    @allure.step("API PUT: {endpoint}")
    def put(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
            json_data: Optional[Dict[str, Any]] = None,
            params: Optional[Dict[str, Any]] = None,
            headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """
        Perform PUT request
        
        Args:
            endpoint: API endpoint (will be appended to base_url)
            data: Optional form data
            json_data: Optional JSON data
            params: Optional query parameters
            headers: Optional additional headers
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        logger.info(f"Making PUT request to {url}")
        
        try:
            response = self.session.put(url, data=data, json=json_data, 
                                       params=params, headers=headers)
            self._log_response(response)
            return response
        except RequestException as e:
            logger.error(f"PUT request to {url} failed: {str(e)}")
            raise
    
    @allure.step("API DELETE: {endpoint}")
    def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None,
               headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """
        Perform DELETE request
        
        Args:
            endpoint: API endpoint (will be appended to base_url)
            params: Optional query parameters
            headers: Optional additional headers
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        logger.info(f"Making DELETE request to {url}")
        
        try:
            response = self.session.delete(url, params=params, headers=headers)
            self._log_response(response)
            return response
        except RequestException as e:
            logger.error(f"DELETE request to {url} failed: {str(e)}")
            raise
    
    @allure.step("API PATCH: {endpoint}")
    def patch(self, endpoint: str, data: Optional[Dict[str, Any]] = None,
              json_data: Optional[Dict[str, Any]] = None,
              params: Optional[Dict[str, Any]] = None,
              headers: Optional[Dict[str, str]] = None) -> requests.Response:
        """
        Perform PATCH request
        
        Args:
            endpoint: API endpoint (will be appended to base_url)
            data: Optional form data
            json_data: Optional JSON data
            params: Optional query parameters
            headers: Optional additional headers
            
        Returns:
            Response object
        """
        url = f"{self.base_url}{endpoint}"
        logger.info(f"Making PATCH request to {url}")
        
        try:
            response = self.session.patch(url, data=data, json=json_data, 
                                         params=params, headers=headers)
            self._log_response(response)
            return response
        except RequestException as e:
            logger.error(f"PATCH request to {url} failed: {str(e)}")
            raise
    
    def _log_response(self, response: requests.Response) -> None:
        """
        Log response details and attach to Allure report
        
        Args:
            response: Response object to log
        """
        logger.info(f"Response status code: {response.status_code}")
        
        # Log headers
        header_str = "\n".join([f"{k}: {v}" for k, v in response.headers.items()])
        logger.debug(f"Response headers:\n{header_str}")
        
        # Try to parse and log JSON response
        try:
            if response.text:
                # Format the JSON for better readability
                formatted_json = json.dumps(response.json(), indent=2)
                logger.debug(f"Response body:\n{formatted_json}")
                
                # Attach to Allure report
                allure.attach(
                    formatted_json,
                    name=f"Response {response.status_code}",
                    attachment_type=allure.attachment_type.JSON
                )
            else:
                logger.debug("Response body is empty")
        except ValueError:
            # Not a JSON response
            if len(response.text) > 1000:
                logger.debug(f"Response body (truncated):\n{response.text[:1000]}...")
                allure.attach(
                    response.text[:1000] + "...",
                    name=f"Response {response.status_code} (truncated)",
                    attachment_type=allure.attachment_type.TEXT
                )
            else:
                logger.debug(f"Response body:\n{response.text}")
                if response.text:
                    allure.attach(
                        response.text,
                        name=f"Response {response.status_code}",
                        attachment_type=allure.attachment_type.TEXT
                    )
    
    @staticmethod
    def is_success(response: requests.Response) -> bool:
        """
        Check if response is successful (status code 2xx)
        
        Args:
            response: Response to check
            
        Returns:
            True if successful, False otherwise
        """
        return 200 <= response.status_code < 300 