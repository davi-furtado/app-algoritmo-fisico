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

## Funcionalidades

- Captura de imagem pela câmera ou galeria
- Reconhecimento de marcadores **ArUco**
- Conversão do pseudocódigo para Python no próprio backend
- Execução do código gerado
- Retorno do código e da saída

## Estrutura do Projeto

### Front-end

- React Native
- Expo
- JavaScript

Responsável pela interface, captura/seleção da imagem e envio ao back-end.

### Back-end

- Python
- FastAPI
- OpenCV (ArUco)

O backend é dividido em duas responsabilidades:

- Leitura dos ArUcos da imagem
- Conversão do pseudocódigo para Python

#### Arquivos principais

- `main.py` → API FastAPI que recebe a imagem, detecta os ArUcos e executa o código
- `conversor.py` → responsável por converter o pseudocódigo em Python

#### Fluxo

1. O front-end envia uma imagem para o endpoint `/convert`
2. O backend usa **OpenCV ArUco** para detectar os marcadores
3. Os **IDs detectados são convertidos em palavras** usando `blocos.json`
4. O pseudocódigo gerado é enviado para `toPython()` (`conversor.py`)
5. O pseudocódigo é transformado em **código Python válido**
6. O backend executa o código usando `exec`
7. A API retorna:

- Pseudocódigo reconhecido
- Código Python gerado
- Saída da execução

#### Exemplo de retorno da API

```json
{
  "pseudocodigo": "inicio\nvalor vale 10\nvalor1 vale 5\nse valor > valor1\nmostre valor\nsenao\nmostre valor1\nfim se\nfim",
  "python": "valor = 10\nvalor1 = 5\nif valor > valor1:\n    print(valor)\nelse:\n    print(valor1)",
  "saida": "10\n"
}
```
