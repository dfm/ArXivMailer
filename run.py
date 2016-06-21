#!/usr/bin/env python
# -*- coding: utf-8 -*-

from arxivmail import create_app

if __name__ == "__main__":
    app = create_app("arxivmail.config.DevelopmentConfig")
    app.run()
