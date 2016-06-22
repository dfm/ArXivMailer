# -*- coding: utf-8 -*-

import json
import random
import pkgutil
from datetime import datetime, timedelta

import flask
from flask_script import Command, Option

from .oai import download
from .mail import send_email
from .models import db, Category, Subscriber, Abstract, subscriptions

__all__ = [
    "CreateTablesCommand", "DropTablesCommand", "RunMailerCommand",
]


class CreateTablesCommand(Command):
    def run(self):
        db.create_all()

        # Create the list of all
        data = pkgutil.get_data("arxivmail",
                                "data/categories.txt").decode("ascii")
        for cat in data.splitlines():
            parent = Category.query.filter_by(
                arxiv_name=cat.split(".")[0]).first()
            if parent is None:
                parent = Category(cat.split(".")[0], True)
                db.session.add(parent)
            if "." in cat:
                if Category.query.filter_by(arxiv_name=cat).count() == 0:
                    child = Category(cat, False)
                    db.session.add(child)
                    parent.children.append(child)
        db.session.commit()


class DropTablesCommand(Command):
    def run(self):
        db.drop_all()


class RunMailerCommand(Command):

    option_list = (
        Option("-f", "--file", dest="test_file", required=False),
    )

    def run(self, test_file=None):
        if test_file is None:
            since = (datetime.utcnow() + timedelta(-1)).strftime("%Y-%m-%d")
            data = [abstract for abstract in download(since)]
        else:
            with open(test_file, "r") as f:
                data = json.load(f)

        for user in Subscriber.query.all():
            cnms = set([sub.arxiv_name for sub in user.subscriptions])
            abstracts = dict()
            for entry in data:
                cats = entry["categories"]
                cats += [c.split(".")[0] for c in cats]
                if len(cnms & set(cats)):
                    abstracts[entry["id"]] = entry
            # abstracts = list(abstracts.values())
            abstracts = [a for a in sorted(abstracts.values(), key=lambda o:
                                           (o["created"], o["id"]))]
            abstracts = abstracts[::-1]
            # random.shuffle(abstracts)
            # print(abstracts[-1])

            html_body = flask.render_template("email.html",
                                              abstracts=abstracts)
            # print(abstracts[0])
            # print(html_body)

            send_email(user.email, "Email", html_body, "Some text")
