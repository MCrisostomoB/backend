from . import db

class CamaraModel(db.Model):
    __tablename__ = "camaras"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), unique=True)
    path = db.Column(db.String(255), nullable=True)
    pasillo_id = db.Column(db.Integer, db.ForeignKey('pasillos.id'), nullable=False)
    

    def __init__(self,nombre: str, pasillo_id: int, path: str):
        self.nombre = nombre
        self.pasillo_id = pasillo_id
        self.path = path

    def json(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'pasillo_id' : self.pasillo_id,
            'path' : self.path
        }

    @classmethod
    def findByName(cls, nombre):
        return cls.query.filter_by(nombre=nombre).first()

    @classmethod
    def findByID(cls, id_camara):
        return cls.query.filter_by(id=id_camara).first()

    @classmethod
    def findByIDPasillo(cls, id_pasillo):
        return cls.query.filter_by(pasillo_id=id_pasillo).all()

    @classmethod
    def find_all(cls):
        return cls.query.all()
    
    def save_to_db(self):
        db.session.add(self)
        db.session.flush()
        db.session.commit()
    
    def delete_from_db(self):
        db.session.delete(self)
        db.session.flush()
        db.session.commit()