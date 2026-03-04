import requests as rq

img = 'path'
url = 'http://localhost:8000/convert'

with open(img, 'rb') as file:
    files = {'file': file}
    response = rq.post(url, files=files)
print(response.json())