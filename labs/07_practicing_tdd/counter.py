import status
from flask import Flask, request

app = Flask(__name__)

COUNTERS = {}

@app.route("/counters/<name>", methods=["POST"])
def create_counter(name):
    """Creates a counter"""
    app.logger.info(f"Request to create counter: {name}")
    global COUNTERS

    if name in COUNTERS:
        return {"message":f"Counter {name} already exists"}, status.HTTP_409_CONFLICT

    COUNTERS[name] = 0
    return { name: COUNTERS[name] }, status.HTTP_201_CREATED


@app.route("/counters/<name>", methods=["PUT"])
def update_counter(name):
    """Updates a counter"""
    app.logger.info(f"Request to update counter: {name}")
    global COUNTERS

    COUNTERS[name] += 1
    return { name: COUNTERS[name] }, status.HTTP_200_OK


@app.route("/counters/<name>", methods=["GET"])
def read_counter(name):
    """Reads a counter"""
    app.logger.info(f"Request to read counter: {name}")
    global COUNTERS
    return { name: COUNTERS[name] }, status.HTTP_200_OK


@app.route("/counters/<name>", methods=["DELETE"])
def delete_counter(name):
    """Deletes a counter"""
    app.logger.info(f"Request to delete counter: {name}")
    global COUNTERS
    del COUNTERS[name]
    return {"message": ""}, status.HTTP_204_NO_CONTENT
