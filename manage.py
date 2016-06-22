#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_script import Manager

from arxivmail import create_app
from arxivmail.manage import (
    CreateTablesCommand, DropTablesCommand, RunMailerCommand,
)

if __name__ == "__main__":
    manager = Manager(create_app)

    manager.add_command("create", CreateTablesCommand())
    manager.add_command("drop", DropTablesCommand())
    manager.add_command("mail", RunMailerCommand())

    manager.run()
