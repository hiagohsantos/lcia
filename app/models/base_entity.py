from app.extensions import db
import uuid
from datetime import datetime, timezone

class BaseEntity(db.Model):
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    disabled = db.Column(db.Boolean, default=False)  

    def __init__(self, *args, **kwargs):
        super(BaseEntity, self).__init__(*args, **kwargs)

