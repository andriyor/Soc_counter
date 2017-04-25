from flask import Flask
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_bootstrap import Bootstrap


app = Flask(__name__)

Bootstrap(app)

app.config['MONGODB_SETTINGS'] = {'db': 'soc_counter'}
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.debug = True

db = MongoEngine(app)
app.session_interface = MongoEngineSessionInterface(db)

flask_bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
