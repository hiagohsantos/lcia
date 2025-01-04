import os

class Config:
    # Configurações gerais
    JSON_AS_ASCII = False
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123@localhost/lcia'

    # Diretório base do projeto
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Caminho para salvar os uploads
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

