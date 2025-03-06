from azure.identity import DefaultAzureCredential
import requests
import urllib.parse
import time
from .auth import Auth

class Client:
    def __init__(self):
        self.auth = Auth()
        self.retryCount = 3
        self.success_list = [200, 202]
        self.scope = 'https://analysis.windows.net/powerbi/api/.default'
            

    def __get_token(self):
        return self.auth.get_token(self.scope)
    
    def __get_headers(self, additional_headers: dict = None):
        headers = {
            "Authorization":"Bearer " + self.__get_token(),
            "Content-Type": "application/json"
            }
        if additional_headers is not None:
            headers = headers | additional_headers
        return headers
    
    def get(self, relative_uri: str, additional_headers: dict = None):
        result = None
        for attempt in range(1, self.retryCount + 1):
            if attempt > 1:
                print(f"Retrying attempt {attempt}.")
                time.sleep(attempt ** 2)
            uri = urllib.parse.urljoin(self.get_api_root(), relative_uri)
            try:
                response = requests.get(uri, headers=self.__get_headers(additional_headers))
                result = self.__process_response(response, uri, attempt)
            except Exception as e:
                result = {"error": f'Error connecting to {uri}. {str(e)}'}
            
            if 'error' not in result:
                return result
        
        if 'error' in result:
            print(result.error)

        return result
    
    def post(self, relative_uri: str, data, additional_headers: dict = None):
        result = None
        for attempt in range(1, self.retryCount + 1):
            if attempt > 1:
                print(f"Retrying attempt {attempt}.")
                time.sleep(attempt ** 2)
            uri = urllib.parse.urljoin(self.get_api_root(), relative_uri)
            try:
                response = requests.post(uri, headers=self.__get_headers(additional_headers), data=data)
                result = self.__process_response(response, uri, attempt)
            except:
                result = {"error": f'Error connecting to {uri}.'}

            if 'error' not in result:
                return result
        
        if 'error' in result:
            print(result.error)

        return result

    def __process_response(self, response, uri: str, attempt: int):
            if response.status_code in self.success_list:
                return response.json()
            
            retry_can_help = False
            if response.status_code == 429:
                print(f"Rate limiting encountered during attempt {attempt}.")
                if response.headers.get('Retry-After', None) is None:
                    waitTime = attempt ** 3 * 5
                else:
                    waitTime = int(response.headers['Retry-After'])
                print(f"Retrying in {waitTime}s. This is expected behavior for larger tenants.")
                retry_can_help = True
                time.sleep(waitTime)
            
            if response.status_code == 403:
                return {'error': f'No access to {uri}.'}
            
            if response.status_code == 404:
                return {'error': f'No object found at {uri}. Check access.'}
            
            if response.status_code == 500:
                retry_can_help = True
            
            error = f"Client error: {response.status_code} {response.text}. {uri}"
            return {'error': error, 'retry_can_help': retry_can_help}
    
    def get_api_root(self) -> str:
        return 'https://api.powerbi.com/'