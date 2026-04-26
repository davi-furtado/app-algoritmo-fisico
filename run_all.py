from subprocess import Popen
import socket as sc

ip = sc.gethostbyname(sc.gethostname())

envs = ['backend/', 'frontend/mobile/', 'frontend/web/']
for env in envs:
    f = open(env + '.env', 'w')
    f.write(f'IP={ip}')
    f.close()

try:
    Popen('uvicorn main:app --host 0.0.0.0', cwd='backend')
except:
    Popen(
        'pip install -r requirements.txt && uvicorn main:app --host 0.0.0.0',
        cwd='backend',
        shell=True
    )

try:
    Popen('npx expo start --port 6000', cwd='frontend/mobile')
except:
    Popen(
        'npm install && npx expo start --port 6000',
        cwd='frontend/mobile',
        shell=True
    )

try:
    Popen('npm run dev -- --host 0.0.0.0 --port 4000', cwd='frontend/web')
except:
    Popen(
        'npm install && npm run dev -- --host 0.0.0.0 --port 4000',
        cwd='frontend/web',
        shell=True
    )