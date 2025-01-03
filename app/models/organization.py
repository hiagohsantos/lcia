from app.extensions import db
from app.models.base_entity import BaseEntity

class Organization(BaseEntity):
    __tablename__ = 'organization'

    name = db.Column(db.String(100), nullable=False)
    api_keys = db.relationship('ApiKey', backref='organization', lazy=True)

    # Database props
    db_server = db.Column(db.String(255), nullable=False)   # IP ou domínio do servidor
    db_name = db.Column(db.String(100), nullable=False)     # Nome do banco
    db_user = db.Column(db.String(50), nullable=False)      # Usuário do banco
    db_password = db.Column(db.String(100), nullable=False) # Senha do banco
     
