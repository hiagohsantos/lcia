import os
from app.repositories.connection_pool import DatabaseConnectionPool
from dotenv import load_dotenv

load_dotenv()
class Config:
    # Configurações gerais
    JSON_AS_ASCII = False
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    PINECONE_API_KEY= os.getenv('PINECONE_API_KEY')
    ADM_API_KEY= os.getenv("ADM_API_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Pool de conexões para SQL Server
    DB_POOL = DatabaseConnectionPool(max_size=50)

    # Diretório base do projeto
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Caminho para salvar os uploads
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')



