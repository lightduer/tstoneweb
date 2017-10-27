from flask import Flask
from flask import redirect
from flask_restful import Api
from test_case.main import test

app = Flask(__name__)
api = Api()
api.init_app(test)
app.register_blueprint(test)


@app.route('/login')
@app.route('/')
def login():
    return redirect('/test_case/welcome')


if __name__ == '__main__':
    app.run()
