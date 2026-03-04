from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import easyocr
import cv2
import tempfile
import subprocess
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

reader = easyocr.Reader(['pt'], gpu=False)

def organizar_linhas(results, y_threshold=25):
    linhas = []

    for bbox, txt, _ in results:
        y = sum(p[1] for p in bbox) / 4

        for linha in linhas:
            if abs(linha['y'] - y) < y_threshold:
                linha['itens'].append((bbox, txt))
                break
        else:
            linhas.append({'y': y, 'itens': [(bbox, txt)]})

    linhas.sort(key=lambda l: l['y'])

    texto_final = []
    for linha in linhas:
        linha['itens'].sort(key=lambda t: t[0][0][0])
        texto_final.append(' '.join(t[1] for t in linha['itens']))

    return '\n'.join(texto_final)

@app.post('/convert')
async def convert(file: UploadFile = File(...)):
    temp_img = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
    temp_img.write(await file.read())
    temp_img.close()

    img = cv2.imread(temp_img.name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(temp_img.name, gray)

    results = reader.readtext(temp_img.name)
    pseudocodigo = organizar_linhas(results)

    prompt = f'''
Converta o pseudocódigo abaixo para Python válido.
Retorne SOMENTE o código Python.

Pseudocódigo:
{pseudocodigo}
'''

    proc = subprocess.run(
        ['ollama', 'run', 'phi3'],
        input=prompt,
        text=True,
        capture_output=True
    )

    python_code = proc.stdout.strip()

    with open('code.py', 'w', encoding='utf-8') as f:
        f.write(python_code)

    exec_proc = subprocess.run(
        ['python', 'code.py'],
        capture_output=True,
        text=True
    )

    os.unlink(temp_img.name)
    os.unlink('code.py')

    return {
        'python': python_code,
        'saida': exec_proc.stdout or exec_proc.stderr
    }
