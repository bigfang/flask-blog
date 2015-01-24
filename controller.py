#!/usr/bin/env python
# -*- coding:utf-8 -*-


from peewee import IntegrityError

from model import User, Post, Comment, Up
from app import app


dup_check_list = [0]
pre_comment = Comment.select().order_by(Comment.created_at.desc()).limit(app.config.get('Q_MAX_SIZE'))
for item in pre_comment:
    dup_check_list.append(item.text)


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
    if content in dup_check_list:
        return None
    else:
        dup_check_list.pop(0)
        dup_check_list.append(content)
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