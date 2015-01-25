#!/usr/bin/env python
# -*- coding:utf-8 -*-


from datetime import datetime
from functools import wraps

from flask import request, session

from model import Comment


def last_comment(func):
    @wraps(func)
    def inner(*args, **kwargs):
        if 'ip' in session:
            try:
                session['last_comment_at'] = Comment.select() \
                    .where(Comment.ip == session['ip']) \
                    .order_by(Comment.created_at.desc()) \
                    .limit(1)[0].created_at
            except:
                session['last_comment_at'] = datetime(2015, 1, 1)
        session['ip'] = request.environ['REMOTE_ADDR']
        return func(*args, **kwargs)

    return inner
