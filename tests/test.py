from requests import post

img = input()
url = 'http://localhost:8000/convert'

with open(img, 'rb') as file:
    files = {'file': file}
    response = post(url, files=files)

result = response.json()
with open('result.json', 'w') as file:
    dump(result, file, indent=2)