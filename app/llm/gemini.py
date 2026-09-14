import os
from app.core.config import settings
from dotenv import load_dotenv
from google import genai


load_dotenv()


class GeminiLLM:

    def __init__(self, model_name: str | None = None):
        
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not set in the environment variables")
    

        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_name = model_name or settings.GEMINI_MODEL

    def generate(self, prompt: str) -> str:

        interaction = self.client.interactions.create(
            model=self.model_name,
            input=prompt
        )

        return interaction.output_text