# ollama_client.py

from ollama import Client
import os

# Configurar la URL de Ollama (por defecto es http://localhost:11434)
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
client = Client(host=OLLAMA_HOST)

def generate_response(prompt: str) -> str:
    """
    Genera una respuesta usando el modelo de Ollama.
    Por defecto usa el modelo 'llama2', pero puedes especificar otros como 'mistral' o 'gemma'
    """
    try:
        # Genera la respuesta usando el modelo
        response = client.generate(
            model='llama2',  # o el modelo que prefieras
            prompt=prompt,
            max_tokens=200,
            temperature=0.7
        )
        return response['response']
    except Exception as e:
        print(f"Error al generar respuesta con Ollama: {str(e)}")
        return "Lo siento, hubo un error al generar la respuesta."

# Ejemplo de uso más avanzado con chat
def chat_with_model(messages: list) -> str:
    """
    Mantiene una conversación con el modelo usando el formato de chat.
    """
    try:
        response = client.chat(
            model='llama2',
            messages=messages,  # Lista de mensajes en formato [{"role": "user", "content": "..."}, ...]
            temperature=0.7
        )
        return response['message']['content']
    except Exception as e:
        print(f"Error en la conversación con Ollama: {str(e)}")
        return "Lo siento, hubo un error en la conversación."

# Ejemplo de cómo obtener los modelos disponibles
def list_available_models():
    """
    Lista todos los modelos disponibles localmente.
    """
    try:
        models = client.list()
        return [model['name'] for model in models]
    except Exception as e:
        print(f"Error al listar modelos: {str(e)}")
        return []
