from app.extensions import db
import uuid
from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column  # Importando a nova sintaxe

class BaseEntity(db.Model):
    __abstract__ = True

    id: Mapped[str] = mapped_column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    created_at: Mapped[datetime] = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    disabled: Mapped[bool] = db.Column(db.Boolean, default=False)  

    def __init__(self, *args, **kwargs):
        super(BaseEntity, self).__init__(*args, **kwargs)
