from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import uuid
from app.extensions import db
import hashlib
from app.models.base_entity import BaseEntity

class ApiKey(BaseEntity):
    __tablename__ = 'api_key'

    organization_id = db.Column(db.String(36), db.ForeignKey('organization.id'), nullable=False)
    hash = db.Column(db.String(256), nullable=False)
    limit_date = db.Column(db.DateTime, nullable=True)

    @staticmethod
    def generate_api_key():
        """Gera uma API key segura."""
        return secrets.token_urlsafe(32)

    @staticmethod
    def hash_api_key(api_key):
        # Função para gerar o hash da API key
        return hashlib.sha256(api_key.encode('utf-8')).hexdigest()

    def verify_api_key(self, api_key):
        """Verifica se a API key corresponde ao hash armazenado."""
        return check_password_hash(self.hash, api_key)