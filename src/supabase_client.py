# supabase_client.py

import os
from supabase import create_client, Client

# Configura tus variables de entorno con la URL y la API KEY de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("Debes configurar las variables de entorno SUPABASE_URL y SUPABASE_KEY.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def log_query_response(question: str, response: str, articles):
    """
    Registra en Supabase la consulta, la respuesta y las referencias (DOI) de los artículos.
    """
    data = {
        "question": question,
        "response": response,
        "references": [article["doi"] for article in articles]
    }
    try:
        supabase.table("query_logs").insert(data).execute()
    except Exception as e:
        print("Error al registrar en Supabase:", e)
