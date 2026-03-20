from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from cv2 import imread, cvtColor, COLOR_BGR2GRAY
from cv2.aruco import (
    getPredefinedDictionary,
    DICT_5X5_100,
    DetectorParameters,
    ArucoDetector
)
from json import load
from tempfile import NamedTemporaryFile
from io import StringIO
from sys import stdout
from os import remove, path
from uvicorn import run
from conversor import indentPseudo, toPython

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

with open('blocos.json') as f:
    blocos = load(f)

dictionary = getPredefinedDictionary(DICT_5X5_100)

parameters = DetectorParameters()
parameters.adaptiveThreshWinSizeMin = 3
parameters.adaptiveThreshWinSizeMax = 23
parameters.adaptiveThreshWinSizeStep = 10
parameters.adaptiveThreshConstant = 7

detector = ArucoDetector(dictionary, parameters)


def ler_arucos(img):
    gray = cvtColor(img, COLOR_BGR2GRAY)
    corners, ids, _ = detector.detectMarkers(gray)
    if ids is None:
        return None

    dados = []
    for i, marker_id in enumerate(ids):
        c = corners[i][0]
        x = int(c[:, 0].mean())
        y = int(c[:, 1].mean())
        dados.append((x, y, marker_id[0]))

    dados.sort(key=lambda t: (t[1], t[0]))
    linhas = []
    y_threshold = 40
    for x, y, marker_id in dados:
        for linha in linhas:
            if abs(linha['y'] - y) < y_threshold:
                linha['itens'].append((x, marker_id))
                break
        else:
            linhas.append({'y': y, 'itens': [(x, marker_id)]})

    linhas.sort(key=lambda l: l['y'])
    texto_final = []
    for linha in linhas:
        linha['itens'].sort(key=lambda t: t[0])
        palavras = []
        for x, marker_id in linha['itens']:
            chave = str(marker_id)
            if chave in blocos:
                palavras.append(blocos[chave])
        texto_final.append(' '.join(palavras))
    return '\n'.join(texto_final)


@app.post('/convert')
async def convert(file: UploadFile = File(...)):
    ext = path.splitext(file.filename)[1].lower()

    with NamedTemporaryFile(delete=False, suffix=ext) as temp_img:
        temp_path = temp_img.name
        temp_img.write(await file.read())

    img = imread(temp_path)
    if img is None:
        remove(temp_path)
        return {'erro': 'Imagem inválida ou corrompida.'}

    try:
        pseudocodigo = ler_arucos(img)
        if pseudocodigo is None or pseudocodigo.strip() == '':
            remove(temp_path)
            return {'erro': 'Nenhum código detectado na imagem.'}
    except Exception as e:
        remove(temp_path)
        return {'erro': f'Erro ao processar a imagem: {str(e)}'}

    python_code = toPython(pseudocodigo)

    stdout_backup = stdout
    sys_stdout = StringIO()
    import sys
    sys.stdout = sys_stdout

    try:
        exec(python_code, {})
        saida = sys_stdout.getvalue().strip()
    except Exception as e:
        return {'erro': f'Erro ao executar o código: {e}'}

    sys.stdout = stdout_backup

    remove(temp_path)

    return {
        'saida': saida,
        'pseudocodigo': indentPseudo(pseudocodigo),
        'python': python_code
    }


run(app, host='0.0.0.0')