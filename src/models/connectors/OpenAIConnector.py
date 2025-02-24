from openai import OpenAI
from .LLMConnector import LLMConnector

class OpenAIConnector(LLMConnector):
    """OpenAI Connector for models"""

    def __init__(self, base_url: str = "https://api.openai.com/v1", api_key: str = "not-needed", model: str = "gpt-4o-mini"):
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
        )
        self.model = model

    def generate_text(self, prompt: str, max_length: int = 300) -> str:
        response = self.client.chat.completions.create(
            model= self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_length
        )
        return response.choices[0].message.content