import os

from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin
from flask_uploads import configure_uploads, patch_request_class

from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

load_dotenv(".env", verbose=True) # import .env file
app.config.from_object("default_config")
app.config.from_envvar("APPLICATION_SETTINGS")

from models import db
from models import camara, pasillo, prediccion,products
db.init_app(app)
migrate = Migrate(app, db)

from resources.prediction import Prediction
from resources.foto import Foto
from resources.pasillo import Pasillo
from resources.camara import Camara
from resources.products import Product

from libs.image_helper import IMAGE_SET

@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
configure_uploads(app, IMAGE_SET)
api = Api(app)
# api.add_resource(Pasillo, '/pasillo/<int:numero>')
api.add_resource(Pasillo, '/pasillo','/pasillo/<apitype>/<int:id>', '/pasillo/<int:id>','/pasillo/<apitype>')
api.add_resource(Camara, '/camara',"/camara/<int:id>")
api.add_resource(Prediction, '/prediccion')
api.add_resource(Foto, '/foto')
api.add_resource(Product, '/producto','/producto/<apitype>/<int:id>','/producto/<name>','producto/<int:id>')


# api.add_resource(Cuadrado, '/cuadrado')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port =int(os.environ.get('PORT', 5000)) ,debug=True)
