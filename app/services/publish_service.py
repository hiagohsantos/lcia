#from app.repositories.publish_repository import ProcessRepository
from groq import Groq
import json

from app.models.file import File
from app.models.organization import Organization
from app.repositories.LC_repository import LCRepository
from app.repositories.base_repository import BaseRepository

class PublishService:
    def __init__(self):
        # Repositórios injetados como dependências
        self._file_repository = BaseRepository(File)


    @staticmethod
    def get_publish_by_id(publish_id, organization: Organization):
        try:  

            print(f"buscando publicacao id {publish_id} para organizacao {organization.name}")
            # Validação do ID
            if publish_id <= 0:
                raise ValueError("ID inválido fornecido.")
            
            _repository = LCRepository(organization)
            #_repository.get_publish_by_id(publish_id)
            #_repository.get_process_by_id(publish_id)
            _repository.get_process_client_position(publish_id)

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


    def create_file(self, file) -> File:
        try:
           
            file_data = {
                'filename': file.filename.split('.')[0],  
                'file_extension': file.filename.split('.')[-1],  
                'file_size': len(file.read()), 
                }
            
            file_instance = self._file_repository.create(File.from_dict(file_data))
            return file_instance
        
        except Exception as e:
            print(e)
            return None
    
    def get_file_by_id(self, file_id: str) -> File | None:
        try:
            
            file_instance = self._file_repository.get(id=file_id)
            return file_instance
        
        except Exception as e:
            print(e)
            return None
    

       