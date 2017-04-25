from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, Regexp, URL
from flask_wtf import FlaskForm
from wtforms import ValidationError
import requests

from models import User

handle = 'rozetked'


class LinksForm(FlaskForm):
    youtube = StringField('YouTube about', validators=[URL()],
                          default="https://www.youtube.com/user/{}/about?hl=en".format(handle))
    twitter = StringField('Twitter', validators=[URL()], default="https://twitter.com/{}".format(handle))
    instagram = StringField('Instagram', validators=[URL()], default="https://www.instagram.com/{}".format(handle))
    facebook = StringField('Facebook', validators=[URL()], default="https://www.facebook.com/{}".format(handle))
    submit = SubmitField()

    def validate_youtube(self, field):
        if 'youtube' and 'user' not in field.data or requests.get(field.data).status_code != 200:
            raise ValidationError('Please enter youtube profile url')

    def validate_twitter(sef, field):
        if 'twitter' not in field.data or requests.get(field.data).status_code != 200:
            raise ValidationError('Please enter twitter profile url')

    def validate_instagram(self, field):
        if 'instagram' not in field.data or requests.get(field.data).status_code != 200:
            raise ValidationError('Please enter instagram profile url')

    def validate_facebook(self, field):
        if 'facebook' not in field.data or requests.get(field.data).status_code != 200:
            raise ValidationError('Please enter facebook profile url')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[
        DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              'Usernames must have only letters, '
                                              'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    @staticmethod
    def validate_email(field):
        if User.objects(email=field.data):
            raise ValidationError('Email already registered.')

    @staticmethod
    def validate_username(field):
        if User.objects(username=field.data):
            raise ValidationError('Username already in use.')
