from app.extensions import db
from sqlalchemy.orm import Mapped
from app.models.base_entity import BaseEntity

class File(BaseEntity):
    __tablename__ = 'files'

    filename: Mapped[str] = db.Column(db.String(255), nullable=False)
    file_extension: Mapped[str] = db.Column(db.String(10), nullable=False)
    file_size: Mapped[int] = db.Column(db.Integer, nullable=False)

    # organization_id = db.Column(db.String(36), db.ForeignKey('organization.id'), nullable=True)
    # organization = db.relationship('Organization', backref='files', lazy=True)

    @classmethod
    def from_dict(cls, data: dict):
        """
        Cria uma instância a partir de um dicionário.
        """
        return cls(
            filename=data.get('filename'),
            file_extension=data.get('file_extension'),
            file_size=data.get('file_size'),
        )

    def to_dict(self):
        """
        Converte a entidade em um dicionário.
        """
        return {
            'id': self.id,
            'filename': self.filename,
            'file_extension': self.file_extension,
            'file_size': self.file_size,
        }
