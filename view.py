#!/usr/bin/env python
# -*- coding:utf-8 -*-


from datetime import datetime

from flask import request, session, redirect, flash, render_template, url_for, abort
from flask.ext import admin

from model import UserAdmin, User, Post, PostAdmin, Comment, CommentAdmin
from app import app


admin = admin.Admin(app, name='Admin')

admin.add_view(UserAdmin(User))
admin.add_view(PostAdmin(Post))
admin.add_view(CommentAdmin(Comment))


@app.route('/')
@app.route('/page/<int:page_id>')
def index(page_id=1):
    page_size = app.config.get('PAGE_SIZE')
    posts = Post.select().order_by(Post.id).paginate(page_id, page_size)
    total = Post.select().count()

    if total == 0:
        page_id = 1
        page_count = 1
    elif total % page_size:
        page_count = total / page_size + 1
    else:
        page_count = total / page_size

    if page_id > page_count:
        abort(404)

    return render_template('index.html', posts=posts, page_id=page_id, page_count=page_count)


@app.route('/post/<int:post_id>')
def post(post_id=1):
    post = Post.select().where(Post.id == post_id).get()
    comments = Comment.select().where(Comment.post == post_id)
    return render_template('post.html', post=post, comments=comments)


@app.route('/comment/new', methods=['POST'])
def new_comment():
    user = request.form.get('user', '')
    email = request.form.get('email', '')
    site = request.form.get('site', '')
    content = request.form.get('content', '')
    post_id = request.form.get('post', None)

    Comment.create(user=user, email=email, url=site, text=content, post=post_id,
                   created_at=datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M'))
    return "successs"
