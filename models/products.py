from . import db

class ProductModel(db.Model):
    __tablename__ = "productos"

    id = db.Column(db.Integer, primary_key=True)
    pasillo_id = db.Column(db.Integer, db.ForeignKey('pasillos.id'), nullable=False)
    product_name = db.Column(db.String(255), nullable=False)
    coordinates = db.Column(db.String(255), nullable=False)
    camara_id = db.Column(db.Integer, db.ForeignKey('camaras.id'),nullable = False)

    def __init__(self, product_name: str,pasillo_id: int, coordinates: str, camara_id:int ):
        self.product_name = product_name
        self.pasillo_id = pasillo_id
        self.coordinates = coordinates
        self.camara_id = camara_id


    def json(self):
        return {
            'id': self.id,
            'product_name': self.product_name,
            'pasillo_id' : self.pasillo_id,
            'coordinates': self.coordinates,
            'camara_id':self.camara_id
        }

    @classmethod
    def find_by_pasillo(cls, pasillo_id: int):
        return cls.query.filter_by(pasillo_id=pasillo_id)
    @classmethod
    def find_by_camara(cls, camara_id: int):
        return cls.query.filter_by(camara_id=camara_id)
    
    @classmethod
    def find_by_id(cls, id: int):
        return cls.query.filter_by(id=id).first()
        
    @classmethod
    def find_by_name(cls, product_name: str):
        return cls.query.filter_by(product_name=product_name)
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