from flask import request, jsonify
from flask_restful import Resource, reqparse
from models import db
from models.pasillo import PasilloModel
from models.camara import CamaraModel
from models.prediccion import PrediccionModel
from sqlalchemy.exc import SQLAlchemyError

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

    parser.add_argument('camaras',
        type =list,
        required = False,
        location = 'json'
    )

    # add new element
    def post(self):
        data = Pasillo.parser.parse_args()
        print(data,flush = True)
        # create new element
        new_pasillo = PasilloModel(data['categoria'],data['numero'])
        
        try:
            new_pasillo.save_to_db()
            if (data['camaras'] is not None):
                savedpasillo = PasilloModel.findByNumber(data['numero'])
                for i in data['camaras']:
                    camara = CamaraModel.findByID(i)
                    if(camara is not None):
                        camara.pasillo_id = i 
                        camara.save_to_db()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return error
            # return {
            #     'message': 'Ha ocurrido un error al ingresar a la base de datos'
            # }
        return new_pasillo.json(), 201 #201 created
    
    # get all
    def get(self,apitype= None, id = None):
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