from app.extensions import db
from app.models.base_entity import BaseEntity

class ApiKey(BaseEntity):
    __tablename__ = 'api_key'

    organization_id = db.Column(db.String(36), db.ForeignKey('organization.id'), nullable=False)
    hash = db.Column(db.String(256), nullable=False)
    limit_date = db.Column(db.DateTime, nullable=True)
