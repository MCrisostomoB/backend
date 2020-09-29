from flask import request, jsonify
from flask_restful import Resource, reqparse
from models import db
from models.camara import CamaraModel
from models.pasillo import PasilloModel

class Camara(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('pasillo_id',
        type=int,
        required=True,
        help="El campo pasillo_id no puede estar vacio.",
        location='json'
    )

    parser.add_argument('nombre',
        type=str,
        required=False,
        location='json'
    )

    parser.add_argument('path',
        type=str,
        required=False,
        location='json'
    )

    # add new element
    def post(self):
        data = Camara.parser.parse_args()

        # find pasillo
        pasillo = PasilloModel.findByID(data['pasillo_id'])
        if not pasillo:
            return f"No se encontro el pasillo: {data['pasillo_id']}", 404

        # create new element
        new_camara = CamaraModel(**data)
        message = 'Ha ocurrido un error al ingresar a la base de datos'
        try:
            new_camara.save_to_db()
        except:
            return {
                'message': message
            }
        
        return new_camara.json(), 201 #201 created
    
    # get all
    def get(self):
        return {'camara': [x.json() for x in CamaraModel.find_all()]}, 200

    