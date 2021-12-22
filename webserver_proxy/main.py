from flask import Flask, jsonify, request

# from sequence import client
from compositions.async_coordinator import client as async_coordinator_client

app = Flask(__name__)

# @app.route("/coordinator", methods=['POST'])
# def coordinator():
#     payload = request.get_json(force=True)
#     re

@app.route("/async_coordinator", methods=['POST'])
def async_coordinator():
    payload = request.get_json(force=True)
    response = async_coordinator_client.invoke(
        sleep=payload['sleep'],
        workflow=payload['workflow'],
        waiter_config=payload['waiter_config']
    )
    
    del response['Payload']
    print(response)
    return jsonify(response)

# @app.route("/async_sequence")
# def async_sequence():

if __name__ == "__main__":
    import bjoern

    bjoern.run(app, "127.0.0.1", 8000)