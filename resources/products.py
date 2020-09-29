from flask import request, jsonify
from flask_restful import Resource, reqparse
from models import db
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
    parser.add_argument('area',
        type=str,
        required=False,
        location='json'
    )

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
    def get(self,id=None,name=None):
        if id is not None:
            return {'producto':[x.json() for x in ProductModel.find_by_pasillo(id)]},200
        elif name is not None:
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



    