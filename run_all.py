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

Popen('uvicorn main:app --host 0.0.0.0', cwd='backend')

Popen('npx expo start --port 6000', cwd='frontend/mobile')

Popen('npm run dev -- --host 0.0.0.0 --port 4000', cwd='frontend/web')