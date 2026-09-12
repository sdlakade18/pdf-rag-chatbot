import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


class GeminiLLM:

    def __init__(self, model_name: str):
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set")

        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name

    def generate(self, prompt: str) -> str:

        interaction = self.client.interactions.create(
            model=self.model_name,
            input=prompt
        )

        return interaction.output_text