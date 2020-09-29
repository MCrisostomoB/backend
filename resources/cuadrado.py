from flask_restful import Resource, reqparse
from models.cuadrado import CuadradoModel

# /cuadrado/<int:prediccion_id>
class Cuadrado(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('prediccion_id',
        type=int,
        required=True,
        help="El campo prediccion no puede estar vacio.",
        location='args'
    )

    def get(self):
        data = Cuadrado.parser.parse_args()
        filter_boxes = CuadradoModel.find_by_prediccion(data['prediccion_id'])
        return {'cuadrados': [box.json() for box in filter_boxes]}, 200