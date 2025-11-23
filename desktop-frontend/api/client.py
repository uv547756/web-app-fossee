"""
API Client for communicating with Django backend
Handles JWT authentication, token refresh, and all API endpoints
"""
import requests
from typing import Optional, Dict, List

class APIClient:
    """Client for Django REST API with JWT authentication"""
    
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.session = requests.Session()
        self.session.timeout = 30
        
    def set_tokens(self, access: str, refresh: str):
        """Set authentication tokens and update session headers"""
        self.access_token = access
        self.refresh_token = refresh
        self.session.headers.update({
            'Authorization': f'Bearer {access}'
        })
        
    def clear_tokens(self):
        """Clear authentication tokens"""
        self.access_token = None
        self.refresh_token = None
        if 'Authorization' in self.session.headers:
            del self.session.headers['Authorization']
        
    def login(self, username: str, password: str) -> Dict:
        """
        Login and get JWT tokens
        
        Args:
            username: Django username
            password: Django password
            
        Returns:
            Dict with 'access' and 'refresh' tokens
            
        Raises:
            Exception: If login fails
        """
        url = f"{self.base_url}/api/token/"
        try:
            response = requests.post(url, json={
                'username': username,
                'password': password
            }, timeout=10)
            response.raise_for_status()
            data = response.json()
            self.set_tokens(data['access'], data['refresh'])
            return data
        except requests.exceptions.RequestException as e:
            if hasattr(e, 'response') and e.response is not None:
                try:
                    error_data = e.response.json()
                    error_msg = error_data.get('detail', str(e))
                except:
                    error_msg = f"HTTP {e.response.status_code}"
            else:
                error_msg = str(e)
            raise Exception(f"Login failed: {error_msg}")
        
    def refresh_access_token(self) -> str:
        """
        Refresh access token using refresh token
        
        Returns:
            New access token
            
        Raises:
            Exception: If refresh fails
        """
        if not self.refresh_token:
            raise Exception("No refresh token available")
            
        url = f"{self.base_url}/api/token/refresh/"
        try:
            response = requests.post(url, json={
                'refresh': self.refresh_token
            }, timeout=10)
            response.raise_for_status()
            data = response.json()
            self.access_token = data['access']
            self.session.headers.update({
                'Authorization': f'Bearer {data["access"]}'
            })
            return data['access']
        except requests.exceptions.RequestException:
            raise Exception("Token refresh failed")
        
    def _request_with_retry(self, method: str, url: str, **kwargs):
        """
        Make HTTP request with automatic token refresh on 401
        
        Args:
            method: HTTP method (GET, POST, etc.)
            url: Request URL
            **kwargs: Additional request parameters
            
        Returns:
            Response object
            
        Raises:
            Exception: If request fails
        """
        try:
            response = self.session.request(method, url, **kwargs)
            
            # Handle 401 Unauthorized - try to refresh token
            if response.status_code == 401 and self.refresh_token:
                try:
                    self.refresh_access_token()
                    # Retry original request with new token
                    response = self.session.request(method, url, **kwargs)
                except Exception:
                    raise Exception("Authentication expired. Please login again.")
            
            response.raise_for_status()
            return response
            
        except requests.exceptions.Timeout:
            raise Exception("Request timed out. Please check your connection.")
        except requests.exceptions.ConnectionError:
            raise Exception("Cannot connect to server. Is the backend running?")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise Exception("Authentication failed. Please login again.")
            elif e.response.status_code == 400:
                try:
                    error_data = e.response.json()
                    error_msg = str(error_data)
                except:
                    error_msg = "Bad request"
                raise Exception(f"Request error: {error_msg}")
            else:
                raise Exception(f"HTTP {e.response.status_code}: {str(e)}")
        except requests.exceptions.RequestException as e:
            raise Exception(f"Request failed: {str(e)}")
            
    def upload_csv(self, file_path: str) -> Dict:
        """
        Upload CSV file to backend
        
        Args:
            file_path: Absolute path to CSV file
            
        Returns:
            Dict with dataset information including statistics
            
        Raises:
            Exception: If upload fails
        """
        url = f"{self.base_url}/upload/"
        try:
            with open(file_path, 'rb') as f:
                files = {'file': (file_path.split('/')[-1], f, 'text/csv')}
                response = self._request_with_retry('POST', url, files=files)
                return response.json()
        except FileNotFoundError:
            raise Exception(f"File not found: {file_path}")
        except PermissionError:
            raise Exception(f"Permission denied: {file_path}")
            
    def get_history(self) -> List[Dict]:
        """
        Get upload history (last 5 datasets)
        
        Returns:
            List of dataset dictionaries
            
        Raises:
            Exception: If request fails
        """
        url = f"{self.base_url}/history/"
        response = self._request_with_retry('GET', url)
        return response.json()
        
    def download_report(self, dataset_id: int, save_path: str):
        """
        Download PDF report for a dataset
        
        Args:
            dataset_id: ID of the dataset
            save_path: Path where PDF should be saved
            
        Raises:
            Exception: If download fails
        """
        url = f"{self.base_url}/datasets/{dataset_id}/report.pdf"
        response = self._request_with_retry('GET', url)
        
        try:
            with open(save_path, 'wb') as f:
                f.write(response.content)
        except PermissionError:
            raise Exception(f"Permission denied: {save_path}")
        except Exception as e:
            raise Exception(f"Failed to save file: {str(e)}")