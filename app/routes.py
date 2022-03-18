# -*- coding: utf-8 -*-
from datetime import datetime

from flask import url_for, render_template, flash
from flask_login import current_user, logout_user, login_user
from werkzeug.utils import redirect

from app import app, db, login_manager
from app.forms import LoginForm, RegisterForm, CommentForm, CreatePostForm
from app.models import Post, User, Comment, Message


@app.route('/create-post', methods=['POST', 'GET'])
def create_post():
    if not current_user.is_authenticated:
        return redirect(url_for('index'))

    form = CreatePostForm()
    if form.validate_on_submit():
        title = form.title.data
        intro = form.intro.data
        text = form.text.data

        current_post = Post(title=title, intro=intro, text=text, author=current_user)
        try:
            db.session.add(current_post)
            db.session.commit()
            return redirect('/blog')
        except:
            return "При добавлении статьи произошла ошибка!"
    else:
        return render_template('create-post.html', what="create-post", form=form)


@app.route('/blog/<post_id>/pin/<should_pin>')  
def pin(post_id, should_pin):
    if not current_user.is_authenticated or \
            (current_user.is_authenticated and current_user.role != 1):
        return redirect(url_for('index'))

    try:
        current_post = Post.query.get(post_id)
        current_post.is_pinned = bool(int(should_pin))
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return "Не удалось закрепить пост :("


@app.route('/blog')
def blog():
    posts = Post.query.order_by(-Post.id).all() 
    return render_template('blog.html', posts=posts, what="blog")


@app.route('/register', methods=['GET', 'POST'])  
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations! You have been registered!')  
        return redirect(url_for('login'))
    return render_template('register.html', what="register", form=form)


@app.route('/login', methods=['GET', 'POST'])  
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login')) 
        login_user(user)
        return redirect(url_for('index'))
    return render_template('login.html', form=form, what="login")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/blog/<current_id>', methods=['GET', 'POST'])
def post(current_id):
    current = Post.query.get(current_id)

    form = CommentForm()

    if form.validate_on_submit():
        current_comment = Comment(author=current_user, post=current, text=form.text.data, date=datetime.now())
        db.session.add(current_comment)
        db.session.commit()
        return redirect(url_for('post', current_id=current_id))
    return render_template('post.html', current=current, what="blog", form=form)


@app.route('/blog/<current_id>/update', methods=['GET', 'POST'])
def update_post(current_id):
    current = Post.query.get_or_404(current_id)
    if (not current_user.is_authenticated) or \
            (current_user.is_authenticated and current_user != current.author and current_user.role != 1):
        return redirect(url_for('index'))

    form = CreatePostForm(title=current.title, intro=current.intro,
                          text=current.text) 

    if form.validate_on_submit():
        current.title = form.title.data
        current.intro = form.intro.data
        current.text = form.text.data

        try:
            db.session.commit()
            return redirect(url_for('post', current_id=current_id))  
        except:
            return "При изменении статьи произошла ошибка!"
    else:
        return render_template('update-post.html', what="blog", current=current, form=form)


@app.route('/blog/<current_id>/remove')
def remove_post(current_id):
    current = Post.query.get_or_404(current_id)
    if (not current_user.is_authenticated) or \
            (current_user.is_authenticated and current_user != current.author and current_user.role != 1):
        return redirect(url_for('index'))

    try:
        db.session.delete(current)
        db.session.commit()
        return redirect(url_for('blog'))
    except:
        return "При удалении статьи произошла ошибка!"


@app.route('/')
def index():
    posts = Post.query.order_by(-Post.id).all()
    return render_template('index.html', what="index", posts=posts)


@app.route('/chat')
def chat():
    messages = Message.query.order_by(Message.id).all()
    return render_template('chat.html', what="chat", messages=messages)


@login_manager.user_loader  
def load_user(user_id):
    return User.query.get(int(user_id))
