from flask import Flask
from flask import redirect

from common.app_cache import session_cache
from common.app_session import RedisSessionInterface
from db_model import db

from settings import SQLALCHEMY_DATABASE_URI
from test_case1.main import test1
from test_case2.main import test2

app = Flask(__name__)
app.register_blueprint(test1)
app.register_blueprint(test2)


app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db.init_app(app)
app.db = db
session_cache.init_app(app)
app.session_cache = session_cache
app.session_interface = RedisSessionInterface(app.session_cache)
app.first_time = False
with app.app_context():
    db.create_all()


@app.route('/login1')
@app.route('/1')
def login1():
    return redirect('/test_case1/welcome?tag=foo')


@app.route('/login2')
@app.route('/2')
def login2():
    return redirect('/test_case2/welcome')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000)
