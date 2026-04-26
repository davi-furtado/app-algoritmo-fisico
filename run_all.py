from subprocess import Popen
import socket as sc

s = sc.socket(sc.AF_INET, sc.SOCK_DGRAM)
s.connect(('10.255.255.255', 1))
ip = s.getsockname()[0]
s.close()
print(ip)

with open('frontend/mobile/.env', 'w') as f:
    f.write(f'IP={ip}')

with open('frontend/web/.env', 'w') as f:
    f.write(f'IP={ip}')

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