# -*- coding: utf-8 -*-

import flask

from .models import db, Subscriber, Category

__all__ = ["web"]

web = flask.Blueprint("web", __name__)

@web.errorhandler(404)
def page_not_found(e):
    return flask.render_template(
        "404.html", bg_img="https://images.unsplash.com/gifs/fail/fail-5.gif"
    ), 404


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
    categories = Category.query.order_by("arxiv_name").all()
    return flask.render_template("manage.html", categories=categories,
                                 user=user)
