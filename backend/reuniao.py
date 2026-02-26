import easyocr
import cv2
import tempfile
import subprocess
import os
import uuid
from tkinter import Tk, filedialog

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

def selecionar_imagem():
    root = Tk()
    root.withdraw()              # Oculta a janela do Tkinter
    root.attributes('-topmost', True)

    caminho = filedialog.askopenfilename(
        title='Selecione uma imagem',
        filetypes=[
            ('Imagens', '*.png;*.jpg;*.jpeg;*.bmp;*.tif;*.tiff'),
            ('Todos os arquivos', '*.*'),
        ]
    )
    root.destroy()
    if caminho: return caminho
    else: exit()

print('Selecione a imagem contendo o pseudocódigo...')
caminho = selecionar_imagem()

if not caminho:
    print('Nenhuma imagem selecionada.')

print(f'\nImagem selecionada: {caminho}')

print('\nCarregando EasyOCR...')
reader = easyocr.Reader(['pt'], gpu=False)

print('Lendo e convertendo imagem...')
img = cv2.imread(caminho)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

temp_img = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
cv2.imwrite(temp_img.name, gray)
temp_img.close()

print('Executando OCR...')
results = reader.readtext(temp_img.name)
pseudocodigo = organizar_linhas(results)

print('\n------------------ PSEUDOCÓDIGO EXTRAÍDO ------------------')
print(pseudocodigo)
print('-----------------------------------------------------------\n')

prompt = f'''
Converta o pseudocódigo abaixo para Python válido.
Retorne SOMENTE o código Python.

Pseudocódigo:
{pseudocodigo}
'''

print('Convertendo pseudocódigo para Python via Ollama...')

proc = subprocess.run(
    ['ollama', 'run', 'phi3'],
    input=prompt,
    text=True,
    capture_output=True
)

python_code = proc.stdout.strip()
print('\n------------------ CÓDIGO PYTHON GERADO ------------------')
print(python_code)
print('-----------------------------------------------------------\n')

py_file = f'/backend/{uuid.uuid4()}.py'
with open(py_file, 'w', encoding='utf-8') as f:
    f.write(python_code)

print('Executando o código gerado...\n')
exec_proc = subprocess.run(
    ['python', py_file],
    capture_output=True,
    text=True
)

print('---------------------- SAÍDA ----------------------')
print(exec_proc.stdout or exec_proc.stderr)
print('--------------------------------------------------')

os.unlink(temp_img.name)
os.unlink(py_file)