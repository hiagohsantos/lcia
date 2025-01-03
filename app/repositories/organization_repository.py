from app.extensions import db
from app.models.organization import Organization
from app.models.apikey import ApiKey

class OrganizationRepository:
    @staticmethod
    def create_organization(empresa_nome):
        # Criar organização
        organization = Organization(name=empresa_nome)
        db.session.add(organization)
        db.session.commit()
        return organization