from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import cv2, tempfile
from os import remove, path
from uvicorn import run

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
    ext = path.splitext(file.filename)[1].lower()
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_img:
        temp_path = temp_img.name
        temp_img.write(await file.read())

    img = cv2.imread(temp_path)

    remove(temp_path)
    if img is None:
        return {'erro': 'Imagem inválida ou corrompida.'}
    
    return {
        'pseudocodigo': 'inicio\n  se 4 > 2\n    mostre 0\n  fim se\nfim',
        'python': 'if 4 > 2:\n    print(0)',
        'saida': '0'
    }

run(app, host='0.0.0.0')