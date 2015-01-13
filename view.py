#!/usr/bin/env python
# -*- coding:utf-8 -*-


from flask import request, session, redirect, flash, render_template, url_for, abort
# from admin import *



from flask.ext import admin
from model import *

admin = admin.Admin(app, name='Admin')

admin.add_view(UserAdmin(User))
admin.add_view(PostAdmin(Post))
admin.add_view(CommentAdmin(Comment))


@app.route('/')
@app.route('/page/<int:page_id>')
def index(page_id=1):
    page_size = 2;
    posts = Post.select().order_by(Post.id).paginate(page_id, page_size)
    total = Post.select().count()

    if total % page_size:
        page_count = total / page_size + 1
    else:
        page_count = total / page_size

    if page_id > page_count:
        abort(404)

    return render_template('index.html', posts=posts, page_id=page_id, page_count=page_count)


@app.route('/post/<int:post_id>')
def post(post_id=1):
    post = Post.select().where(Post.id == post_id)
    return render_template('post.html', post=post.get())


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))
