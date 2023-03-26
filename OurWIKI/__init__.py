from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='DEV',
        DATABASE='OurWIKI/OurWIKI_DATABASE.sqlite'
    )

    from OurWIKI import database
    database.init_app(app)

    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .post import post_blueprint
    app.register_blueprint(post_blueprint)

    return app
