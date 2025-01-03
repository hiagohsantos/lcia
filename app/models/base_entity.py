from app.extensions import db
import uuid
from datetime import datetime, timezone

class BaseEntity(db.Model):
    __abstract__ = True  # Indica que esta classe não será mapeada diretamente para uma tabela

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    disabled = db.Column(db.Boolean, default=False)  

    def __init__(self, *args, **kwargs):
        super(BaseEntity, self).__init__(*args, **kwargs)

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance

    @classmethod
    def find_by_id(cls, entity_id):
        return cls.query.get(entity_id)

    def disable(self):
        """Método para desabilitar a entidade"""
        self.disabled = True
        db.session.commit()

    def enable(self):
        """Método para habilitar a entidade"""
        self.disabled = False
        db.session.commit()
