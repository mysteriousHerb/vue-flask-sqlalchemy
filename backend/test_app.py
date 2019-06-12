from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"

if __name__ == "__main__":
    # If you have the debugger disabled or trust the users on your network, 
    # you can make the server publicly available simply by
    #  adding --host=0.0.0.0 to the command line
    app.run(host='0.0.0.0', debug=False)