import requests

url = "https://svs-data-collection-e14762fe7642.herokuapp.com/pull_data"

payload = {}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload, allow_redirects=False)

print(response.text)
