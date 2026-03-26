import os
from requests import post
from json import dump

url = 'http://localhost:8000/convert'
paths = []

results = {}
index = 1
for path in paths:
    if not os.path.exists(path): continue

    with open(path, 'rb') as entry:
        files = {'file': entry}
        response = post(url, files=files)
        if response.status_code != 200: continue

    response = response.json()
    if not response: continue

    results[f'test_{index}'] = {'path': path} | response
    with open('results.json', 'w') as file:
        dump(result, file, indent=2)

    index += 1