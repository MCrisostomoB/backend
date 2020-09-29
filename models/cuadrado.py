from . import db

class CuadradoModel(db.Model):
    __tablename__ = "cuadrados"
    id = db.Column(db.Integer, primary_key=True)
    prediccion_id = db.Column(db.Integer, db.ForeignKey('predicciones.id'), nullable=False)
    clase = db.Column(db.Integer, nullable=False)
    center_x = db.Column(db.Integer, nullable=False)
    center_y = db.Column(db.Integer, nullable=False)
    width = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    accuracy = db.Column(db.Float, nullable=False)

    def __init__(self, prediccion_id: int, label: int, confidence: float, x: int, y: int, w: int, h: int):
        self.prediccion_id = prediccion_id
        self.clase = label
        self.center_x = x
        self.center_y = y
        self.width = w
        self.height = h
        self.accuracy = confidence

    def json(self):
        return {
            'id': self.id,
            'prediccion_id': self.prediccion_id,
            'clase': self.clase,
            'center_x': self.center_x,
            'center_y': self.center_y,
            'width': self.width,
            'height': self.height,
            'accuracy': self.accuracy
        }

    @classmethod
    def find_by_prediccion(cls, prediccion_id: int):
        return cls.query.filter_by(prediccion_id=prediccion_id)