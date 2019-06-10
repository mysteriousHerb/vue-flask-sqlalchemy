from flask import Flask, render_template, jsonify, request, send_from_directory
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_cors import CORS

# https://flask-marshmallow.readthedocs.io/en/latest/
from flask_marshmallow import Marshmallow

from werkzeug.utils import secure_filename
import os
import shutil


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


# if the database does not exist, use db.create_all()
def initialize():
    try:
        Todo.query.get(1)
        FileEntry.query.get(1)        
    except:
        print('creating database..')
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
    
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        print('creating upload folder')
        os.makedirs(app.config['UPLOAD_FOLDER'])


def query_database():
    todos = Todo.query.all()
    todos_schema = TodoSchema(many=True)
    # convert the sqlresult into python dictionary that can be jsonify
    output = todos_schema.dump(todos)
    return output


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


ALLOWED_EXTENSIONS = ["txt", "pdf", "png", "jpg", "jpeg", "gif"]

def allowed_file(filename):
    # string.rsplit(separator, max) Specifies how many splits to do.
    if "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS:
        return True
    else:
        return False


class upload_file(Resource):
    def post(self):
        file = request.files.get('file')
        if file:
            if file.filename == "":
                return {"message": "No file found", "status": "error"}

            elif allowed_file(file.filename) is True:
                # https://werkzeug.palletsprojects.com/en/0.15.x/utils/#werkzeug.utils.secure_filename
                filename = secure_filename(file.filename)
                filename_no_extension = filename.rsplit(".", 1)[0]

                existed_entry = FileEntry.query.filter_by(name=filename_no_extension).first()
                if existed_entry is None:
                    file_entry = FileEntry(name=filename_no_extension, filepath=os.path.join(app.config["UPLOAD_FOLDER"], filename))
                    db.session.add(file_entry)
                else:
                    # if the name  already exist, remove the existing file and update the db entry
                    os.remove(existed_entry.filepath)
                    existed_entry.filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                db.session.commit()

                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

                return {
                    "filename": filename,
                    "message": "file uploaded",
                    "status": "success",
                }

        # same api can accept other arguments for file system modification, using json to communicate
        file_upload_args = request.get_json()
        print(file_upload_args)

        if "remove_file" in file_upload_args:
            filename = file_upload_args["remove_file"]
            filename = secure_filename(filename)
            filename_no_extension = filename.rsplit(".", 1)[0]
            existed_entry = FileEntry.query.filter_by(name=filename_no_extension).first()
            db.session.delete(existed_entry)
            db.session.commit()
            try:
                os.remove(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            except FileNotFoundError:
                print('file is already deleted')

class download_file(Resource):
    # http://flask.pocoo.org/docs/1.0/patterns/fileuploads/
    def get(self):
        response =  send_from_directory(app.config["UPLOAD_FOLDER"], 'download.jpg')
        response.headers['x-suggested-filename'] = 'download.jpg'.split('.')[0]
        response.headers['x-suggested-filetype'] = 'download.jpg'.split('.')[1]
        # https://stackoverflow.com/questions/41543951/how-to-change-downloading-name-in-flask
        # to pass the filename as header to frontend, we need to solve by CORS setting

        return response
    
    def post(self):
        args = request.get_json()
        if 'index_files' in args:
            if args['index_files'] is True:
                file_entries = FileEntry.query.all()
                file_entries_schema = FileEntrySchema(many=True)
                output = file_entries_schema.dump(file_entries)
                return output

        if 'change_file' in args:
            filename_no_extension = args['change_file']
            existed_entry = FileEntry.query.filter_by(name=filename_no_extension).first()
            filepath = existed_entry.filepath
            shutil.copy2(filepath, os.path.join(app.config["UPLOAD_FOLDER"], 'download.jpg'))

            return 200
            

api.add_resource(todo_database_access, "/todo_db")
api.add_resource(upload_file, "/upload_file")
api.add_resource(download_file, "/download_file")


if __name__ == "__main__":
    initialize()
    # query_database()
    app.run(debug=True)
