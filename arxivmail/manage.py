# -*- coding: utf-8 -*-

import pkgutil

from flask_script import Command, Option

from .models import db, Category

__all__ = [
    "CreateTablesCommand", "DropTablesCommand",
]


class CreateTablesCommand(Command):
    def run(self):
        db.create_all()
        data = pkgutil.get_data("arxivmail",
                                "data/categories.txt").decode("ascii")
        for cat in data.splitlines():
            db.session.add(Category(cat))
        db.session.commit()


class DropTablesCommand(Command):
    def run(self):
        db.drop_all()


# class UpdateCommand(Command):

#     option_list = (
#         Option("-s", "--since", dest="since", required=False),
#     )

#     def run(self, since):
#         update(since=since)
