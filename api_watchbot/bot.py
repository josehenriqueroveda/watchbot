import os
import requests
from datetime import datetime, timedelta



API_LIST = [
    {"name": "IT Services API", "url": "http://10.80.11.69:8008/health"},
    {"name": "GLPI API", "url": "http://10.80.11.69:8008/v1/glpi/category"},
]

def check_api_status(api):
    try:
        response = requests.get(api["url"])
        if response.status_code == 200:
            return (200, "OK")
        else:
            return (response.status_code, response.text)
    except requests.exceptions.RequestException as e:
        return (500, str(e))



for api in API_LIST:
    status_code, message = check_api_status(api)
    print(f"\n{api['name']}: {status_code} - {message}")
