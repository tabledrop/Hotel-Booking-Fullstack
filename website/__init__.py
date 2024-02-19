from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

# Create the Flask app
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'supersecretkeylol'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # Register the blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # generate database
    # ensure commits DO NOT INCLUDE DATABASES
    # place any db files in gitignore file
    from .models import User, Room

    with app.app_context():
        db.create_all()

    return app
