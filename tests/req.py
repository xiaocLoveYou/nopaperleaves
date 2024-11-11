import requests
import json


url = "http://10.33.2.49:5000/api/attendance/attendancelist"
# credentials = {
#     "username": "信息系",
#     "password": "admin4"
# }

try:
    response = requests.get(url, headers={"Content-Type": "application/json", "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyNDY4LCJ1c2VyX25hbWUiOiJcdTRmZTFcdTYwNmZcdTdjZmIiLCJyb2xlIjoibWFuYWdlciIsImRlcGFydG1lbnRfaWQiOjQsImNsYXNzX2lkIjpudWxsLCJleHAiOjE3MzE2MzA5Njl9.FwBE3gHXSK0cEydHHpLpZ0CgVlzNzrdOxZbZUgiQdNs"})
    response.raise_for_status()
    result = response.json()
    print(result)
except requests.exceptions.RequestException as e:
    print("Error occurred:", e)
except ValueError:
    print("Response is not in JSON format:", response.text)
