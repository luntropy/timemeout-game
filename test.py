import requests

BASE = 'http://127.0.0.1:5000/'

response = requests.post(BASE + 'room/1/3x2/30')
print(response.json())
response = requests.get(BASE + 'room/1')
print(response.json())
