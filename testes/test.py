from requests import post

img = input()
url = 'http://localhost:8000/convert'

with open(img, 'rb') as file:
    files = {'file': file}
    response = post(url, files=files)

saida = response.json()
print(saida)
with open('saida.py', 'w') as file: file.write(saida['python'])
with open('saida.json', 'w') as file:
    from json import dump
    dump(file, saida)