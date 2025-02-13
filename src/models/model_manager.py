from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

class ModelManager:
    def __init__(self, model_name="meta-llama/Llama-3-8B"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, device_map="auto")
        self.generator = pipeline("text-generation", model=self.model, tokenizer=self.tokenizer, device=0)
    
    def generate_query(self, user_question: str) -> str:
        """Convierte la pregunta del usuario en una consulta avanzada de PubMed."""
        prompt = f"Convert the following question into an advanced PubMed search query: {user_question}"
        return self.generator(prompt, max_length=100, do_sample=True)[0]['generated_text']

    def generate_response(self, query: str, context: list) -> str:
        """Genera una respuesta basada en los fragmentos recuperados."""
        final_prompt = f"Using the following information: {context}, answer the following question: {query}"
        return self.generator(final_prompt, max_length=300, do_sample=True)[0]['generated_text']