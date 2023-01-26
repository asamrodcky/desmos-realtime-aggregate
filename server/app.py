import os
import time
import json
import argparse
import sys

from flask import Flask
from flask_sock import Sock


app = Flask(__name__)
sock = Sock(app)

@sock.route("/echo")
def echo(sock):
    print("Someone Connected!")
    # update these with student points from webcam
    data = {}
    while True:
        sock.send(data)

@app.teardown_appcontext
def teardown(exception):
    print(exception)

if __name__ == "__main__":
    app.run()
