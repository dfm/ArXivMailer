# -*- coding: utf-8 -*-

import flask

from .mail import send_email
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
                db.session.add(user)
                db.session.commit()
                html_body = flask.render_template("welcome_email.html",
                                                  user=user)
                send_email(email, "Welcome", html_body)
            if cat in user.subscriptions:
                flask.flash("Already subscribed to {0}".format(category))
            else:
                user.subscriptions.append(cat)
                db.session.add(user)
                db.session.commit()
                flask.flash("{0} subscribed to {1}".format(email, category))

    categories = Category.query.order_by("arxiv_name").all()
    return flask.render_template("index.html", categories=categories)

@web.route("/confirm/<token>")
def confirm(token):
    user = Subscriber.check_token(token)
    if user is None:
        return flask.abort(404)
    user.confirmed = True
    db.session.add(user)
    db.session.commit()
    flask.flash("Confirmed {0}.".format(user.email))
    return flask.redirect(flask.url_for(".manage", token=token))

@web.route("/manage/<token>", methods=["GET", "POST"])
def manage(token):
    user = Subscriber.check_token(token)
    if user is None:
        return flask.abort(404)

    categories = Category.query.order_by("arxiv_name").all()
    cdict = dict((c.arxiv_name, c) for c in categories)

    if flask.request.method == "POST":
        cats = [cdict.get(c, None)
                for c in flask.request.form.getlist("category")]
        user.subscriptions = [c for c in cats if c is not None]

    return flask.render_template("manage.html", categories=categories,
                                 user=user)


@web.route("/unsubscribe/<token_or_email>")
def unsubscribe(token_or_email):
    user = Subscriber.query.filter_by(email=token_or_email).first()
    if user is None:
        user = Subscriber.check_token(token_or_email)
    if user is not None:
        db.session.delete(user)
        db.session.commit()
    flask.flash("Unsubscribed.")
    return flask.redirect(flask.url_for(".index"))
