# from re import T
from flask import Flask
# UPLOAD_FOLDER = 'uploads'

app = Flask(__name__)
    # app.config.from_mapping(
    #     # SECRET_KEY="dev",  # RuntimeError: The session is unavailable because no secret key was set.
    #     UPLOAD_FOLDER=UPLOAD_FOLDER
    # )

app.config['SECRET_KEY'] = 'b43e2ce96eac84c9c5690f4c315f2fd3'
app.config["DEBUG"] = True

@app.route("/hello")
def hello():
    return "Hello, World!"

from tableetl.index import bp
app.register_blueprint(bp)
app.add_url_rule("/", endpoint="index")

