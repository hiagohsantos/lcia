import json
from openai import OpenAI
from flask import current_app
from app.services.interfaces.llm_client import LLMClient


class OpenAIClient(LLMClient):
    def __init__(self):
        super().__init__(current_app.config['OPENAI_API_KEY'])
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o"

    def send_message(self, schema: dict, system_message: str, user_message: str):
        try:
            messages = [
                {"role": "system", "content": system_message + json.dumps(schema)},
                {"role": "user", "content": user_message}
            ]
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0,
                response_format={ "type": "json_object" }
            )

            # Extrair e retornar a resposta
            content = response.choices[0].message.content
            return json.loads(content) if content else None

        except Exception as e:
            print(f"Erro na comunicação com OpenAI: {e}")
            return None
