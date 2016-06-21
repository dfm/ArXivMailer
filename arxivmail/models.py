# -*- coding: utf-8 -*-

from __future__ import division, print_function

from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from werkzeug.security import (
    generate_password_hash, check_password_hash
)


__all__ = ["db", "Subscriber", "Abstract", "Category"]

db = SQLAlchemy()


subscriptions = db.Table("subscriptions",
    db.Column("subscriber_id", db.Integer, db.ForeignKey("subscriber.id")),
    db.Column("category_id", db.Integer, db.ForeignKey("category.id"))
)

abstract_categories = db.Table("abstract_categories",
    db.Column("abstract_id", db.Integer, db.ForeignKey("abstract.id")),
    db.Column("category_id", db.Integer, db.ForeignKey("category.id"))
)


class Subscriber(db.Model):
    __tablename__ = "subscriber"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    email_hash = db.Column(db.String)
    word_vector = db.Column(JSON)
    subscriptions = db.relationship("Category", secondary=subscriptions,
                                    backref=db.backref("subscribers",
                                                       lazy="dynamic"))

    def __init__(self, email):
        self.email = email
        self.email_hash = generate_password_hash(email)


class Abstract(db.Model):
    __tablename__ = "abstract"

    id = db.Column(db.Integer, primary_key=True)
    arxiv_id = db.Column(db.String, unique=True)
    word_vector = db.Column(JSON)
    categories = db.relationship("Category", secondary=abstract_categories,
                                 backref=db.backref("abstracts",
                                                    lazy="dynamic"))

    def __init__(self, arxiv_id):
        self.arxiv_id = arxiv_id


class Category(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    arxiv_name = db.Column(db.String, unique=True)

    def __init__(self, arxiv_name):
        self.arxiv_name = arxiv_name
