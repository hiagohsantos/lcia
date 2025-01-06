import json
from flask import current_app
from groq import Groq
from app.services.interfaces.llm_client import LLMClient


class GroqClient(LLMClient):
    def __init__(self):
        super().__init__(current_app.config['GROQ_API_KEY'])
        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.3-70b-specdec"

    def send_message(self, schema: dict, system_message: str, user_message: str):
        try: 
            messages = [
                {"role": "system", "content": system_message + json.dumps(schema)},
                {"role": "user", "content": user_message}
            ]
            
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0,
                response_format={"type": "json_object"}
            )
            
            content = completion.choices[0].message.content
            return json.loads(content) if content else None

        except Exception as e:
            print(f"Erro na comunicação com Groq: {e}")
            return None
