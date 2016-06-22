# -*- coding: utf-8 -*-

import flask
import random

__all__ = ["create_app"]


def before_first_request():
    pass

def page_not_found(e):
    return flask.render_template(
        "404.html",
        bg_img="https://images.unsplash.com/gifs/fail/fail-{0}.gif".format(
            random.randint(1, 9)
        )
    ), 404

def create_app(config_object="arxivmail.config.ProductionConfig"):
    app = flask.Flask(__name__)
    app.config.from_object(config_object)

    # Set up the database.
    from .models import db
    db.init_app(app)

    app.before_first_request(before_first_request)
    app.register_error_handler(404, page_not_found)

    # Bind the blueprints.
    from .web import web
    app.register_blueprint(web)

    # from .api import api
    # app.register_blueprint(api)

    return app
