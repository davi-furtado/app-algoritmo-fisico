from os import listdir
from requests import post
from json import dump

paths = listdir('fotos')
url = 'http://localhost:8000/convert'

results = []

for path in paths:
    with open('fotos/'+path, 'rb') as entry:
        files = {'file': entry}
        response = post(url, files=files)

    if response.status_code != 200: continue

    data = response.json()
    if not data: continue

    results.append({'path': path} | data)

with open('results.json', 'w') as file:
    dump(results, file, indent=2)