from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_login import LoginManager
# from flask_bootstrap import Bootstrap
from flask_migrate import Migrate

db=SQLAlchemy()
# bootstrap=Bootstrap()
mylogin=LoginManager()
migrate=Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    # bootstrap.init_app(app)
    mylogin.init_app(app)
    migrate.init_app(app, db)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app