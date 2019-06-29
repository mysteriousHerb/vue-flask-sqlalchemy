from flask import Flask, render_template, jsonify, request, send_from_directory, session
from flask_restful import Resource, Api
from flask_cors import CORS

from flask_sqlalchemy import SQLAlchemy
# specific blob datatype for binary
from sqlalchemy.dialects.sqlite import BLOB
# https://flask-marshmallow.readthedocs.io/en/latest/
from flask_marshmallow import Marshmallow

from werkzeug.utils import secure_filename
import os
import time
import shutil
import hashlib
import pickle
import json

from config import Config
import face_recognition
from  face_recognition_helper import  FaceReconHelperClassBuilder
from hashing_helper import *


# https://flaskvuejs.herokuapp.com/sqlalchemy
app = Flask(__name__)
CORS(app, expose_headers=["x-suggested-filename", "x-suggested-filetype"])

# load settings from the config.py
app.config.from_object(Config)
# for RESTful api
api = Api(app)
#  init db object
db = SQLAlchemy(app)
# marshmallow converting complex datatypes, such as objects, to and from native Python datatypes
ma = Marshmallow(app)

# Create the database model  https://www.lucidchart.com/pages/database-diagram/database-design#discovery__top
# logical structure of a database and manner data can be stored, organized and manipulated.
class Todo(db.Model):
    # Use Column to define a column.
    id = db.Column("todo_id", db.Integer, primary_key=True)
    content = db.Column(db.String)
    done = db.Column(db.Boolean)
    # def __init__ is optional:
    # SQLAlchemy adds an implicit constructor to accept keyword arguments for all its columns and relationships


# Integration with Flask-SQLAlchemy and marshmallow-sqlalchemy
# ModelSchema that generates fields based on the model class Meta option
class TodoSchema(ma.ModelSchema):
    # class Meta options are a way to configure and modify a Schema's behavior.
    class Meta:
        model = Todo


class FileEntry(db.Model):
    id = db.Column("file_id", db.Integer, primary_key=True)
    name = db.Column(db.String)
    filepath = db.Column(db.String)


class FileEntrySchema(ma.ModelSchema):
    class Meta:
        model = FileEntry


class DescriptorEntry(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    user_name = db.Column(db.String)
    salt1 = db.Column(db.String)
    descriptor_hash = db.Column(db.String)
    user_descriptor_hash = db.Column(db.String)
    server_descriptor = db.Column(db.String)

class DescriptorEntrySchema(ma.ModelSchema):
    class Meta:
        model = DescriptorEntry


# if the database does not exist, use db.create_all()
def initialize():
    try:
        Todo.query.get(1)
        FileEntry.query.get(1)
    except:
        print("creating database..")
        db.create_all()
        # # put some place holder data
        # todo0 = Todo(content="buy food", done=False)
        # FileEntry.query.get(1)
        # file_entry_0 = FileEntry(name="Tian", filepath='C:')

        # # add and then commit to apply changes
        # db.session.add(todo0)
        # db.session.add(file_entry_0)
        # db.session.commit()
        # # delete use: db.session.delete(me)

    if not os.path.exists(app.config["UPLOAD_FOLDER"]):
        print("creating upload folder")
        os.makedirs(app.config["UPLOAD_FOLDER"])

    if not os.path.exists(app.config["TEMP_FOLDER"]):
        print("creating temp folder")
        os.makedirs(app.config["TEMP_FOLDER"])


def query_database():
    todos = Todo.query.all()
    todos_schema = TodoSchema(many=True)
    # convert the sqlresult into python dictionary that can be jsonify
    output = todos_schema.dump(todos)
    return output.data


def modify_todo(id=-1, content="", done=False, delete=False):
    if id == -1:
        # if the id is not specified, then we add a new item
        new_todo = Todo(content=content, done=done)
        db.session.add(new_todo)
    else:
        # if the id already exist, then modify the existing item
        existing_todo = Todo.query.get(id)
        if delete == True:
            db.session.delete(existing_todo)
        else:
            existing_todo.content = content
            existing_todo.done = done

    # apply changes
    db.session.commit()


class todo_database_access(Resource):
    def get(self):
        # the arguments for the function is given by the URL
        # curl http://localhost:5000
        output = query_database()
        return jsonify(output)

    def post(self):
        # accept argument by parsing the packages
        todo_args = request.get_json()
        # print(todo_args)
        modify_todo(**todo_args)
        return jsonify(status="modify success")


ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg"]


def allowed_file(filename):
    # string.rsplit(separator, max) Specifies how many splits to do.
    if "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS:
        return True
    else:
        return False


class upload_file(Resource):
    def post(self):
        file = request.files.get("file")
        print(file)
        if file:
            if file.filename == "":
                return {"message": "No file found", "status": "error"}

            elif allowed_file(file.filename) is True:
                # https://werkzeug.palletsprojects.com/en/0.15.x/utils/#werkzeug.utils.secure_filename
                filename = secure_filename(file.filename)
                filename_no_extension = filename.rsplit(".", 1)[0]

                existed_entry = FileEntry.query.filter_by(
                    name=filename_no_extension
                ).first()
                if existed_entry is None:
                    file_entry = FileEntry(
                        name=filename_no_extension,
                        filepath=os.path.join(app.config["UPLOAD_FOLDER"], filename),
                    )
                    db.session.add(file_entry)
                else:
                    # if the name  already exist, remove the existing file and update the db entry
                    os.remove(existed_entry.filepath)
                    existed_entry.filepath = os.path.join(
                        app.config["UPLOAD_FOLDER"], filename
                    )
                db.session.commit()

                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

                return {
                    "filename": filename,
                    "message": "file uploaded",
                    "status": "success",
                }

        # same api can accept other arguments for file system modification, using json to communicate
        file_upload_args = request.get_json()
        if "remove_file" in file_upload_args:
            filename = file_upload_args["remove_file"]
            filename = secure_filename(filename)
            filename_no_extension = filename.rsplit(".", 1)[0]
            existed_entry = FileEntry.query.filter_by(
                name=filename_no_extension
            ).first()
            db.session.delete(existed_entry)
            db.session.commit()
            try:
                os.remove(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            except FileNotFoundError:
                print("file is already deleted")


class download_file(Resource):
    # http://flask.pocoo.org/docs/1.0/patterns/fileuploads/
    def get(self, filename):
        response = send_from_directory(app.config["UPLOAD_FOLDER"], filename)
        response.headers["x-suggested-filename"] = filename.split(".")[0]
        response.headers["x-suggested-filetype"] = filename.split(".")[1]
        # https://stackoverflow.com/questions/41543951/how-to-change-downloading-name-in-flask
        # to pass the filename as header to frontend, we need to solve by CORS setting
        return response

class existing_files(Resource):
    def get(self):
        file_entries = FileEntry.query.all()
        file_entries_schema = FileEntrySchema(many=True)
        output = file_entries_schema.dump(file_entries)
        print(output)
        # os.path to return tail/filename to be system agnostic
        output = [os.path.basename(item['filepath']) for item in output.data]
        return output

# GAP: ----------------------------- Face recognition related codes ----------------------------------------
class initialise_session(Resource):
    def post(self):
        # assuming vue will take care of the random_id for each session, 
        # we can store everything in the pickle file
        args = request.get_json()
        # NOTE: important parameters
        folder = os.path.join(app.config["TEMP_FOLDER"], args['session_id'])
        print('Creating a temp folder')
        os.mkdir(folder)
        json_path = os.path.join(folder, 'data.json')
        

class clean_up_session(Resource):
    ''' called before vue.js closes to remove the session folder and data '''
    def post(self):
        args = request.get_json()
        folder = os.path.join(app.config["TEMP_FOLDER"], args['session_id'])
        print('Removing the temp folder')
        shutil.rmtree(folder)


class generate_descriptor(Resource):
    ''' upload the photo and generate unknown_descriptor'''
    def post(self):
        # receive server images and save it to a temp folder
        # and generate encodings from it
        file = request.files.get("file")
        session_id = request.form.get('session_id')
        face_location = request.form.get('face_location').split(',')
        # convert face_location to usable format
        face_location = [tuple([int(float(i)) for i in face_location])]

        if file:
            if 'unknown_face' not in file.filename:
                return {"message": "No file found", "status": "error"}
            else:
                # http://flask.pocoo.org/docs/0.12/quickstart/#sessions
                filename = secure_filename(file.filename)
                folder = os.path.join(app.config["TEMP_FOLDER"], session_id)
                image_path = os.path.join(folder, filename)
                file.save(image_path)

                # use a thread to do the image processing, so we don't block the app
                # thread will also have no return value, so the file saving etc is handled by the original function
                json_path = os.path.join(folder, 'data.json')
                FaceReconHelper = FaceReconHelperClassBuilder(json_path)
                # Thread will throw file not found error?
                FaceReconHelper.GenerateDescriptor(image_path=image_path, face_location=face_location, unknown=True)

                return {
                    "status": "success",
                }


class generate_smith_key(Resource):
    ''' upload descriptor and hash it and save it to database and produce .smith key '''
    def post(self):
        # NOTE: random_id should be provided by the frontend
        file = request.files.get("file")
        # Vue formData
        user_name = request.form.get('user_name')
        session_id = request.form.get('session_id')
        face_location = request.form.get('face_location').split(',')
        # convert face_location to usable format
        face_location = [tuple([int(float(i)) for i in face_location])]
        # first generate the descriptor using the uploaded image
        if file:
            if file.filename != 'known_face.jpg':
                return {"message": "No file found", "status": "error"}
            else:
                folder = os.path.join(app.config["TEMP_FOLDER"], session_id)
                # read file without saving to local filesystem
                json_path = os.path.join(folder, 'data.json')
                FaceReconHelper = FaceReconHelperClassBuilder(json_path)
                known_descriptor = FaceReconHelper.GenerateDescriptor(image_path=file, face_location=face_location, unknown=False)
                # for the hashing and database to work on the list,
                # we convert it to list and then encode to byteformat
                # NOTE: the type is now encoded string of list
                salt1, descriptor_hash , user_descriptor, salt2, user_descriptor_hash, server_descriptor = split_and_hash_descriptor(known_descriptor)

                # Save the hashes and splited descriptor to the server
                # NOTE: the type is now string of encoded string of list, to unpack: eval(eval(descriptor).decode())
                descriptor_entry = DescriptorEntry(
                    user_name=user_name,
                    salt1=str(salt1),
                    descriptor_hash=str(descriptor_hash),
                    user_descriptor_hash=str(user_descriptor_hash),
                    server_descriptor=str(server_descriptor),
                )

                db.session.add(descriptor_entry)
                db.session.commit()

                return jsonify({"user_descriptor": str(user_descriptor), "salt2": str(salt2)})


class upload_smith_key(Resource):
    ''' upload the key contains user_descriptor and salt2 '''
    def post(self):
        file = request.files.get("file")
        session_id = request.form.get('session_id')
        if '.smith' not in file.filename:
            return {"message": "No the right file", "status": "error"}
        else:
            # the .smith file contains the key info: user_descriptor and the salt2
            user_descriptor, salt2 = read_smith_file(file)
            # user upload the half of descriptor and salt2
            # NOTE: conver the string back to bytes for hashing
            generated_user_descriptor_hash = GenerateUserDescriptorHash(eval(user_descriptor), eval(salt2))

            # NOTE: we use the user's half of descriptor's hash to look up value
            # directly query the database to find the matching hash to idetify user
            descriptor_entry = DescriptorEntry.query.filter_by(
                user_descriptor_hash=generated_user_descriptor_hash
            ).first()
            if descriptor_entry:
                # the username is fetched from database
                user_name = descriptor_entry.user_name
                # NOTE: the type is now string of encoded string of list, to unpack: eval(eval(descriptor).decode())
                server_descriptor= eval(eval(descriptor_entry.server_descriptor).decode())
                # NOTE: the type is now string of encoded string of list, to unpack: eval(eval(descriptor).decode())
                user_descriptor= eval(eval(user_descriptor).decode())

                # holographic recombine
                known_descriptor = RecombineDescriptors(user_descriptor, server_descriptor)

                # save it to data.json
                folder = os.path.join(app.config["TEMP_FOLDER"], session_id)
                json_path = os.path.join(folder, 'data.json')
                FaceReconHelper = FaceReconHelperClassBuilder(json_path)
                print(json_path)
                FaceReconHelper.LoadKnownDescriptor(known_descriptor)

                return {
                        "filename": file.filename,
                        "user_name": user_name, 
                        "message": "key uploaded successfully",
                        "status": "success",
                    }

            else:
                return {
                        "filename": file.filename,
                        "message": "something is wrong",
                        "status": "failed",
                    }
        


class compare_descriptors(Resource):
    def post(self):
        # there should be only one file
        args = request.get_json()
        print(args)
        session_id = args['session_id']
        folder = os.path.join(app.config["TEMP_FOLDER"], session_id)
        json_path = os.path.join(folder, 'data.json')
        FaceReconHelper = FaceReconHelperClassBuilder(json_path)
        compare_result = FaceReconHelper.CompareDescriptors()
        # user_name should be availble to frontend when uploaded files 
        return jsonify({'match': compare_result})







api.add_resource(todo_database_access, "/api/todo_db")
api.add_resource(upload_file, "/api/upload_file")
api.add_resource(download_file, "/api/download_file/<filename>")
api.add_resource(existing_files, "/api/existing_files")

api.add_resource(initialise_session, '/api/initialise_session')
api.add_resource(clean_up_session, '/api/clean_up_session')
api.add_resource(generate_descriptor, "/api/generate_descriptor")
api.add_resource(upload_smith_key, '/api/upload_smith_key')
api.add_resource(compare_descriptors, "/api/compare_descriptors")
api.add_resource(generate_smith_key, '/api/generate_smith_key')




if __name__ == "__main__":
    initialize()
    app.run(host="0.0.0.0", debug=True)

