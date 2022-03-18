# coding=utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, TextField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length

from app.models import User


class LoginForm(FlaskForm):  
    username = StringField('Login', validators=[DataRequired(),Length(min=1, max=30)])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=1, max=100)])
    submit = SubmitField('Sign in!')


class RegisterForm(FlaskForm):
    username = StringField('Login', validators=[DataRequired(),Length(min=1, max=30)])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=1, max=100)])
    password2 = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password'),Length(min=1, max=100)])
    submit = SubmitField('Create!')

    def validate_username(self, username): 
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('This username is using by other user')


class CommentForm(FlaskForm):
    text = TextAreaField('text', validators=[DataRequired(),Length(min=1, max=74)])
    submit = SubmitField('Comment!')


class CreatePostForm(FlaskForm):
    title = TextField('title', validators=[DataRequired(), Length(min=1, max=100)])
    intro = TextAreaField('intro', validators=[DataRequired(), Length(min=1, max=255)])
    text = TextAreaField('text', validators=[DataRequired(),Length(min=1, max=6000) ])
    submit = SubmitField('Create!')
