from app.extensions import db
from app.models.apikey import ApiKey

class AuthRepository:
    @staticmethod
    def create_api_key_for_organization(organization_id):
        # Gerar e salvar API key
        api_key = ApiKey.generate_api_key()
        api_key_hash = ApiKey.hash_api_key(api_key)
        apikey = ApiKey(organization_id=organization_id, hash=api_key_hash)
        db.session.add(apikey)
        db.session.commit()
        return api_key  