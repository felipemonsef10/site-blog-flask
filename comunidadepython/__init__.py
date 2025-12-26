from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os
import sqlalchemy


app = Flask(__name__)

app.config['SECRET_KEY'] = 'cafe21d28999850c8855b75bb3192523'

if os.getenv('DATABASE_URL'):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Faça login para continuar!'
login_manager.login_message_category = 'alert-warning'

from comunidadepython import models

if 'sqlite' not in app.config['SQLALCHEMY_DATABASE_URI']:
    engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    inspector = sqlalchemy.inspect(engine)

    if not inspector.has_table('usuario'):
        with app.app_context():
            db.drop_all()
            db.create_all()
        print('-----------------------')
        print('Database criado')
        print('-----------------------')
    else:
        print('-----------------------')
        print('Database já existente')
        print('-----------------------')

from comunidadepython import routes