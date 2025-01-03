import os

class Config:
    # Configurações gerais
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:123@localhost/lcia'


