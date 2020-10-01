from flask import request, send_file
from flask_restful import Resource, reqparse
from werkzeug.datastructures import FileStorage
from models.camara import CamaraModel
from flask_uploads import UploadNotAllowed
import os 

from flask import current_app
from libs import image_helper

class Foto(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument('image',
        type=FileStorage,
        required = True,
        help = "Este campo no puede estar vacio",
        location='files',
    )

    parser.add_argument('camara_id',
        type=int,
        required = True,
        help = "Este campo no puede estar vacio",    
    )

    parser_get = reqparse.RequestParser()

    parser_get.add_argument('camara_id',
        type=int,
        required = True,
        help = "Este campo no puede estar vacio",    
        location='args'
    )

    def post(self,apitype = None):
        if apitype is not None:
            data = Foto.parser.parse_args()
            camara_id = data['camara_id']
            if apitype == "prediccion":
                folder = f'camaras_{camara_id}'
                if(not os.path.exists(folder)):
                    os.mkdir(folder)
                camara = CamaraModel.findByID(camara_id)
                if camara is None:
                    return {'message': f'La cámara {camara_id} no existe'}, 400 
                
                # print(image_helper.get_path(data['image'], folder=folder),flush=True)
            elif apitype == "rectangulos":
                folder = f'productos/camaras_{camara_id}'
                if(not os.path.exists("productos")):
                    os.mkdir("productos")
                if(not os.path.exists(folder)):
                    os.mkdir(folder)
                camara = CamaraModel.findByID(camara_id)
                if camara is None:
                    return {'message': f'La cámara {camara_id} no existe'}, 400 
                
                # print(image_helper.get_path(data['image'], folder=folder),flush=True)
            try:
                os.remove(folder+"/foto.jpg")
            except:
                pass
            try:
                image_path = data['image'].save(folder+"/foto.jpg")
                # basename = image_helper.get_basename(image_path) 
                return {'message': f'El archivo foto.jpg ha sido subido correctamente'}, 201 
            
            except UploadNotAllowed:
                extension = image_helper.get_extension(data['image'])
                return {'message': f'La extension \'{extension}\' del archivo no esta permitida'}, 400
        
    def get(self,apitype= None):
        if apitype is not None:
            data = Foto.parser_get.parse_args()
            camara_id = data['camara_id']
            folder = ""
            if apitype == "prediccion":
                folder = f'camaras_{camara_id}'
            elif apitype == "rectangulo":   
                folder = f'productos/camaras_{camara_id}'
           
            try:
                return send_file(folder+"/foto.jpg")
            except FileNotFoundError:
                return {'message': 'La imagen no fue encontrada'}
