import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SECRET_KEY = os.environ.get("SECRET_KEY") or "super-secret-key"
    CSRF_ENABLED = True
    UPLOAD_FOLDER = 'saved_files'
    TEMP_FOLDER = 'temp'
    KNOWN_DESCRIPTORS_FOLDER = 'known_descriptors'
    THREADED=True

