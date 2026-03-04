from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run
from os import remove
import cv2, tempfile

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.post('/convert')
async def convert(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as temp_img:
        temp_path = temp_img.name
        temp_img.write(await file.read())

    img = cv2.imread(temp_path)

    if img is None:
        remove(temp_path)
        return {'erro': 'Imagem inválida ou corrompida.'}
    
    remove(temp_path)

    return {
        'pseudocodigo': 'INÍCIO\nSE 4 > 2 ENTÃO\n  IMPRIMA 0\nFIM SE',
        'python': 'if 4 > 2:\n    print(0)',
        'saida': '0'
    }

run(app, host='0.0.0.0')