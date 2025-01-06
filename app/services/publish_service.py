#from app.repositories.publish_repository import ProcessRepository
from flask import config, current_app
from groq import Groq
import json

from app.models.appointment_extration import AppointmentExtraction
from app.models.file import File
from app.models.organization import Organization
from app.repositories.LC_repository import LCRepository
from app.repositories.base_repository import BaseRepository
from app.services.groq_service import GroqClient

class PublishService:
    def __init__(self, organization: Organization):
        # Repositórios injetados como dependências
        self._file_repository = BaseRepository(File)
        self.organization = organization
        self._repository = LCRepository(organization)

    def get_publish_by_id(self, publish_id):
        try:  
            # Validação do ID
            if publish_id <= 0:
                raise ValueError("ID inválido fornecido.")
            
            publish = self._repository.get_publish_by_id(publish_id)
            if not publish: return None
            
            print(publish.sentence)
            schema_json = AppointmentExtraction.model_json_schema()

            prompty = f"""Analise o texto informado e extraia todos os compromissos em formato JSON."""
            
            client = GroqClient()
            response = client.send_message(schema_json, prompty, publish.sentence)
            print(response)

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
    

       