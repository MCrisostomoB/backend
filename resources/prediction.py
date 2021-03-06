from flask_restful import Resource, reqparse
import json
import ast 

from models import db
from models.prediccion import PrediccionModel
from models.products import ProductModel

def sumaBoxes(boxes: list) -> int:
    sum_area = 0
    for box in boxes:
        sum_area += box['w'] * box['h']
    return sum_area

# /prediccion
class Prediction(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('data',
        type=str,
        required=True,
        help="El campo producto no puede estar vacio.",
        location='json'
    )

    def post(self):
        data = Prediction.parser.parse_args()
        created = []
        # find the camera
        products =  ast.literal_eval(data['data'])
        for i in products.keys():
            producto = ProductModel.find_by_id(i)
            # print(producto.id,flush=True)
            if not producto:
                return f"No se encontro la producto: {i}", 404
            # add the prediction
            # print(products[i],flush= True)
            new_prediction = PrediccionModel(i, products[i])
            db.session.add(new_prediction)
            db.session.flush() # make a transaction
            db.session.commit() # save the prediction and the boxes
            created.append(new_prediction)
        return f"Se Insertaron las predicciones con exito", 201

    def get(self):
        return {'predicciones':[prediccion.json() for prediccion in PrediccionModel.find_all()]}, 200