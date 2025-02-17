
import ollama
import openai
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch



class HuggingFaceConnector(LLMConnector):
    """Conector para modelos de Hugging Face"""
    
    def __init__(self, model_name: str = "mistralai/Mistral-7B-Instruct-v0.2"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        self.generator = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer)
    
    def generate_text(self, prompt: str, max_length: int = 300) -> str:
        response = self.generator(prompt, max_length=max_length, do_sample=True)[0]['generated_text']
        return response

class OllamaConnector(LLMConnector):
    """Conector para modelos locales via Ollama"""
    
    def __init__(self, model_name: str = "llama2"):
        self.model = model_name
    
    def generate_text(self, prompt: str, max_length: int = 300) -> str:
        response = ollama.generate(
            model=self.model,
            prompt=prompt,
            max_tokens=max_length
        )
        return response['response']

class LMStudioConnector(LLMConnector):
    """Conector para modelos vía LM Studio API compatible con OpenAI"""
    
    def __init__(self, base_url: str = "http://localhost:1234/v1", api_key: str = "not-needed"):
        self.client = openai.OpenAI(
            base_url=base_url,
            api_key=api_key
        )
    
    def generate_text(self, prompt: str, max_length: int = 300) -> str:
        response = self.client.chat.completions.create(
            model="local-model",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_length
        )
        return response.choices[0].message.content

class LLMConnectorFactory:
    """Fábrica de conectores LLM"""
    
    @staticmethod
    def get_connector(connector_type: str, **kwargs) -> LLMConnector:
        """
        Crea y retorna una instancia del conector especificado
        
        Args:
            connector_type: Tipo de conector ("huggingface", "ollama", "lmstudio")
            **kwargs: Argumentos específicos para el conector
        
        Returns:
            LLMConnector: Instancia del conector solicitado
        """
        connectors = {
            "huggingface": HuggingFaceConnector,
            "ollama": OllamaConnector,
            "lmstudio": LMStudioConnector
        }
        
        if connector_type not in connectors:
            raise ValueError(f"Conector no soportado. Opciones válidas: {list(connectors.keys())}")
            
        return connectors[connector_type](**kwargs)
