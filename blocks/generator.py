import cv2
import cv2.aruco as aruco
import os
import json

with open('blocks.json') as f:
    blocks = json.load(f)

directory = 'arucos'
os.makedirs(directory, exist_ok=True)
dictionary = aruco.getPredefinedDictionary(aruco.DICT_5X5_100)

for id_str, text in blocks.items():
    marker_id = int(id_str)

    marker = aruco.generateImageMarker(dictionary, marker_id, 300)

    marker = cv2.copyMakeBorder(
        marker,
        30, 30, 30, 30,
        cv2.BORDER_CONSTANT,
        value=255
    )

    name = text.replace(' ', '_')
    match name:
        case '+': name = 'mais'
        case '-': name = 'menos'
        case '*': name = 'vezes'
        case '/': name = 'dividido'
        case '==': name = 'igual'
        case '!=': name = 'diferente'
        case '<': name = 'menor'
        case '>': name = 'maior'
        case '<=': name = 'menor_igual'
        case '>=': name = 'maior_igual'

    cv2.imwrite(f'{directory}/{marker_id}_{name}.png', marker)