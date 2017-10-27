from flask import Blueprint

test = Blueprint("test_case", __name__, url_prefix='/test_case')


@test.route('/welcome')
def _index():
    return 'Welcome to my restful-blueprint'


@test.route('/restful')
def _restful():
    return 'Welcome to my restful'
