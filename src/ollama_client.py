# ollama_client.py

import requests

def generate_response(prompt: str) -> str:
    """
    Llama al modelo de Ollama para generar una respuesta basada en el prompt.
    Si la llamada falla o no se dispone de Ollama, se devuelve una respuesta simulada.
    """
    # Ejemplo de endpoint; reemplázalo por el real si cuentas con él.
    url = "http://localhost:11434/generate"  
    payload = {
        "prompt": prompt,
        "max_tokens": 200,
        "temperature": 0.7
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        # Se asume que la respuesta tiene una clave "text"
        return result.get("text", "No se generó respuesta.")
    except Exception as e:
        # Respuesta simulada en caso de error o falta de endpoint real
        return "Respuesta simulada basada en la evidencia:\n\n" + prompt[:200] + "..."
