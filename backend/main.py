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


def read_arucos(img):
    gray = cvtColor(img, COLOR_BGR2GRAY)
    corners, ids, _ = detector.detectMarkers(gray)
    if ids is None:
        return None

    data = []
    for i, marker_id in enumerate(ids):
        c = corners[i][0]
        x = int(c[:, 0].mean())
        y = int(c[:, 1].mean())
        data.append((x, y, marker_id[0]))

    data.sort(key=lambda t: (t[1], t[0]))
    lines = []
    y_threshold = 40
    for x, y, marker_id in data:
        for line in lines:
            if abs(line['y'] - y) < y_threshold:
                line['items'].append((x, marker_id))
                break
        else:
            lines.append({'y': y, 'items': [(x, marker_id)]})

    lines.sort(key=lambda l: l['y'])
    final_text = []
    for line in lines:
        line['items'].sort(key=lambda t: t[0])
        words = []
        for x, marker_id in line['items']:
            key = str(marker_id)
            if key in blocos:
                words.append(blocos[key])
        final_text.append(' '.join(words))
    return '\n'.join(final_text)


@app.post('/convert')
async def convert(file: UploadFile = File(...)):
    ext = path.splitext(file.filename)[1].lower()

    with NamedTemporaryFile(delete=False, suffix=ext) as temp_img:
        temp_path = temp_img.name
        temp_img.write(await file.read())

    img = imread(temp_path)
    if img is None:
        remove(temp_path)
        return {'error': 'Imagem inválida ou corrompida.'}

    try:
        pseudocode = read_arucos(img)
        if pseudocode is None or pseudocode.strip() == '':
            remove(temp_path)
            return {'error': 'Nenhum código detectado na imagem.'}
    except Exception as e:
        remove(temp_path)
        return {'error': f'Erro ao processar a imagem: {str(e)}'}

    python_code = toPython(pseudocode)

    stdout_backup = stdout
    sys_stdout = StringIO()
    import sys
    sys.stdout = sys_stdout

    try:
        exec(python_code, {})
        output = sys_stdout.getvalue().strip()
    except Exception as e:
        return {'error': f'Erro ao executar o código: {e}'}

    sys.stdout = stdout_backup

    remove(temp_path)

    return {
        'output': output,
        'pseudocode': indentPseudo(pseudocode),
        'python': python_code
    }


if __name__ == '__main__':
    from uvicorn import run
    run(app, host='0.0.0.0')