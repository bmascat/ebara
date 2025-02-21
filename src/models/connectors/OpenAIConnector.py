
import openai
from .LLMConnector import LLMConnector

class OpenAIConnector(LLMConnector):
    """OpenAI Connector for models"""
    
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