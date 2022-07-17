# from re import T
from flask import Flask
# UPLOAD_FOLDER = 'uploads'


def create_app(test_config=None):
    app = Flask(__name__)
    # app.config.from_mapping(
    #     # SECRET_KEY="dev",  # RuntimeError: The session is unavailable because no secret key was set.
    #     UPLOAD_FOLDER=UPLOAD_FOLDER
    # )

    app.config["DEBUG"] = True

    if test_config is not None:
        app.config.update(test_config)

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    from tableetl.index import bp
    app.register_blueprint(bp)
    app.add_url_rule("/", endpoint="index")

    return app
