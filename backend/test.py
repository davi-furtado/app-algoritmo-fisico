from requests import post

img = input()
url = 'http://localhost:8000/convert'

with open(img, 'rb') as file:
    files = {'file': file}
    response = post(url, files=files)

output = response.json()
print(output)