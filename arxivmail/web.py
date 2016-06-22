# -*- coding: utf-8 -*-

import flask

from .models import db, Subscriber, Category

__all__ = ["web"]

web = flask.Blueprint("web", __name__)

@web.route("/", methods=["GET", "POST"])
def index():
    if flask.request.method == "POST":
        email = flask.request.form.get("email", None)
        if email is None:
            flask.flash("Missing email address.")
        category = flask.request.form.get("category", None)
        if category is None:
            flask.flash("Missing arXiv category.")
        if email is not None and category is not None:
            category = category.strip()
            email = email.strip()
            cat = Category.query.filter_by(arxiv_name=category).first()
            user = Subscriber.query.filter_by(email=email).first()
            if user is None:
                user = Subscriber(email)
            if cat in user.subscriptions:
                flask.flash("Already subscribed to {0}".format(category))
            else:
                user.subscriptions.append(cat)
                db.session.add(user)
                db.session.commit()
                flask.flash("{0} subscribed to {1}".format(email, category))

    categories = Category.query.order_by("arxiv_name").all()
    return flask.render_template("index.html", categories=categories)


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
        print(sender, body)
        for line in body.splitlines():
            print(sender, line.strip())
            do_subscribe(sender, line.strip())

    return sender

@web.route("/subscribe/<category_name>")
def subscribe(category_name):
    email = flask.request.args.get("email", None)
    if email is None:
        return "Missing required argument 'email' or 'category'", 400

    if do_subscribe(email, category_name):
        return "Subscribed {0} to {1}".format(email, category_name)
    return "Failed"
