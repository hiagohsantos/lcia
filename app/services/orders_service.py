from app.models.apikey import ApiKey
from app.models.file import File
from app.models.input_models.organization_input import OrganizationInputModel
from app.models.organization import Organization
from app.repositories.base_repository import BaseRepository
from app.services.auth_service import AuthService
import pandas as pd
from docx import Document

from app.services.lang_chain_service import AplicacaoGerenciamento

class ErrosData(Exception):
    """
    Exceção personalizada para erros relacionados ao carregamento ou manipulação de dados.
    Utilizada para distinguir problemas específicos de dados de outros tipos de exceções.
    """
    pass

class OrdersService:
    def __init__(self):
        self.apikey_repo =  BaseRepository(ApiKey)
        self._file_repository = BaseRepository(File)

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
    
    def extract_data(self, file_name: str) -> str:
        try:
            try: 
                document_text = self.carregar_texto_docx(file_name)
                #print(f"Texto extraído do documento: {document_text}")

            except Exception as e:
                return f"Erro ao processar o arquivo DOCX: {str(e)}"

            prompt = """
                Leia atentamente o documento fornecido e extraia as seguintes informações:
                Quais os pedidos feitos pelo autor?
                Há valor especificado nos pedidos? Se sim, qual?
                Existe cobrança de juros? (Sim/Não)
                Se sim: Qual é o percentual dos juros?
                Correção Monetária: Existe menção a correção monetária? Se sim, qual o índice requerido (informar exatamente como no documento)?
                Multa: Existe previsão de multa? Se sim, qual percentual ou valor?
                Honorários: Há pedido de honorários advocatícios? Se sim, qual o valor ou percentual?
            """
            
            response = AplicacaoGerenciamento().enviar_prompt(prompt, documento=document_text, inserir_novos_embeddings=False)
            return response
        except Exception as ex:
            print(ex)


    def carregar_texto_docx(self, file_path: str) -> str:
        """
        Carrega o texto de um arquivo .docx.
        
        Parâmetros:
        -----------
        caminho_arquivo : str
            Caminho para o arquivo .docx.
        
        Retorna:
        --------
        str
            O texto completo do arquivo .docx.
        """
        documento = Document(file_path)
        texto = "\n".join(paragrafo.text for paragrafo in documento.paragraphs)
        return texto
