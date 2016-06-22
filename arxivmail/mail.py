# -*- coding: utf-8 -*-

from __future__ import division, print_function

import flask
import requests
from werkzeug.datastructures import MultiDict

__all__ = ["send_email"]


def send_email(to, subject, html_body, text_body=None, from_=None):
    if from_ is None:
        from_ = "ArXiv Mailer <mailer@arxiv.dfm.io>"
    url = "https://api.mailgun.net/v3/mailgun.arxiv.dfm.io/messages"
    data = MultiDict([
        ("from", from_),
        ("to", to),
        ("subject", subject),
        ("html", html_body),
        ("text", text_body),
    ])

    r = requests.post(url, data=data,
                      auth=("api",
                            flask.current_app.config["MAILGUN_API_KEY"]))
    r.raise_for_status()
