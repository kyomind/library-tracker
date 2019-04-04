from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from config import mode


db=SQLAlchemy()
mylogin=LoginManager()
migrate=Migrate()
mail=Mail()


def create_app(mode_key):
    app = Flask(__name__)
    app.config.from_object(mode[mode_key])
    mode[mode_key].init_app(app)

    db.init_app(app)
    mylogin.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app