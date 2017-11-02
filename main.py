from flask import Flask
from flask import redirect
from flask import session

from common.app_cache import session_cache
from common.app_database import db
from common.app_session import RedisSessionInterface
from role.main import EndpointResourceManager
from settings import SQLALCHEMY_DATABASE_URI

from test_case1.main import test1
from test_case2.main import test2
from user.view import user_view

app = Flask(__name__)
app.register_blueprint(test1)
app.register_blueprint(test2)
app.register_blueprint(user_view)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
db.init_app(app)
app.db = db
session_cache.init_app(app)
app.cache = session_cache
app.session_interface = RedisSessionInterface(app.cache)
app.first_time = False
with app.app_context():
    db.create_all()
    EndpointResourceManager.script_init_endpoint_resource_table(app)


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
