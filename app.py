from flask import Flask

import requests

from myocen.services import services

app = Flask(__name__)

app.register_blueprint(services)

@app.route("/hello")
def hello_world():
    return "<p>Hello, World!</p>"

