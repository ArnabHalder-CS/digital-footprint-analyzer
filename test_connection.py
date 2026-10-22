import requests

url = "https://github.com"

response = requests.get(url)

print("Status Code:", response.status_code)