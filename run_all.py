from subprocess import Popen
import socket as sc

try:
    Popen('uvicorn main:app --host 0.0.0.0', cwd='backend')
    if sc.socket().connect_ex(('localhost', 8000)) is None: raise
except:
    Popen(
        'pip install -r requirements.txt && uvicorn main:app --host 0.0.0.0',
        cwd='backend',
        shell=True
    )

try:
    Popen('npx expo start --port 6000', cwd='frontend/mobile')
    if sc.socket().connect_ex(('localhost', 6000)) is None: raise
except:
    Popen(
        'npm install && npx expo start --port 6000',
        cwd='frontend/mobile',
        shell=True
    )

try:
    Popen('npm run dev -- --host 0.0.0.0 --port 4000', cwd='frontend/web')
    if sc.socket().connect_ex(('localhost', 4000)) is None: raise
except:
    Popen(
        'npm install && npm run dev -- --host 0.0.0.0 --port 4000',
        cwd='frontend/web',
        shell=True
    )