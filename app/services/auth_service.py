from app.models.apikey import ApiKey
from app.repositories.auth_repository import AuthRepository
from app.repositories.organization_repository import OrganizationRepository

class AuthService:
    @staticmethod
    def create_organization_and_api_key(empresa_nome):
        organization = OrganizationRepository.create_organization(empresa_nome)

        api_key = AuthRepository.create_api_key_for_organization(organization.id)

        return organization, api_key  
