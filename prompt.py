import random
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env file

client = OpenAI(       
    api_key=os.environ.get("OPENAI_API_KEY")
)

class Prompt():
    def __init__(self):
        self.prompts = []

    def generate_prompt(self):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a smooth mysterious casanova delivering a confident first greeting"},
                {"role": "user", "content": "Give me a short, slightly arrogent, intriguing legitimate opening question."}
            ],
            max_tokens=20,
            temperature=1.0,
        )

        prompt = response.choices[0].message.content.strip()
        self.prompts.append(prompt)
        return prompt

    def get_random_prompt(self):
        if not self.prompts:
            self.generate_prompt()
        return random.choice(self.prompts)


# Example usage
prompt_generator = Prompt()
print(prompt_generator.generate_prompt())
print(prompt_generator.get_random_prompt())