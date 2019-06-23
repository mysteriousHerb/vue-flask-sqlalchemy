from flask import Flask, session, redirect, url_for, escape, request, jsonify
from flask_restful import Resource, Api
from face_recognition_helper import FaceReconHelperClassBuilder
from hashing_helper import *
import json
import os
import pickle
import random
import string
from config import Config

from flask_cors import CORS
import shutil


app = Flask(__name__)
app.secret_key = 'super_useful_key'
# load settings from the config.py
app.config.from_object(Config)
CORS(app)

api = Api(app)


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


class initialise_session(Resource):
    def post(self):
        # assuming vue will take care of the random_id for each session, 
        # we can store everything in the pickle file
        args = request.get_json()
        # NOTE: important parameters
        folder = os.path.join(app.config["TEMP_FOLDER"], args['session_id'])
        os.mkdir(folder)
        json_path = os.path.join(folder, 'data.json')
        

class clean_up_session(Resource):
    ''' called before vue.js closes to remove the session folder and data '''
    def post(self):
        args = request.get_json()
        folder = os.path.join(app.config["TEMP_FOLDER"], args['session_id'])
        print('removing the folder')
        shutil.rmtree(folder)


class check_session(Resource):
    def post(self):
        args = request.get_json()
        return jsonify({'session_id': args['session_id']})


class file_upload(Resource):
    def post(self):
        # read file without saving
        file = request.files.get("file")
        user_name = request.form.get('user_name', 'tester')
        folder = 'temp'
        json_path = os.path.join(folder, 'temp.json')
        FaceReconHelper = FaceReconHelperClassBuilder(json_path)
        known_descriptor = FaceReconHelper.GenerateDescriptor(image_path=file, unknown=False)
        salt1, descriptor_hash , user_descriptor, salt2, user_descriptor_hash, server_descriptor = split_and_hash_descriptor(known_descriptor)
        return jsonify({"user_descriptor": str(user_descriptor), "salt2": str(salt2)})


api.add_resource(initialise_session, "/api/initialise_session")
api.add_resource(clean_up_session, "/api/clean_up_session")
api.add_resource(check_session, "/api/check_session")
api.add_resource(file_upload, "/api/file_upload")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

