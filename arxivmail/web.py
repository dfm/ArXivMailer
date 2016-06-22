# -*- coding: utf-8 -*-

import flask

from .models import db, Subscriber, Category

__all__ = ["web"]

web = flask.Blueprint("web", __name__)

@web.route("/")
def index():
    return "Hello"

@web.route("/subscribe/<category_name>")
def subscribe(category_name):
    email = flask.request.args.get("email", None)
    if email is None:
        return "Missing required argument 'email' or 'category'", 400

    category = Category.query.filter_by(
        arxiv_name=category_name.strip()).first()
    if category is None:
        return "Unknown category '{0}'".format(category_name), 400

    user = Subscriber.query.filter_by(email=email).first()
    if user is None:
        user = Subscriber(email)
    if category in user.subscriptions:
        return "{0} already subscribed to {1}".format(email, category_name)
    user.subscriptions.append(category)
    db.session.add(user)
    db.session.commit()

    return "Subscribed {0} to {1}".format(email, category_name)
