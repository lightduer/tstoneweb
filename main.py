from flask import Flask
from app import init_app

app = Flask(__name__)
init_app(app)


@app.route('/')
def main_page():
    return "main_page"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000)
