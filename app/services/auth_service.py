from datetime import datetime, timedelta
import secrets
import hashlib
from app.repositories.base_repository import BaseRepository
from app.models.apikey import ApiKey
from app.models.organization import Organization

class AuthService:
    def __init__(self):
        self.api_key_repository = BaseRepository(ApiKey)


    def generate_api_key(self):
        """Gera uma API key segura."""
        return secrets.token_urlsafe(32)


    def hash_api_key(self, api_key):
        """Gera um hash seguro para a API key."""
        return hashlib.sha256(api_key.encode('utf-8')).hexdigest()
    

    def verify_api_key(self, api_key):
        """Verifica se a API key é válida e não está expirada."""
        hashed_key = self.hash_api_key(api_key)
        stored_key = self.api_key_repository.get(hash=hashed_key)

        if stored_key and stored_key.limit_date >= datetime.utcnow():
            return True
        return False


    def revoke_api_key(self, api_key):
        """Revoga uma API key, removendo-a do banco de dados."""
        hashed_key = self.hash_api_key(api_key)
        api_key_record = self.api_key_repository.find_one(hash=hashed_key)

        if api_key_record:
            self.api_key_repository.delete(api_key_record)
            return True
        return False


    def renew_api_key(self, api_key, new_limit_days=30):
        """Renova a validade de uma API key."""
        hashed_key = self.hash_api_key(api_key)
        api_key_record = self.api_key_repository.find_one(hash=hashed_key)

        if api_key_record:
            api_key_record.limit_date = datetime.utcnow() + timedelta(days=new_limit_days)
            self.api_key_repository.update(api_key_record)
            return True
        return False
