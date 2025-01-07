import json
from flask import current_app
from groq import Groq
from app.services.interfaces.llm_client import LLMClient

class ErroDePrompt(Exception):
    """
    Exceção personalizada para erros relacionados ao prompt.

    Essa exceção é lançada quando o prompt fornecido é inválido, está vazio
    ou quando ocorre um erro durante a comunicação com a API do OpenAI.
    """

class GroqClient(LLMClient):
    def __init__(self):
        super().__init__(current_app.config['GROQ_API_KEY'])
        self.client = Groq(api_key=self.api_key)
        self.model = "llama3-70b-8192"

    def send_message(self, schema: dict, system_message: str, user_message: str):
        try: 
            messages = [
                {"role": "system", "content": system_message + json.dumps(schema)},
                {"role": "user", "content": user_message}
            ]
            
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            
            content = completion.choices[0].message.content
            return json.loads(content) if content else None

        except Exception as e:
            print(f"Erro na comunicação com Groq: {e}")
            return None
        
        
    def send_order(self, prompt: str, system_message: str, schema: dict) -> str:
        """
        Gera uma resposta do GPT-4 com base no prompt fornecido.

        Este método envia o prompt e uma mensagem de sistema contendo instruções
        e o esquema esperado para o modelo. Retorna a resposta no formato JSON.

        Parâmetros:
        -----------
        prompt : str
            O texto de entrada que será enviado ao modelo GPT-4.
        system_message : str
            Mensagem que define o contexto ou instruções do sistema.
        schema : dict
            Um dicionário que define o esquema esperado para a resposta.

        Retorna:
        --------
        str
            A resposta gerada pelo GPT-4 no formato JSON.

        Exceções:
        ---------
        ErroDePrompt:
            Lançada se o prompt estiver vazio ou se ocorrer um erro ao tentar
            obter a resposta da API do OpenAI.

        Exemplos:
        ---------
        >>> cliente = ClienteGPT()
        >>> prompt = "Explique o conceito de inteligência artificial."
        >>> system_message = "Responda no seguinte formato JSON:"
        >>> schema = {"tipo": "explicacao"}
        >>> resposta = cliente.chat(prompt, system_message, schema)
        >>> print(resposta)
        """
        if not prompt:
            raise ErroDePrompt("O prompt não pode estar vazio. Por favor, forneça um prompt válido.")

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": f"{system_message} Por favor, retorne no formato JSON. Esquema: {json.dumps(schema)}",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                temperature=0,
                stream=False,
                response_format={"type": "json_object"},
                # model="llama-3.3-70b-versatile"
                model="gemma2-9b-it"
            )

            response = chat_completion.choices[0].message.content
            return response
        except Exception as e:
            raise ErroDePrompt(f"Ocorreu o seguinte erro ao tentar obter uma resposta do Groq: {e}")
