# -*- coding: utf-8 -*-

import flask

from .models import db, Subscriber, Category

__all__ = ["web"]

web = flask.Blueprint("web", __name__)

@web.route("/")
def index():
    return "Hello"


@web.route("/manage/<token>")
def manage(token):
    user = Subscriber.check_token(token)
    if user is None:
        return flask.abort(404)
    return flask.render_template("unsubscribe.html", user=user)

def do_subscribe(email, category_name):
    category = Category.query.filter_by(
        arxiv_name=category_name.strip()).first()
    if category is None:
        return False

    user = Subscriber.query.filter_by(email=email).first()
    if user is None:
        user = Subscriber(email)
    if category in user.subscriptions:
        return False
    user.subscriptions.append(category)
    db.session.add(user)
    db.session.commit()
    return True

@web.route("/email_subscribe", methods=["POST"])
def email_subscribe():
    if flask.request.method == "POST":
        sender = flask.request.form.get("sender")
        body = flask.request.form.get("stripped-text", "")
        for line in body.splitlines():
            do_subscribe(sender, line.strip())

    return "nothing"

@web.route("/subscribe/<category_name>")
def subscribe(category_name):
    email = flask.request.args.get("email", None)
    if email is None:
        return "Missing required argument 'email' or 'category'", 400

    if do_subscribe(email, category_name):
        return "Subscribed {0} to {1}".format(email, category_name)
    return "Failed"
