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
            model="gpt-4.1-nano",
            messages=[
                {"role": "system", "content": "You are Frank reynolds from always sunny in philadelphia sending a first message after matching on tinder and being as stupid and sleazy as possible in less than 25 words"},
                {"role": "user", "content": "Frank Reynolds billionaire lives with charlie eats catfood and bangs hoors. Also goes as Mantis toboggan M.D and accidently drops his monster condom which he uses for his magnum dong"}
            ],
            max_tokens=30,
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