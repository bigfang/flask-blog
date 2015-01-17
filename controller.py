#!/usr/bin/env python
# -*- coding:utf-8 -*-


from model import User, Post, Comment, Up


def up(post_id, ip):
    record = Post.select().where(Post.id == post_id).get()
    print record.up_time
    record.up_time += 1
    ret = record.up_time
    record.save()

    Up.create(ip=ip, post=post_id)
    return ret
