from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import cv2, cv2.aruco as aruco
import json, tempfile
from os import remove, path
import io, sys
from conversor import toPython

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

with open('blocos.json', encoding='utf-8') as f:
    blocos = json.load(f)

dictionary = aruco.getPredefinedDictionary(aruco.DICT_5X5_100)
detector = aruco.ArucoDetector(dictionary)

def ler_arucos(img):
    corners, ids, _ = detector.detectMarkers(img)
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

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_img:
        temp_path = temp_img.name
        temp_img.write(await file.read())

    img = cv2.imread(temp_path)
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

    stdout_backup = sys.stdout
    sys.stdout = io.StringIO()
    try:
        exec(python_code, {})
        saida = sys.stdout.getvalue()
    except Exception as e:
        return {'erro': f'Erro ao executar o código: {e}'}
    sys.stdout = stdout_backup

    remove(temp_path)

    return {
        'pseudocodigo': pseudocodigo,
        'python': python_code,
        'saida': saida
    }