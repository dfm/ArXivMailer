# -*- coding: utf-8 -*-

import flask

__all__ = ["create_app"]


def before_first_request():
    pass


def create_app(config_object="arxivmail.config.ProductionConfig"):
    app = flask.Flask(__name__)
    app.config.from_object(config_object)

    # Set up the database.
    from .models import db
    db.init_app(app)

    # Before request.
    app.before_first_request(before_first_request)

    # Bind the blueprints.
    from .web import web
    app.register_blueprint(web)

    # from .api import api
    # app.register_blueprint(api)

    return app
