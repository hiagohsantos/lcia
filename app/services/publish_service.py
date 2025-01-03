#from app.repositories.publish_repository import ProcessRepository
from groq import Groq
import json

class ProcessService:
    @staticmethod
    def get_process_by_id(process_id):
        try:  
            # Validação do ID
            if process_id <= 0:
                raise ValueError("ID inválido fornecido.")

            # process = ProcessRepository.get_by_id(process_id)
            # client = Groq(api_key="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")

            # system_message = f"""Analise a decisao abaixo e extraia os dados seguindo o formato JSON especificado:"""

            # schema = {
            #     "partes": "String - Nome da(s) parte(s)",
            #     "prazo_judicial": "Tipo e periodo do tempo",
            #     "lei_aplicavel": "Lei aplicável"}

            # chat_completion = client.chat.completions.create(
            # messages=[
            #     {
            #         "role": "system",
            #         "content": system_message + json.dumps(schema),
            #     },
            #     {
            #         "role": "user",
            #         "content": process.sentence,
            #     }
            # ],
            # temperature=0,
            # stream=False,
            # response_format={"type": "json_object"},
            # model="llama-3.3-70b-versatile")

            # response = chat_completion.choices[0].message.content
                    
            # if response:
            #     return json.loads(response)
            
        except Exception as e:
            print(e)
            return None

    

       