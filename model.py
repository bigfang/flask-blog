#!/usr/bin/env python
# -*- coding:utf-8 -*-


from datetime import datetime

import peewee
from flask.ext.admin.contrib.peewee import ModelView

from app import app


db = peewee.SqliteDatabase(app.config.get('DATABASE'), check_same_thread=False)


class BaseModel(peewee.Model):
    class Meta:
        database = db


class User(BaseModel):
    username = peewee.CharField(max_length=80)
    email = peewee.CharField(max_length=120)
    password = peewee.CharField(max_length=9)

    def __unicode__(self):
        return self.username


class UserInfo(BaseModel):
    key = peewee.CharField(max_length=64)
    value = peewee.CharField(max_length=64)

    user = peewee.ForeignKeyField(User)

    def __unicode__(self):
        return '%s - %s' % (self.key, self.value)


class Post(BaseModel):
    title = peewee.CharField(max_length=120)
    text = peewee.TextField(null=False)
    created_at = peewee.DateTimeField(default=datetime.now)
    up_time = peewee.IntegerField(default=0)

    user = peewee.ForeignKeyField(User)

    def __unicode__(self):
        return self.title


class Comment(BaseModel):
    user = peewee.CharField(max_length=80)
    email = peewee.CharField(max_length=120)
    url = peewee.CharField(max_length=120)
    text = peewee.TextField(null=False)
    created_at = peewee.DateTimeField(default=datetime.now)

    post = peewee.ForeignKeyField(Post)

    def __unicode__(self):
        return self.user


class Up(BaseModel):
    ip = peewee.CharField(max_length=15)

    post = peewee.ForeignKeyField(Post)

    class Meta:
        primary_key = peewee.CompositeKey('ip', 'post')


class UserAdmin(ModelView):
    inline_models = (UserInfo,)


class CommentAdmin(ModelView):
    pass


class PostAdmin(ModelView):
    # Visible columns in the list view
    column_exclude_list = ['text']

    # List of columns that can be sorted. For 'user' column, use User.email as
    # a column.
    column_sortable_list = ('title', ('user', User.email), 'created_at')

    # Full text search
    column_searchable_list = ('title', User.username)

    # Column filters
    column_filters = ('title',
                      'created_at',
                      User.username)

    form_ajax_refs = {
        'user': {
            'fields': (User.username, 'email')
        }
    }


if __name__ == '__main__':
    try:
        User.create_table()
        UserInfo.create_table()
        Post.create_table()
        Comment.create_table()
        Up.create_table()
    except:
        pass
