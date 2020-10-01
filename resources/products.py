from flask import request, jsonify
import json
import ast 

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
    parser.add_argument('crear',
        type = list,
        required = False,
        location = 'json'
    )
    parser.add_argument('actualizar',
        type = list,
        required = False,
        location = 'json'
    )
    parser.add_argument('eliminar',
        type = list,
        required = False,
        location = 'json'
    )

    def put(self):
        data = Product.parser.parse_args()
        for i in data['eliminar']:
            producto = ProductModel.find_by_id(i)
            producto.coordinates = ""
            producto.save_to_db()
        for i in data['actualizar']:
            product =  ast.literal_eval(i)
            producto = ProductModel.find_by_id(data['id'])
            producto.product_name = producto['nombre_producto']
            producto.pasillo_id = data['pasillo_id']
            producto.camara_id = data['camara_id']
            producto.coordinates = producto['coordenadas']
            producto.save_to_db()
        for i in data['crear']:
            product = ast.literal_eval(i)
            new_product = ProductModel(product['nombre_producto'],data['pasillo_id'],product['coordenadas'],data['camara_id'])
            new_product.save_to_db()
        return "productos modificado", 200

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



    