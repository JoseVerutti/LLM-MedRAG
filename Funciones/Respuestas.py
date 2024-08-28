from openai import OpenAI
import os
import faiss
import numpy as np
from .Embeding import get_embedding



api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=api_key)

def getRespuestasPotenciales(preguntaEmb, pdf_contents):
    contexto = ""
    k = 20 
    index = faiss.read_index("pdf_index_filt.faiss")
    distances, ids_potenciales_respuestas = index.search(np.array([preguntaEmb]), k)

    for idx in ids_potenciales_respuestas[0]:
        print(idx +1)
        contexto =contexto + (pdf_contents[str(idx+1)])
    print(contexto)

    return contexto

def get_answer(pregunta, pdf_contents):

    preguntaEMB=get_embedding(pregunta)

    contexto= getRespuestasPotenciales(preguntaEMB, pdf_contents)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        max_tokens=800,
        messages=[
            {"role": "system", "content": f"Eres un asistente de ingenieria clinica en colombia especialista en reglamentacion para acreditacion, habilitación, y comercializacion de servicios de salud y dispositivos medicos. Responde acorde al contexto que se encuentra entre comillas simples, y !!cita¡¡ los articulos o contenidos que se te entreguen en el contexto al final''' {contexto} '''"},
            {"role": "user", "content": f"{pregunta}.Cita los articulos y documentos que se te entregan en el contexto, No te salgas demasiado de la informacion que te brinda el contexto"}
        ]
    )
    return completion.choices[0].message