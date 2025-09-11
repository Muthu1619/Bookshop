from flask import render_template,Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///D:/Codes/Python/bookolx/eazyshop/shop.db'
app.config['SECRET_KEY']='50271c5e58c01c24ca7b9288'
db=SQLAlchemy(app)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view='login' 
from eazyshop import route 