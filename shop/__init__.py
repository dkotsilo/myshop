from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import sys

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myshop.db'
app.config['SECRET_KEY']='hfouewhfoiwefoquw'

db = SQLAlchemy(app)



from shop.admin import routes