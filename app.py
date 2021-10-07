from flask import Flask, request
from main import hello_world


app = Flask(__name__)


@app.route("/")
def resize():
    return hello_world(request)


app.run()
