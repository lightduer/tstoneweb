from flask import g
from flask import session

from common.app_cache import session_cache
from common.app_session import RedisSessionInterface
from db_model import db
from settings import SQLALCHEMY_DATABASE_URI
from user_misc.view import user_misc


def init_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    db.init_app(app)
    with app.app_context():
        db.create_all()


def init_cache(app):
    session_cache.init_app(app)
    app.session_cache = session_cache
    app.session_interface = RedisSessionInterface(app.session_cache)


def register_blueprint(app):
    app.register_blueprint(user_misc)


def init_hook(app):
    app.before_request(before_request)
    app.teardown_request(teardown_request)


def before_request():

    g.user = session.get('user', None)
    g.role = session.get('role', None)
    g.app_db = db.session


def teardown_request(exc):
    app_db = getattr(g, 'pg_db', None)
    if app_db:
        app_db.remove()


def init_app(app):
    init_db(app)
    init_cache(app)
    init_hook(app)
    register_blueprint(app)

