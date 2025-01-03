from app.extensions import db
from app.models.apikey import ApiKey
import uuid

from app.models.base_entity import BaseEntity

class Organization(BaseEntity):
    __tablename__ = 'organization'

    name = db.Column(db.String(100), nullable=False)
    api_keys = db.relationship('ApiKey', backref='organization', lazy=True)
