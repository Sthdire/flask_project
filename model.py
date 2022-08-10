from flask_login import UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask import Flask


App = Flask(__name__)

login_manager = LoginManager(App)
App.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:rEtyuol44@localhost/union'
App.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(App)
db.create_all()

class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)



@login_manager.user_loader
def load_user(user_id):
    return users.query.get(user_id)