from flask import Flask
from flask import redirect
from test_case1.main import test1
from test_case2.main import test2

app = Flask(__name__)
app.register_blueprint(test1)
app.register_blueprint(test2)


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
