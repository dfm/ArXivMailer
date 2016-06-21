# -*- coding: utf-8 -*-

import flask

__all__ = ["web"]

web = flask.Blueprint("web", __name__)

@web.route("/")
def index():
    return "Hello"
