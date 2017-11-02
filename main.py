from flask import Flask
from common.app_cache import session_cache
from common.app_session import RedisSessionInterface
from db_model import db

from settings import SQLALCHEMY_DATABASE_URI
from user_misc.view import user_misc

app = Flask(__name__)
app.register_blueprint(user_misc)


app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db.init_app(app)
app.db = db
session_cache.init_app(app)
app.session_cache = session_cache
app.session_interface = RedisSessionInterface(app.session_cache)
app.first_time = False
with app.app_context():
    db.create_all()


@app.route('/')
def main_page():
    return "main_page"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000)
