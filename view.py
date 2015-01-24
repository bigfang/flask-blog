#!/usr/bin/env python
# -*- coding:utf-8 -*-


from datetime import datetime
import os.path as op

from flask import request, render_template, abort
from flask.ext.admin import Admin
from flask.ext.admin.contrib.fileadmin import FileAdmin

from model import UserAdmin, PostAdmin, CommentAdmin, User, Post, Comment
from controller import up
from app import app


admin = Admin(app, name='Admin')

admin.add_view(UserAdmin(User))
admin.add_view(PostAdmin(Post))
admin.add_view(CommentAdmin(Comment))
path = op.join(op.dirname(__file__), 'upload')
admin.add_view(FileAdmin(path, '/upload/', name='Uploaded Files'))


@app.route('/')
@app.route('/page/<int:page_id>')
def index(page_id=1):
    page_size = app.config.get('PAGE_SIZE')
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

    posts = Post.select().order_by(Post.id).paginate(page_id, page_size)

    return render_template('index.html', posts=posts, page_id=page_id, page_count=page_count)


@app.route('/post/<int:post_id>')
def post(post_id=1):
    try:
        post = Post.select().where(Post.id == post_id).get()
    except:
        abort(404)
    else:
        comments = Comment.select().where(Comment.post == post_id)
        return render_template('post.html', post=post, comments=comments)


@app.route('/comment', methods=['POST'])
def new_comment():
    user = request.form.get('user', '')
    email = request.form.get('email', '')
    site = request.form.get('site', '')
    content = request.form.get('content', '')
    post_id = request.form.get('post', None)

    Comment.create(user=user, email=email, url=site, text=content, post=post_id,
                   created_at=datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M'))
    return render_template('comment.html', comments=Comment.select().order_by(Comment.id.desc()).limit(1))


@app.route('/up', methods=['POST'])
def vote_up():
    post_id = request.form.get('post_id', 1)
    ip = request.environ['REMOTE_ADDR']
    num = up(post_id, ip)
    return str(num)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    return render_template('50x.html'), 500
