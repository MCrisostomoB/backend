from flask import request, jsonify
import json
from flask_restful import Resource, reqparse
from models import db
from models.prediccion import PrediccionModel
from models.pasillo import PasilloModel
from models.products import ProductModel


class Product(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('pasillo_id',
        type=int,
        required=True,
        help="El campo pasillo_id no puede estar vacio.",
        location='json'
    )
    parser.add_argument('camara_id',
        type=int,
        required=True,
        help="El campo pasillo_id no puede estar vacio.",
        location='json'
    )
    parser.add_argument('product_name',
        type=str,
        required=False,
        location='json'
    )

    parser.add_argument('coordinates',
        type=str,
        required=False,
        location='json'
    )

    def put(self,id= None):
        data = Product.parser.parse_args()
        if id is not None:
            producto = ProductModel.find_by_id(id)
            producto.product_name = data['product_name']
            producto.pasillo_id = data['pasillo_id']
            producto.camara_id = data['camara_id']
            producto.coordinates = data['coordinates']
            producto.save_to_db()
            return "producto modificado", 200

    # add new element
    def post(self):
        data = Product.parser.parse_args()

        # find pasillo
        pasillo = PasilloModel.findByID(data['pasillo_id'])
        if not pasillo:
            return f"No se encontro el pasillo: {data['pasillo_id']}", 404

        # create new element
        new_product = ProductModel(**data)
        message = 'Ha ocurrido un error al ingresar a la base de datos'
        try:
            new_product.save_to_db()
        except:
            return {
                'message': message
            }
        
        return new_product.json(), 201 #201 created
    
    # get all
    def get(self,apitype=None,id=None,name=None):
        if apitype is not None:
            if apitype == "pasillo":
                if id is not None:
                    dic = dict()
                    dic['products'] = []
                    for x in ProductModel.find_by_pasillo(id):
                        dic['products'].append(x.json())
                        area = PrediccionModel.findByProductId(x.id)
                        if area is not None:
                            a = {"porcentaje_vacio": area.area}
                            dic['products'][-1].update(a)
                        else:
                            a = {"porcentaje_vacio": 0}
                            dic['products'][-1].update(a)
                    return dic,200
            elif apitype == "camara":
                if id is not None:
                    return {'producto': [x.json() for x in ProductModel.find_by_camara(id)]},200
        if name is not None:
            return {'producto': [x.json() for x in ProductModel.find_by_name(name)]},200
        else:
            return {'productos': [x.json() for x in ProductModel.find_all()]}, 200

    def delete(self,id):
        product = ProductModel.find_by_id(id)[0]
        message = 'Ha ocurrido un error al intentar eliminar el producto'
        try:
            product.delete_from_db()
        except:
            return {
                'message': message
            }
        return 'deleted', 200 #201 created



    