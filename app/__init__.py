from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from config import mode


db = SQLAlchemy()
mylogin = LoginManager()
migrate = Migrate()
mail = Mail()


def create_app(mode_key):
    app = Flask(__name__)
    app.config.from_object(mode[mode_key])
    mode[mode_key].init_app(app)

    db.init_app(app)
    mylogin.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    from app.main import main
    app.register_blueprint(main)

    from app.auth import auth
    app.register_blueprint(auth, url_prefix='/auth')

    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        sslify = SSLify(app)
    
    return app