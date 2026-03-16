<div align="center">
  <h1>APP Algoritmo Físico</h1>

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

```tree
.\app-algoritmo-fisico\
├── backend\
│   ├── auto_return.py
│   ├── blocos.json
│   ├── conversor.py
│   ├── main.py
│   ├── requirements.txt
│   └── test.py
├── blocos\
│   ├── arucos\
│   │   ├── 0_0.png
│   │   ├── 1_1.png
│   │   ├── ...
│   │   ├── 50_enquanto.png
│   │   └── 51_fim_enquanto.png
│   ├── blocos.json
│   ├── blocos.pdf
│   ├── generator.py
│   └── problemas.pdf
├── frontend\
│   ├── assets\
│   │   ├── images\
│   │   │   ├── adaptive-icon.png
│   │   │   ├── favicon.png
│   │   │   ├── icon.png
│   │   │   └── splash-icon.png
│   │   └── JetBrainsMonoNL-Bold.ttf
│   ├── components\
│   ├── app.json
│   ├── App.jsx
│   ├── index.js
│   ├── package-lock.json
│   ├── package.json
│   └── styles.js
├── .gitignore
└── README.md
```

## Front-end

Tecnologias utilizadas:

- React Native
- Expo
- JavaScript
- React Native WebView

Responsável pela:

- Interface do aplicativo
- Captura ou seleção de imagens
- Envio da imagem ao backend

O front-end também exibe:

- Pseudocódigo reconhecido
- Python gerado
- Saída da execução

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

API FastAPI responsável por:

- Receber a imagem enviada pelo aplicativo
- Detectar os ArUcos
- Reconstruir o pseudocódigo
- Executar o Python gerado

#### `conversor.py`

Arquivo responsável por converter o pseudocódigo em Python.

#### `blocos.json`

Define o **mapeamento entre IDs dos marcadores ArUco e comandos do pseudocódigo**.

### Arquivos secundários

#### `auto_return.py`

API que tem um retorno único independente da imagem enviada. Para testar o frontend.

#### `test.py` e `test.rest`

Arquivos feitos para testar o backend de forma rápida, sem precisar rodar o front.

#### `requirements.txt`

Arquivo com todas as bibliotecas usadas

# Como rodar?

1. Abra um terminal na pasta `backend`
2. Dê o conando `pip install -r requirements.txt`
3. Dê o comando `python main.py`
4. Vá no arquivo `App.jsx` e coloque o seu **ip** na constante `ip`
5. Abra um segundo terminal na pasta `frontend`
6. Dê o comando `npm install`
7. Dê o comando `npx expo start`
8. Caso queira rodar na web, clique no link indicado, senão baixe o app _Expo Go_ no seu celular e escaneie o QR code mostrado

# Pasta de blocos físicos

O projeto possui uma pasta `blocos` com os materiais necessários para utilizar o sistema com **algoritmos físicos**.

## `blocos.pdf`

PDF contendo **todos os blocos de pseudocódigo prontos para impressão**.
Os blocos podem ser recortados e utilizados fisicamente para montar algoritmos.

## `problemas.pdf`

PDF contendo **exercícios de lógica de programação**.

Os alunos podem resolver os problemas **montando algoritmos com os blocos físicos** e depois usar o aplicativo para verificar a solução.

## `blocos.json`

Arquivo que define o **mapeamento entre IDs de ArUco e palavras do pseudocódigo**.

Exemplo simplificado:

```json
{
  "0": "inicio",
  "1": "fim",
  "2": "mostre",
  "3": "se",
  "4": "senao",
  "5": "repita"
}
```

Esse arquivo também existe no **backend**, onde é utilizado durante o reconhecimento dos blocos.

## `generator.py`

Script responsável por **gerar automaticamente os marcadores ArUco utilizados no projeto**.

Ele cria todas as imagens dentro da pasta `blocos/codes`.

# Fluxo de funcionamento

1. O front-end envia uma imagem para o endpoint `/convert`
2. O backend usa **OpenCV ArUco** para detectar os marcadores
3. Os **IDs detectados são convertidos em palavras** usando `blocos.json`
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

## Indentação automática

O conversor implementa um sistema de **controle de níveis de bloco**, permitindo:

- Indentação correta do pseudocódigo
- Geração de Python com indentação válida

O projeto utiliza:

- 2 espaços para pseudocódigo
- 4 espaços para Python

Isso garante que o código gerado seja **executável imediatamente**.

# Exemplo de retorno da API

```json
{
  "pseudocodigo": "inicio\n  valor vale 10\n  valor1 vale 5\n  se valor > valor1\n    mostre valor\n  senao\n    mostre valor1\n  fim se\nfim",
  "python": "valor = 10\nvalor1 = 5\nif valor > valor1:\n    print(valor)\nelse:\n    print(valor1)",
  "saida": "10"
}
```
