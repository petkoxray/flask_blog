from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from flask_debugtoolbar import DebugToolbarExtension
from config import Config
from .core.jinja_ext import register_jinja_ext


db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()
bootstrap = Bootstrap()
moment = Moment()
debug_toolbar = DebugToolbarExtension()


def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)

    register_jinja_ext(app)

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.routes import errors
    from flaskblog.comments.routes import comments
    from flaskblog.tags.routes import tags
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)
    app.register_blueprint(comments)
    app.register_blueprint(tags)

    return app


