from flask import Flask
from .views import views
from .auth import auth

# Create the Flask app
def create_app():
    app = Flask(__name__)
    
    # Register the blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app