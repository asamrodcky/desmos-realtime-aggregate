import os
import time
import json
import argparse
import sys

from flask import Flask
from flask_sock import Sock
import uuid


app = Flask(__name__)
sock = Sock(app)

desmos_init_state = ""

state = {
    "connected-users": {},
}

def handle_init():
    # generate a uuid for the user
    # keep track of graph state on serverside
    user_uuid = str(uuid.uuid4())
    number_of_connected_users = len(state["connected-users"])
    print(len(state["connected-users"]))
    state["connected-users"][user_uuid] = {
        "uuid": user_uuid,
        "id": number_of_connected_users + 1,
        "x": 0,
        "y": 0
    }
    return user_uuid


def handle_point_update(uuid, data):
    # Find which dictionary entry has the uuid
    state["connected-users"][uuid]["uuid"] = uuid
    state["connected-users"][uuid]["x"] = data["x"]
    state["connected-users"][uuid]["y"] = data["y"]
    return


@sock.route("/echo")
def echo(sock):
    print("Someone Connected!")
    # update these with student points from webcam

    while True:
        received_data = sock.receive(timeout=1./30)

        if received_data:
            parsed_data_dict = json.loads(received_data)

            if parsed_data_dict["message-type"] == "init":
                new_user_uuid = handle_init()
                sock.send({
                    "message-type": "init-res",
                    "data": {
                        "uuid": new_user_uuid,
                        # "desmos-init-state": state["desmos-init-state"]
                    }
                })
            elif parsed_data_dict["message-type"] == "point-update":
                handle_point_update(parsed_data_dict["uuid"], parsed_data_dict["data"])

        sock.send({
            "message-type": "point-update",
            "data": state
        })

@app.teardown_appcontext
def teardown(exception):
    print(exception)

if __name__ == "__main__":
    app.run()
