from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import easyocr, cv2, tempfile, subprocess
from os import remove
from uvicorn import run

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

reader = easyocr.Reader(['pt'], gpu=False)

def organizar_linhas(results):
    if not results:
        return ''

    alturas = []
    for bbox, _, _ in results:
        altura = abs(bbox[3][1] - bbox[0][1])
        alturas.append(altura)

    y_threshold = int(sum(alturas) / len(alturas) * 0.6)

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
    ext = path.splitext(file.filename)[1].lower()]:
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as temp_img:
        temp_path = temp_img.name
        temp_img.write(await file.read())

    img = cv2.imread(temp_path)

    if img is None:
        remove(temp_path)
        return {'erro': 'Imagem inválida ou corrompida.'}

    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(temp_path, gray)
        results = reader.readtext(temp_path)
    except Exception as e:
        remove(temp_path)
        return {'erro': f'Erro ao processar a imagem: {str(e)}'}

    pseudocodigo = organizar_linhas(results)

    prompt = f'''
Converta o pseudocódigo abaixo para Python válido.
Retorne SOMENTE o código Python.
Caso o pseudocódigo seja ambíguo, faça as melhores suposições para criar um código funcional.
Caso haja erros de sintaxe no pseudocódigo, corrija-os na conversão.

Pseudocódigo:
{pseudocodigo}
'''
    try:
        proc = subprocess.run(
            ['ollama', 'run', 'phi3'],
            input=prompt,
            text=True,
            capture_output=True
        )
    except Exception as e:
        remove(temp_path)
        return {'erro': f'Erro ao executar o modelo: {str(e)}'}

    python_code = proc.stdout.strip()

    with open('code.py', 'w', encoding='utf-8') as f:
        f.write(python_code)

    exec_proc = subprocess.run(
        ['python', 'code.py'],
        capture_output=True,
        text=True
    )

    remove(temp_path)
    remove('code.py')

    return {
        'pseudocodigo': pseudocodigo,
        'python': python_code,
        'saida': exec_proc.stdout
    }

run(app, host='0.0.0.0')