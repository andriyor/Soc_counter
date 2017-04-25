from flask_login import UserMixin
from flask_mongoengine import MongoEngine

from app import app, login_manager, flask_bcrypt

db = MongoEngine(app)

handle = 'rozetked'


class Links(db.EmbeddedDocument):
    youtube = db.StringField(max_length=200)
    twitter = db.StringField(max_length=200)
    instagram = db.StringField(max_length=200)
    facebook = db.StringField(max_length=200)


class User(UserMixin, db.Document):
    email = db.StringField(max_length=50, unique=True)
    username = db.StringField(max_length=50, unique=True)
    password_hash = db.StringField(max_length=200)
    links = db.EmbeddedDocumentField(Links)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = flask_bcrypt.generate_password_hash(password).decode("utf-8")

    def verify_password(self, password):
        return flask_bcrypt.check_password_hash(self.password_hash, password)

    @staticmethod
    def get_by_email(email):
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None


@login_manager.user_loader
def load_user(user_id):
    return User.objects.with_id(user_id)
