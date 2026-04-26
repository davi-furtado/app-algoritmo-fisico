<div align="center">
  <h1>APP Algoritmo Físico</h1>

  <img src="https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB">
  <img src="https://img.shields.io/badge/vite-%23646CFF.svg?style=for-the-badge&logo=vite&logoColor=white">
  <img src="https://img.shields.io/badge/react_native-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB">
  <img src="https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E">
  <img src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi">
</div>

<p align="right">
Aplicativo que escaneia pseudocódigos em blocos (algoritmos físicos) a partir de imagens e retorna o código equivalente em <b>Python</b> junto com a <b>saída da execução</b>.
</p>

# Funcionalidades

- Captura de imagem pela câmera ou galeria
- Reconhecimento de marcadores **ArUco**
- Conversão do pseudocódigo para Python no próprio backend
- Execução do código gerado
- Retorno do código e da saída
- Indentação automática do pseudocódigo
- Indentação automática do Python gerado
- Visualização ampliada da imagem capturada

# Estrutura do Projeto

<details>
  <summary>Filetree</summary>

```
app-algoritmo-fisico/
│
├── backend/
│   ├── aruco_reader.py
│   ├── blocks.json
│   ├── conversor.py
│   ├── executor.py
│   ├── main.py
│   ├── mono_return.py
│   └── requirements.txt
│
├── blocks/
│   ├── arucos/
│   │   ├── ...
│   │   ├── 21_verdadeiro.png
│   │   ├── 22_falso.png
│   │   ├── 23_inicio.png
│   │   ├── 24_fim.png
│   │   ├── 25_mostre.png
│   │   ├── 26_vale.png
│   │   └── ...
│   │
│   ├── blocks.json
│   ├── blocks.pdf
│   ├── generator.py
│   ├── problems.pdf
│   └── requirements.txt
│
├── frontend/
│   ├── mobile/
│   │   ├── assets/
│   │   │   ├── images/
│   │   │   │   ├── adaptive-icon.png
│   │   │   │   ├── favicon.png
│   │   │   │   ├── icon.png
│   │   │   │   └── splash-icon.png
│   │   │   │
│   │   │   └── JetBrainsMonoNL-Bold.ttf
│   │   │
│   │   ├── components/
│   │   │   ├── CodeBox.jsx
│   │   │   ├── InsertPhotoBtn.jsx
│   │   │   └── SegmentedToggle.jsx
│   │   │
│   │   ├── .env
│   │   ├── app.json
│   │   ├── App.jsx
│   │   ├── index.js
│   │   ├── package-lock.json
│   │   ├── package.json
│   │   └── styles.js
│   │
│   └── web/
│       ├── public/
│       │   ├── favicon.svg
│       │   └── icons.svg
│       │
│       ├── src/
│       │   ├── components/
│       │   │   ├── CodeBox.jsx
│       │   │   ├── InsertPhotoBtn.jsx
│       │   │   └── SegmentedToggle.jsx
│       │   │
│       │   ├── .env
│       │   ├── App.jsx
│       │   ├── main.jsx
│       │   └── styles.css
│       │
│       ├── eslint.config.js
│       ├── index.html
│       ├── package-lock.json
│       ├── package.json
│       └── vite.config.js
│
├── tests/
│   ├── pics/
│   │   ├── img1.jpg
│   │   ├── img2.jpg
│   │   └── ...
│   │
│   ├── multiple_test.py
│   ├── requirements.txt
│   ├── results.json
│   └── test.py
│
├── .gitignore
├── README.md
├── run_all.py
└── set_envs.py
```

Filetree gerada com a biblioteca [`pyletree`](https://github.com/davi-furtado/pyletree)

</details>

## Front-end

O front-end é dividido em duas implementações: mobile e web.

### Mobile

Tecnologias utilizadas:

- React Native
- Expo
- JavaScript

Responsável pela interface do aplicativo móvel, incluindo:

- Captura ou seleção de imagens
- Envio da imagem ao backend
- Exibição do pseudocódigo reconhecido, Python gerado e saída da execução

### Web

Tecnologias utilizadas:

- React
- Vite
- JavaScript

Responsável pela interface web, oferecendo funcionalidades similares ao mobile:

- Seleção de imagens
- Envio da imagem ao backend
- Exibição do pseudocódigo reconhecido, Python gerado e saída da execução

## Back-end

Tecnologias utilizadas:

- Python
- FastAPI
- OpenCV (ArUco)

O backend é responsável por:

1. Detectar os marcadores ArUco na imagem
2. Reconstruir o pseudocódigo a partir dos marcadores
3. Converter o pseudocódigo em Python
4. Executar o código gerado
5. Retornar o resultado para o aplicativo

### Arquivos principais

#### `main.py`

API FastAPI que atua como ponto de entrada, responsável por:

- Receber a imagem enviada pelo aplicativo
- Orquestrar a detecção, conversão e execução chamando os módulos auxiliares
- Retornar os resultados processados

#### `aruco_reader.py`

Módulo dedicado à visão computacional com OpenCV. Responsável por:

- Detectar os marcadores ArUco na imagem
- Reconstruir o texto do pseudocódigo baseado nas posições espaciais dos idenficadores

#### `executor.py`

Ambiente isolado (via `multiprocessing`) projetado para:

- Executar o código Python gerado
- Prevenir loops infinitos ou tempo excessivo de execução através de um mecanismo de **timeout**
- Capturar e interceptar a saída simulando a saída padrão (stdout) e os erros da execução

#### `conversor.py`

Arquivo responsável por converter o pseudocódigo em Python.

#### `blocks.json`

Define o **mapeamento entre IDs dos marcadores ArUco e comandos do pseudocódigo**.

### Arquivos secundários

#### `mono_return.py`

API que tem um retorno único independente da imagem enviada. Pode ser usada para testar conectividade com o front-end sem processar imagens.

#### `requirements.txt`

Arquivo com todas as dependências usadas no back-end.

# Como rodar?

## Requisitos

- Python 3.8 ou superior
- Node.js 14 ou superior
- npm 6 ou superior

## Configurando o Back-end

1. Abra um terminal na pasta `backend`
2. Instale as dependências executando o comando:
   ```bash
   pip install -r requirements.txt
   ```
3. Inicie a API com o comando:
   ```bash
   python main.py
   ```
   ou
   ```bash
   uvicorn main:app --host 0.0.0.0
   ```

## Configurando o Front-end [Mobile]

1. Crie o arquivo `frontend/mobile/.env` e coloque o seu **IP local** na variável `IP` para que o aplicativo consiga comunicar com o backend localmente. Deve ficar assim:
   ```bash
   IP=w.x.y.x
   ```
2. Abra um terminal na pasta `frontend/mobile`
3. Instale as dependências executando:
   ```bash
   npm install
   ```
4. Inicie o projeto Expo:
   ```bash
   npx expo start --port 6000
   ```
5. Para rodar no celular, baixe o aplicativo **Expo Go** e escaneie o QR code exibido.

## Configurando o Front-end [Web]

1. Crie o arquivo `frontend/web/.env` e coloque o seu **IP local** na variável `IP` para que o aplicativo consiga comunicar com o backend localmente. Deve ficar assim:
   ```bash
   IP=w.x.y.x
   ```
2. Abra um terminal na pasta `frontend/web`
3. Instale as dependências executando:
   ```bash
   npm install
   ```
4. Inicie o servidor de desenvolvimento:
   ```bash
   npm run dev -- --host 0.0.0.0 --port 4000
   ```
5. Abra o navegador no endereço `http://localhost:4000` ou `http://<seu_ip>:4000`.

## Usando os scripts de automação

O arquivo `set_envs.py` automatiza a criação dos arquivos `.env` para o frontend mobile e o frontend web, preenchendo a variável `IP` com o endereço IP local da máquina.

Ele reescreve os arquivos:

- `frontend/mobile/.env`
- `frontend/web/.env`

O arquivo `run_all.py` inicia os três serviços do projeto automaticamente:

- `backend`
- `frontend/mobile`
- `frontend/web`

Ele tenta iniciar:

- `uvicorn` para o backend
- `expo start` para o app mobile
- `npm run dev` para o web

Para usar, execute o script na raiz do projeto:

```bash
python run_all.py
```

# Pasta de blocos físicos

O projeto possui uma pasta `blocks` com os materiais necessários para utilizar o sistema com **algoritmos físicos**.

## `blocks.pdf`

PDF contendo **todos os blocos de pseudocódigo prontos para impressão**.
Os blocos podem ser recortados e utilizados fisicamente para montar algoritmos.

## `problems.pdf`

PDF contendo **exercícios de lógica de programação**.

Os alunos podem resolver os problemas **montando algoritmos com os blocos físicos** e depois usar o aplicativo para verificar a solução.

## `blocks.json`

Arquivo que define o **mapeamento entre IDs de ArUco e palavras do pseudocódigo**.

Exemplo simplificado:

```json
{
  "21": "verdadeiro",
  "22": "falso",
  "23": "inicio",
  "24": "fim",
  "25": "mostre",
  "26": "vale"
}
```

Esse arquivo também existe no **backend**, onde é utilizado durante o reconhecimento dos blocos.

## `generator.py`

Script responsável por **gerar automaticamente os marcadores ArUco utilizados no projeto**.

Ele cria todas as imagens dentro da pasta `blocks/arucos`.

# Fluxo de funcionamento

1. O front-end envia uma imagem para o endpoint `/convert`
2. O backend usa **OpenCV ArUco** para detectar os marcadores
3. Os **IDs detectados são convertidos em palavras** usando `blocks.json`
4. O pseudocódigo gerado é enviado para `toPython()` (`conversor.py`)
5. O pseudocódigo é transformado em **código Python válido**
6. O backend executa o código usando `exec`
7. A API retorna: pseudocódigo reconhecido, código Python gerado e saída da execução

# Conversão de pseudocódigo

O arquivo `conversor.py` implementa um **parser simples baseado em tokens** responsável por:

- Interpretar palavras do pseudocódigo
- Gerar estruturas Python equivalentes
- Controlar níveis de indentação
- Converter expressões e operadores

## Estruturas suportadas

### Condicionais

```
se
senao
senao se
fim se
```

### Repetição

```
repita
fim repita
enquanto
fim enquanto
```

### Saída

```
mostre _____
```

### Variáveis

```
_____ vale __
```

### Operadores e Valores

- **Operadores Matemáticos**: `+`, `-`, `*`, `/`
- **Operadores Relacionais**: `==`, `!=`, `<`, `>`, `<=`, `>=`
- **Valores Lógicos**: `verdadeiro` e `falso`
- **Valores e Variáveis Pré-definidas**: Números de `0` a `20`, e as variáveis `quantidade`, `valor`, `valor1`, `valor2`, `amigos`, `resto` e `resultado`.

## Indentação automática

O conversor implementa um sistema de **controle de níveis de bloco**, permitindo:

- Indentação correta do pseudocódigo
- Geração de Python com indentação válida

O projeto utiliza:

- 2 espaços para pseudocódigo
- 4 espaços para Python

Isso garante que o código gerado seja **executável imediatamente**.

# Pasta de testes

A pasta `tests` contém utilitários projetados para validar e debugar o back-end (em específico a API de conversão de imagens) rapidamente, sem a necessidade de rodar o front-end simultaneamente. O ambiente de testes possui seu próprio arquivo `requirements.txt` e uma subpasta `fotos/` com imagens de amostra para realizar testes pré-configurados.

## `test.py`

Script simples onde o usuário informa o caminho local de uma imagem por meio da entrada padrão do terminal. O script envia a imagem para o endpoint `/convert` local (porta `8000`) e imprime o JSON retornado pela API na tela.

## `multiple_test.py`

Script iterativo útil para processar e debugar um lote de imagens em sequência. Ele varre uma lista de caminhos de imagens (na variável iterável `paths`), as envia uma por vez para a API e compila os resultados (erros, pseudocódigo gerado e saídas em Python) num arquivo unificado independente chamado `results.json` na própria pasta.

# Exemplo de retorno da API

```json
{
  "path": "pics/img2.jpg",
  "output": "10",
  "pseudocode": "inicio\n  valor vale 10\n  valor1 vale 5\n  se valor > valor1\n    mostre valor\n  senao\n    mostre valor1\n  fim se\nfim",
  "python": "valor = 10\nvalor1 = 5\nif valor > valor1:\n    print(valor)\nelse:\n    print(valor1)"
}
```
