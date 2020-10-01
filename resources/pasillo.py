from flask import request, jsonify
from flask_restful import Resource, reqparse
from models import db
import json

from models.pasillo import PasilloModel
from models.products import ProductModel
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
    def put(self,id=None):
        data = Pasillo.parser.parse_args()
        if id is not None:
            pasillo = PasilloModel.findByID(id)
            pasillo.numero = data['numero']
            pasillo.categoria = data['categoria']
            for i in data['camaras']:
                camara = CamaraModel.findByID(i)
                if(camara is not None):
                    camara.pasillo_id = id 
                    camara.save_to_db()
            pasillo.save_to_db()
            return "pasillo modificado", 200

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
        if apitype is not None:
            if apitype == "admin":
                if id is not None:
                    dic = dict()
                    dic["id_pasillo"] = id
                    pasillo = PasilloModel.findByID(id)
                    dic['numero'] = pasillo.numero
                    dic['categoria'] = pasillo.categoria
                    dic['camaras'] = []
                    camaras = CamaraModel.findByIDPasillo(id)
                    for i in camaras:
                        productos = ProductModel.find_by_camara(i.id)
                        dic['camaras'].append({'id_camara':i.id,'url_foto':i.path})
                        products = []
                        for j in productos:
                            products.append({'id':j.id,'nombre_producto':j.product_name , 'coordenadas': j.coordinates})
                        
                        dic['camaras'][-1].update({'productos': products})
                    return dic ,200
                else:
                    allPasillos = []
                    for x in PasilloModel.find_all():
                        if x.numero != -1:
                            allPasillos.append(x.jsonWithCameras())
                    for pasillo in allPasillos:
                        pasillo.update({'total_camaras':len(pasillo['camaras'])})
                        del pasillo['camaras']
                    return {'pasillos': allPasillos}, 200
        elif id is not None:
            dic = dict()
            dic['camaras'] = []
            dic["id_pasillo"] = id
            pasillo = PasilloModel.findByID(id)
            dic['numero'] = pasillo.numero
            camaras = CamaraModel.findByIDPasillo(id)
            for i in camaras:
                productos = ProductModel.find_by_camara(i.id)
                dic['camaras'].append({'id_camara':i.id,'url_foto':i.path})
                products = []
                for j in productos:
                    prediccion = PrediccionModel.findByProductId(j.id)
                    if prediccion.area is not None:
                        products.append({'nombre_producto':j.product_name , 'porcentaje_vacio':prediccion.area})
                    else:
                        products.append({'nombre_producto':j.product_name , 'porcentaje_vacio':0})

                
                dic['camaras'][-1].update({'productos': products})
            return dic ,200
        else:
            retorno = []
            allPasillos =PasilloModel.find_all()
            for i in allPasillos:
                total = 0
                totalproductos = 0
                productos =  ProductModel.find_by_pasillo(i.id)
                for j in productos:
                    prediccion= PrediccionModel.findByProductId(j.id)
                    total += prediccion.area
                    totalproductos +=1
                # i['total_espacio_vacio'] = total
                retorno.append(i.json())
                if totalproductos != 0:
                    total = total/totalproductos
                retorno[-1]['total_espacio_vacio'] = total
            return retorno , 200
