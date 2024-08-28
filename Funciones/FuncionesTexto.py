import json
import os 

def leer_archivos_txt(carpeta):
    contenido_completo = ""
    for archivo in os.listdir(carpeta):
        if archivo.endswith(".txt"):
            with open(os.path.join(carpeta, archivo), 'r', encoding='utf-8') as f:
                contenido_completo += f.read() + "\n"  # Agregar un salto de línea entre archivos
    return contenido_completo

def exportar_a_txt(contenido, archivo_salida):
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write(contenido)

def leer_archivo(nombre_archivo):
    with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
        contenido = archivo.read()
    return contenido

def separar_parrafos(contenido):
    return [parrafo.strip() for parrafo in contenido.split("---***") if parrafo.strip()]

def crear_diccionario_indexado(parrafos):
    return {str(i+1): parrafo for i, parrafo in enumerate(parrafos)}

def guardar_json(diccionario, nombre_archivo):
    with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
        json.dump(diccionario, archivo, ensure_ascii=False, indent=2)