import ttkbootstrap as tb
from ttkbootstrap.constants import *
import os
import json
import numpy as np
from Funciones.FuncionesTexto import leer_archivos_txt, separar_parrafos, crear_diccionario_indexado, guardar_json
from Funciones.Embeding import *
import faiss
from Funciones.Respuestas import get_answer
from tkinter import filedialog
import tkinter as tk

archivoJson = 'IndexTextoFiltrado.json'

global pdf_contents

# Crear la ventana principal
ventana = tb.Window(themename="darkly")
ventana.title("Interfaz de Usuario")
ventana.geometry("800x600")

# Tamaño de la fuente para los widgets
font_large = ("Helvetica", 15)
font_medium = ("Helvetica", 13)

# Configurar estilo para ttkbootstrap
style = tb.Style()
style.configure("TButton", font=font_medium)
style.configure("TLabel", font=font_large)
style.configure("TEntry", font=font_medium)

def seleccionar_carpeta():
    carpeta = filedialog.askdirectory()
    if carpeta:
        carpeta_seleccionada.set(carpeta)

def leerTextos(carpeta_seleccionada):
    contenido = leer_archivos_txt(carpeta_seleccionada)
    parrafos = separar_parrafos(contenido)
    diccionario_indexado = crear_diccionario_indexado(parrafos)
    guardar_json(diccionario_indexado, archivoJson)

def embedingF():
    with open(archivoJson, 'r', encoding='utf-8') as file:
        pdf_contents = json.load(file)

    embedding_size = 768
    embeddings = np.zeros((len(pdf_contents), embedding_size), dtype=np.float32)

    for idx, text in pdf_contents.items():
        embeddings[int(idx)-1] = get_embedding(text)

    index = faiss.IndexFlatL2(embedding_size)  # Usar IndexFlatL2 para distancias euclidianas
    index.add(embeddings)
    index_name = "pdf_index_filt.faiss"
    faiss.write_index(index, index_name)

def enviar_prompt(prompt):
    with open(archivoJson, 'r', encoding='utf-8') as file:
        pdf_contents = json.load(file)

    respuesta = get_answer(prompt, pdf_contents)

    area_texto.config(state=tk.NORMAL)
    area_texto.delete(1.0, tk.END)  # Limpiar el área de texto
    area_texto.insert(tk.END, respuesta.content)
    area_texto.config(state=tk.DISABLED)

# Crear y colocar los widgets
# Sección de selección de carpeta
tb.Label(ventana, text="Carpeta:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
carpeta_seleccionada = tk.StringVar()
tb.Entry(ventana, textvariable=carpeta_seleccionada, state="readonly", width=50).grid(row=0, column=1, columnspan=4, padx=10, pady=10, sticky="we")
tb.Button(ventana, text="Seleccionar Carpeta", command=seleccionar_carpeta, bootstyle="success").grid(row=1, column=1, padx=10, pady=10, sticky="w")

# Botón para combinar archivos TXT
tb.Button(ventana, text="Textos", command=lambda: leerTextos(carpeta_seleccionada.get()), bootstyle="info-outline").grid(row=1, column=2, padx=10, pady=10, sticky="w")
tb.Button(ventana, text="Embedings", command=lambda: embedingF(), bootstyle="info-outline").grid(row=1, column=3, padx=10, pady=10, sticky="w")

# Sección de prompt
tb.Label(ventana, text="Prompt:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
entrada_prompt = tb.Entry(ventana, width=50)
entrada_prompt.grid(row=2, column=1, columnspan=4, padx=10, pady=10, sticky="we")

tb.Button(ventana, text="Enviar", command=lambda: enviar_prompt(entrada_prompt.get()), bootstyle="primary").grid(row=3, column=1, padx=10, pady=10, sticky="w")

# Área de texto para mostrar resultados de enviar prompt
area_texto = tk.Text(ventana, height=20, width=50, bg="#3E3E3E", fg="#FFFFFF", wrap=tk.WORD, font=font_medium)
area_texto.grid(row=4, column=0, columnspan=5, padx=10, pady=10, sticky="nswe")
area_texto.config(state=tk.DISABLED)

# Configurar el grid para que se expanda correctamente
ventana.columnconfigure(1, weight=1)
for i in range(6):
    ventana.rowconfigure(i, weight=1)

# Iniciar el loop de eventos
ventana.mainloop()
