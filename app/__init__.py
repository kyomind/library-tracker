from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
# from flask_login import LoginManager

db=SQLAlchemy()
# mylogin=LoginManager()




def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    
    

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app