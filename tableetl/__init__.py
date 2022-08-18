from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="dev",  # RuntimeError: The session is unavailable because no secret key was set.
    )

    if test_config is not None:
        app.config.update(test_config)

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    from index import bp
    app.register_blueprint(bp)
    # app.add_url_rule("/", endpoint="index")

    return app

app = Flask(__name__)