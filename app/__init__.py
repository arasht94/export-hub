from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['MODELS_DIR'] = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
    
    from app.routes import main
    app.register_blueprint(main)
    
    return app

