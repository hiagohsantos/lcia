import os
from datetime import datetime, timedelta
from app.extensions import db
from app.models.organization import Organization
from app.models.apikey import ApiKey
from app.repositories.base_repository import BaseRepository
from app.services.auth_service import AuthService
from flask import current_app as app

def seed_data():
    """Função para criar dados iniciais no banco de dados."""
    # Repositórios e serviços
    organization_repo = BaseRepository(Organization)
    apikey_repo = BaseRepository(ApiKey)
    auth_service = AuthService()

    try:
        # Organizações para criar
        organizations = [
            {
                'name': 'ADM',
                'db_server': '',
                'db_name': '',
                'db_user': '',
                'db_password': ''
            },
            {
                'name': 'VAA ATC',
                'db_server': '110.95.201.18',
                'db_name': 'lcr_LegalControl_Vigna_atc',
                'db_user': 'LCVigna',
                'db_password': '2016@Vigna'
            },
        ]

        for org in organizations:
            if organization_repo.get(name=org['name']):  
                continue

            organization = Organization(
                name=org['name'],
                db_server=org['db_server'],
                db_name=org['db_name'],
                db_user=org['db_user'],
                db_password=org['db_password']
            )
            db.session.add(organization)
            db.session.flush() 

            # Cria a API Key
            if org['name'] == 'ADM':
                api_key = app.config['ADM_API_KEY']
            else:
                api_key = auth_service.generate_api_key()

            hashed_key = auth_service.hash_api_key(api_key)

            key = ApiKey(
                organization_id=organization.id,
                hash=hashed_key,
                limit_date=datetime.utcnow() + timedelta(days=365)
            )
            db.session.add(key)

            print(f"Organização {org['name']} criada com chave: {api_key}")

        db.session.commit()

    except Exception as e:
        print(f"Erro ao criar dados iniciais: {str(e)}")
        db.session.rollback()
