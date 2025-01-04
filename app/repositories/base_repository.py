from app.extensions import db

class BaseRepository:
    def __init__(self, model):
        """Inicializa o repositório com o modelo especificado."""
        self.model = model

    def get(self, **kwargs):
        return self.model.query.filter_by(**kwargs).first()
    

    def get_all(self):
        return self.model.query.all()


    def get_by_id(self, id):
        return self.model.query.get(id)


    def filter_by(self, **kwargs):
        return self.model.query.filter_by(**kwargs).all()


    def create(self, instance):
        db.session.add(instance)
        db.session.commit()
        return instance


    def update(self, id, **kwargs):
        instance = self.model.query.get(id)
        if not instance:
            return None
        for key, value in kwargs.items():
            setattr(instance, key, value)
        db.session.commit()
        return instance


    def delete(self, id):
        instance = self.model.query.get(id)
        if instance:
            db.session.delete(instance)
            db.session.commit()
            return True
        return False


## Exemplos de Uso

## Trabalhando com Organization
# organization_repo = BaseRepository(Organization)

## Criar uma nova organização
# organization = organization_repo.create(name="Empresa ABC")

## Buscar todas as organizações
# organizations = organization_repo.get_all()

## Trabalhando com ApiKey
# apikey_repo = BaseRepository(ApiKey)