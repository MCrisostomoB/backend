from . import db

class PasilloModel(db.Model):
    __tablename__ = "pasillos"
    
    id = db.Column(db.Integer, primary_key=True)
    numero =  db.Column(db.Integer, nullable=True)
    categoria = db.Column(db.String(255))
    camaras = db.relationship('CamaraModel', backref='pasillos', lazy='select')

    def __init__(self, categoria: str, numero: int):
        self.categoria = categoria
        self.numero =  numero
    
    def json(self):
        return {
            'id': self.id,
            'numero': self.numero,
            'categoria': self.categoria,
        }

    def jsonWithCameras(self):
        return {
            'id': self.id,
            'numero': self.numero,
            'categoria': self.categoria,
            'camaras': self.camaras,
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def findByNumber(cls, num):
        return cls.query.filter_by(numero=num).first()

    @classmethod
    def findByID(cls, id_pasillo):
        return cls.query.filter_by(id=id_pasillo).first()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.flush()
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.flush()
        db.session.commit()