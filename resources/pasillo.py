from flask import request, jsonify
from flask_restful import Resource, reqparse
from models import db
from models.pasillo import PasilloModel
from models.camara import CamaraModel
from models.prediccion import PrediccionModel

class Pasillo(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('numero',
        type=int,
        required = False
    )

    parser.add_argument('categoria',
        type=str,
        required = True,
        help = "Este campo no puede estar vacio"
    )

    # add new element
    def post(self):
        data = Pasillo.parser.parse_args()

        # create new element
        new_pasillo = PasilloModel(**data)
        
        try:
            new_pasillo.save_to_db()
        except:
            return {
                'message': 'Ha ocurrido un error al ingresar a la base de datos'
            }
        
        return new_pasillo.json(), 201 #201 created
    
    # get all
    def get(self):
        allPasillos = [x.jsonWithCameras() for x in PasilloModel.find_all()]
        for pasillo in allPasillos:
            predicciones = []
            for camara in pasillo['camaras']:
                # camara.predicciones TODO: sort this list to replace the line below
                ultimaPrediccion = PrediccionModel.findByIDCamara(camara.id) # sacar ultima prediccion por camara
                if ultimaPrediccion: # in case the camera dont have predictions
                    predicciones.append(ultimaPrediccion.json())
            pasillo["predicciones"] = predicciones
            del pasillo['camaras']

        return {'pasillos': allPasillos}, 200