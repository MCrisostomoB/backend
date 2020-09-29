import os

CORS_HEADERS = 'Content-Type'
SQLALCHEMY_DATABASE_URI = "postgres://gcgyrdxfjfbosl:f9c289eb8b810217b4bd5de08b07d97fe1ba7573e454c59c9c96c72ab73c2207@ec2-35-169-92-231.compute-1.amazonaws.com:5432/d9bpn34vt1lgtb"
SQLALCHEMY_TRACK_MODIFICATIONS= False
PROPAGATE_EXCEPTIONS=True
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
UPLOADED_IMAGES_DEST = os.path.join("static", "images")
