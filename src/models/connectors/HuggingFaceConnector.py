from connectors import LLMConnector
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