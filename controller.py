#!/usr/bin/env python
# -*- coding:utf-8 -*-


from peewee import IntegrityError

from model import User, Post, Comment, Up, Sensitive
from app import app


try:
    dup_check_list = range(app.config.get('DUP_MAX_SIZE'))
    pre_comment = Comment.select().order_by(Comment.created_at.desc()).limit(app.config.get('DUP_MAX_SIZE'))
    for item in pre_comment:
        dup_check_list.pop(0)
        dup_check_list.append(item.text)

    sensitive_list = [i.word for i in Sensitive.select()]

    recent_comments = Comment.select() \
        .group_by(Comment.ip) \
        .order_by(Comment.created_at.desc()) \
        .limit(app.config.get('RCTC_MAX_SIZE'))
except Exception, err:
    app.logger.warning(err)


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
    for word in sensitive_list:
        content = content.replace(word, '*' * len(word))
    return content


def comment_check(content):
    dup_res = duplicate_check(content)
    if not dup_res:
        return None
    sen_res = sensitive_check(dup_res)
    return sen_res