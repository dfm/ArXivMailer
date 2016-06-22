# -*- coding: utf-8 -*-

from __future__ import division, print_function

import flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON


__all__ = ["db", "Subscriber", "Abstract", "Category"]

db = SQLAlchemy()


subscriptions = db.Table("subscriptions",
    db.Column("subscriber_id", db.Integer, db.ForeignKey("subscriber.id")),
    db.Column("category_id", db.Integer, db.ForeignKey("category.id")),
)

abstract_categories = db.Table("abstract_categories",
    db.Column("abstract_id", db.Integer, db.ForeignKey("abstract.id")),
    db.Column("category_id", db.Integer, db.ForeignKey("category.id"))
)


class Subscriber(db.Model):
    __tablename__ = "subscriber"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    word_vector = db.Column(JSON)
    subscriptions = db.relationship("Category", secondary=subscriptions,
                                    backref=db.backref("subscribers",
                                                       lazy="dynamic"))

    def __init__(self, email):
        self.email = email


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
    is_parent = db.Column(db.Boolean)
    parent_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    children = db.relationship("Category", lazy="joined")

    def __init__(self, arxiv_name, is_parent):
        self.arxiv_name = arxiv_name
        self.is_parent = is_parent
