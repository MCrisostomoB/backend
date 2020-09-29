from . import db
import datetime
from sqlalchemy import desc

class PrediccionModel(db.Model):
    __tablename__ = "predicciones"
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    fecha = db.Column(db.DateTime, nullable=False)
    area = db.Column(db.Float, nullable=False)

    def __init__(self, product_id: int, area: int):
        self.fecha = datetime.datetime.now()
        self.product_id = product_id
        self.area = area

    def json(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'fecha': str(self.fecha),
            'area': self.area
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def findByIDCamara(cls, product_id):
        return cls.query.filter_by(product_id = product_id).order_by(desc(cls.fecha)).first()

        
    def delete_from_db(self):
        db.session.delete(self)
        db.session.flush()
        db.session.commit()