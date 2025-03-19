import json

def guardar_json(diccionario, nombre_archivo):
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        json.dump(diccionario, archivo, ensure_ascii=False, indent=4)