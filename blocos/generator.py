import cv2
import cv2.aruco as aruco
import os
import json

with open("blocos.json", "r", encoding="utf-8") as f:
    blocos = json.load(f)

os.makedirs("arucos", exist_ok=True)
dictionary = aruco.getPredefinedDictionary(aruco.DICT_5X5_100)

for id_str, texto in blocos.items():
    marker_id = int(id_str)

    marker = aruco.generateImageMarker(dictionary, marker_id, 300)

    marker = cv2.copyMakeBorder(
        marker,
        60, 60, 60, 60,
        cv2.BORDER_CONSTANT,
        value=255
    )

    nome = texto
    match nome:
        case "+": nome = "mais"
        case "-": nome = "menos"
        case "*": nome = "vezes"
        case "/": nome = "dividido"
        case '=': nome = "igual"
        case "!=": nome = "diferente"
        case "<": nome = "menor"
        case ">": nome = "maior"
        case "<=": nome = "menor_igual"
        case ">=": nome = "maior_igual"

    cv2.imwrite(f"arucos/{marker_id}_{nome}.png", marker)