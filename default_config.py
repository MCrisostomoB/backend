import os

CORS_HEADERS = 'Content-Type'
SQLALCHEMY_DATABASE_URI = "postgres://zazyvjwaxgvnzj:84f5ca096b3fd01e832fbfb12d657b7ec2de7eb436de40cee42c534f1b96517d@ec2-54-157-234-29.compute-1.amazonaws.com:5432/d9c3224elv7c3r"
SQLALCHEMY_TRACK_MODIFICATIONS= False
PROPAGATE_EXCEPTIONS=True
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
UPLOADED_IMAGES_DEST = os.path.join("static", "images")