from app.models.apikey import ApiKey
from app.models.file import File
from app.models.input_models.organization_input import OrganizationInputModel
from app.models.organization import Organization
from app.repositories.base_repository import BaseRepository
from app.services.auth_service import AuthService

class OrganizationService:
    def __init__(self):
        self.organization_repo = BaseRepository(Organization)
        self.apikey_repo =  BaseRepository(ApiKey)
        self._auth_service = AuthService()


    def create_organization_and_api_key(self, input: OrganizationInputModel):
        try: 
            if self.organization_repo.get(name=input.name):
                raise ValueError("Já existe uma empresa com o nome informado.")
            
            data = Organization(**input.model_dump())

            organization = self.organization_repo.create(data)

            api_key =  self._auth_service.generate_api_key()
            hashed_key =  self._auth_service.hash_api_key(api_key)
            
            key = ApiKey(organization_id=organization.id, hash=hashed_key)

            self.apikey_repo.create(key)
            
            return organization, api_key  
        
        except Exception as e:
            print(e)
            raise e

