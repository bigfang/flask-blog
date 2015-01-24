#!/usr/bin/env python
# -*- coding:utf-8 -*-


from peewee import IntegrityError

from model import User, Post, Comment, Up
from app import app


def up(post_id, ip):
    record = Post.select().where(Post.id == post_id).get()

    try:
        Up.create(ip=ip, post=post_id)
    except IntegrityError, err:
        app.logger.error(err)
    else:
        record.up_time += 1

    ret = record.up_time
    record.save()

    return ret


def duplicate_check(content):
    return content


def sensitive_check(content):
    ret = content
    return ret


def comment_check(content):
    dup_res = duplicate_check(content)
    if not dup_res:
        return None
    sen_res = sensitive_check(dup_res)
    return sen_res