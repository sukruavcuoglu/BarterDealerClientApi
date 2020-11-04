import os

# third-party imports
import connexion
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# local imports
from config import app_config

basedir = os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()


def create_app(config_name):
    # Create the connexion application instance
    connex_application = connexion.App(__name__, specification_dir=basedir)

    if config_name == "production":
        # Get the underlying Flask app instance
        app = connex_application.app
        SECRET_KEY = os.urandom(32)
        app.config.update(
            SECRET_KEY=SECRET_KEY,
            SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:123455@localhost/barterdealer"
        )
    else:
        app = connex_application.app
        # app = Flask(__name__, instance_relative_config=True)
        app.config.from_object(app_config[config_name])
        app.config.from_pyfile('config.py')

    # from .application import api_bp
    # app.register_blueprint(api_bp, url_prefix='/api')

    db.init_app(app)

    # Initialize Marshmallow
    ma.init_app(app)

    migrate = Migrate(app, db)

    # login_manager.init_app(app)

    return connex_application
