from flask import Flask
from flask import redirect
from common.exceptions import register_error_handler
from db.main import db as app_db
from settings import SQLALCHEMY_DATABASE_URI

from test_case1.main import test1
from test_case2.main import test2
from user.view import user_view

app = Flask(__name__)
register_error_handler(app)
app.register_blueprint(test1)
app.register_blueprint(test2)
app.register_blueprint(user_view)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app_db.init_app(app)
with app.app_context():
    app_db.create_all()


@app.route('/login1')
@app.route('/1')
def login1():
    return redirect('/test_case1/welcome?tag=foo')


@app.route('/login2')
@app.route('/2')
def login2():
    return redirect('/test_case2/welcome')


if __name__ == '__main__':
    app.run()
