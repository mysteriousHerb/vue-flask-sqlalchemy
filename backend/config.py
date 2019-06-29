import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///smith.db'
    SECRET_KEY = os.environ.get("SECRET_KEY") or "super-secret-key"
    CSRF_ENABLED = True
    UPLOAD_FOLDER = 'saved_files'
    TEMP_IMG_FOLDER = os.path.join('temp', 'images')
    DESCRIPTORS_FOLDER = os.path.join('temp', 'descriptor')
    TEMP_FOLDER = 'temp'

    THREADED=True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


