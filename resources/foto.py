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

    def post(self):
        data = Foto.parser.parse_args()
        camara_id = data['camara_id']
        folder = f'camaras_{camara_id}'

        camara = CamaraModel.findByID(camara_id)

        if camara is None:
            return {'message': f'La cámara {camara_id} no existe'}, 400 

        try:
            os.remove(image_helper.get_path(folder+"/"+data['image'], folder=folder))
        except:
            print("no lo borro", flush = True)
            pass
        try:
            image_path = image_helper.save_image(data['image'],folder=folder)
            basename = image_helper.get_basename(image_path) 
            return {'message': f'El archivo \'{basename}\' ha sido subido correctamente'}, 201 
        
        except UploadNotAllowed:
            extension = image_helper.get_extension(data['image'])
            return {'message': f'La extension \'{extension}\' del archivo no esta permitida'}, 400
        
    def get(self):
        data = Foto.parser_get.parse_args()
        camara_id = data['camara_id']
        folder = f'camaras_{camara_id}'

        camara = CamaraModel.findByID(camara_id)

        try:
            return send_file(image_helper.get_path(camara.path, folder= folder))
        except FileNotFoundError:
            return {'message': 'La imagen no fue encontrada'}
