import os
import openai
import tiktoken
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize API key
openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

class GPTSummarizer:
    def __init__(self, model=MODEL):
        self.model = model

    def summarize_problems(self, text: str) -> str:
        instruction = (
            "You are an expert researcher. From the following Reddit posts, "
            "list the most commonly mentioned problems or pain points in bullet form."
        )
        return self._call_chat(instruction, text)

    def summarize_solutions(self, text: str) -> str:
        instruction = (
            "You are an expert researcher. From the following Reddit posts, "
            "list how users are overcoming or solving these problems in bullet form."
        )
        return self._call_chat(instruction, text)

    def _call_chat(self, instruction: str, text: str) -> str:
        messages = [
            {"role": "system", "content": instruction},
            {"role": "user",   "content": text}
        ]
        # Single API call using openai module
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            temperature=0.0,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()