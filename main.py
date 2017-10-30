from flask import Flask
from flask import redirect
from common.wrapper_exceptions import register_error_handler
from db.main import db as app_db
from settings import SQLALCHEMY_DATABASE_URI

from test_case1.main import test1
from test_case2.main import test2
from url_resource.main import EndpointResourceManager
from user.view import user_view

app = Flask(__name__)
register_error_handler(app)
app.register_blueprint(test1)
app.register_blueprint(test2)
app.register_blueprint(user_view)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app_db.init_app(app)
app.db = app_db
app.first_time = False
with app.app_context():
    app_db.create_all()
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
