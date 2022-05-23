from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="dev",  # RuntimeError: The session is unavailable because no secret key was set.
        DATABASE="database.db",
    )

    if test_config is not None:
        app.config.update(test_config)

    @app.route("/hello")
    def hello():
        return "Hello, World!"

    from comments import db
    db.init_app(app)

    from comments.comments import bp
    app.register_blueprint(bp)
    from comments.auth import bp
    app.register_blueprint(bp)
    app.add_url_rule("/", endpoint="index")

    return app
