from flask import request, jsonify
from flask_restful import Resource, reqparse
from models import db
from models.camara import CamaraModel
from models.pasillo import PasilloModel
from models.products import ProductModel
from sqlalchemy.exc import SQLAlchemyError

class Camara(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('nombre',
        type=str,
        required=False,
        location='json'
    )
    parser.add_argument('pasillo_id',
        type=int,
        required=False,
        location='json'
    )

    parser.add_argument('path',
        type=str,
        required=False,
        location='json'
    )

    def put (self,id = None):
        data = Camara.parser.parse_args()
        if id is not None:
            camara = CamaraModel.findByID(id)
            camara.nombre = data['nombre']
            camara.pasillo_id = data['pasillo_id']
            camara.path = data['path']
            camara.save_to_db()
            return "camara modificada", 200

    # add new element
    def post(self):
        data = Camara.parser.parse_args()

        # create new element
        new_camara = CamaraModel(**data)
        message = 'Ha ocurrido un error al ingresar a la base de datos'
        try:
            new_camara.save_to_db()
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return error
            # return {
            #     'message': message
            # }
        
        return new_camara.json(), 201 #201 created
    
    # get all
    def get(self,id = None):
        if id is not None:
            camara = CamaraModel.findByID(id)
            productos = ProductModel.find_by_camara(id)
            products = []
            for i in productos:
                products.append({'id':i.id,'nombre_producto': i.product_name,'coordenadas':i.coordinates})
            return {'id_camara':id,'url_foto':camara.path, 'productos': products}    

        else:
            return {'camara': [x.json() for x in CamaraModel.find_all()]}, 200

    