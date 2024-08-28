
import numpy as np
from sentence_transformers import SentenceTransformer


model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

def get_embedding(text):
    return model.encode(text)