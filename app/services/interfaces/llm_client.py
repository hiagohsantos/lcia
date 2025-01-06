
class LLMClient:
    def __init__(self, api_key: str):
        self.api_key = api_key

    def send_message(self, schema: dict, system_message: str, user_message: str):
        raise NotImplementedError("Método deve ser implementado na subclasse.")
