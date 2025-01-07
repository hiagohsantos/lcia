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
from app.services.openai_service import OpenAIClient

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
            
            #schema_json = AppointmentExtraction.model_json_schema()
    
            client = OpenAIClient()
            
            prompty = f"""Analise o texto informado e extraia todos os prazo solicitados as partes do processo em formato JSON."""

            schema = {
                "appointments": [ 
                    {
                        "description": "Descrição detalhada da ação obrigatória ou dirigida às partes envolvidas no processo. Inclua instruções claras e detalhadas sobre o que a parte precisa fazer, sem mencionar opções ou sugestões.",
                        "text": "Trecho do texto onde a ação foi encontrada. Inclua citações relevantes para contexto.",
                        "summary": "Resumo detalhado da ação direta, incluindo prazos por extenso, explicando a finalidade e as implicações da ação solicitada.",
                        "start_date": "Data e hora de início do prazo no formato ISO 8601 (YYYY-MM-DDTHH:MM).",
                        "end_date": "Data e hora de finalização do prazo no formato ISO 8601 (YYYY-MM-DDTHH:MM).",
                    }
                ]
            }

            response = client.send_message(schema, prompty, publish.sentence)
            response['publish_id'] = publish_id
            response['original_text'] = publish.sentence
            
            print("\n",json.dumps(response, indent=4, ensure_ascii=False))
            return response

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
    

       