from flask import Flask, render_template, jsonify, request, send_from_directory
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from flask_cors import CORS

# https://flask-marshmallow.readthedocs.io/en/latest/
from flask_marshmallow import Marshmallow

from werkzeug.utils import secure_filename
import os


# https://flaskvuejs.herokuapp.com/sqlalchemy
app = Flask(__name__)
CORS(app)
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


# Create the database model  https://www.lucidchart.com/pages/database-diagram/database-design#discovery__top
# logical structure of a database and manner data can be stored, organized and manipulated.
class FileContents(db.Model):
    # Use Column to define a column.
    id = db.Column("file_id", db.Integer, primary_key=True)
    name = db.Column(db.String)
    filepath = db.Column(db.String)
    # def __init__ is optional:
    # SQLAlchemy adds an implicit constructor to accept keyword arguments for all its columns and relationships


# if the database does not exist, use db.create_all()
def initialize_database():
    try:
        Todo.query.get(1)
    except:
        db.create_all()
        # put some place holder data
        todo1 = Todo(content="buy food", done=False)
        todo2 = Todo(content="cook food", done=False)
        # add and then commit to apply changes
        db.session.add(todo1)
        db.session.add(todo2)
        db.session.commit()
        # delete use: db.session.delete(me)


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
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


class upload_file(Resource):
    # https://github.com/flask-restful/flask-restful/issues/485
    # http://flask.pocoo.org/docs/1.0/patterns/fileuploads/
    # accept argument by parsing the packages
    def post(self):
        # curl http://localhost:5000/upload --data-binary "file=@test.txt" -X POST
        # curl -F ‘data=@test.txt’ http://localhost:5000/upload
        # only check when a file is uploaded https://www.programcreek.com/python/example/51528/flask.request.files
        if 'file' in request.files:
            file = request.files["file"]
            # in case of empty file
            if file.filename == "":
                return {"message": "No file found", "status": "error"}

            elif allowed_file(file.filename):
                # https://werkzeug.palletsprojects.com/en/0.15.x/utils/#werkzeug.utils.secure_filename
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
                return {
                    "filename": filename,
                    "message": "file uploaded",
                    "status": "success",
                }
        # same api can accept other arguments for file system modification
        file_args = request.get_json()
        print(file_args)

        if "cancel_upload" in file_args:
            filename = file_args["cancel_upload"]
            try:
                os.remove(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            except:
                print("file not exist")


class download_file(Resource):
    # http://flask.pocoo.org/docs/1.0/patterns/fileuploads/
    def get(self):
        return send_from_directory(app.config["UPLOAD_FOLDER"], "alex.jpg")


api.add_resource(todo_database_access, "/todo_db")
api.add_resource(upload_file, "/upload_file")
api.add_resource(download_file, "/download_file")


if __name__ == "__main__":
    # initialize_database()
    # query_database()
    app.run(debug=True)
