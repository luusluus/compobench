import logging
from flask import Flask, jsonify, request, Response

# from sequence import client
from compositions.function_sequence import client as sequence_client
from compositions.coordinator import client as coordinator_client
from compositions.compiled_sequence import client as compiled_client
from compositions.async_coordinator import client as async_coordinator_client
from compositions.async_function_sequence import client as async_sequence_client
from compositions.routing_slip import client as routing_slip_client
from compositions.event_sourcing import client as event_sourcing_client
from compositions.blackboard_based import client as blackboard_client
from compositions.message_queue_based import client as message_queue_client
from compositions.storage_based import client as storage_client
from compositions.workflow_engine import client as workflow_client

app = Flask(__name__)

@app.route("/sequence", methods=['POST'])
def sequence():
    payload = request.get_json(force=True)
    logging.info('invoking sequence')
    status_code = sequence_client.invoke(
        sleep=payload['sleep'],
    )
    return Response("", status=status_code, mimetype='application/json')

@app.route("/coordinator", methods=['POST'])
def coordinator():
    payload = request.get_json(force=True)
    status_code = coordinator_client.invoke(
        sleep=payload['sleep'],
        workflow=payload['workflow']
    )
    return Response("", status=status_code, mimetype='application/json')

@app.route("/compiled", methods=['POST'])
def compiled():
    payload = request.get_json(force=True)
    status_code = compiled_client.invoke(
        sleep=payload['sleep']
    )
    return Response("", status=status_code, mimetype='application/json')

@app.route("/async_coordinator", methods=['POST'])
def async_coordinator():
    payload = request.get_json(force=True)
    status_code = async_coordinator_client.invoke(
        sleep=payload['sleep'],
        workflow=payload['workflow'],
        waiter_config=payload['waiter_config']
    )
    return Response("", status=status_code, mimetype='application/json')

@app.route("/async_sequence", methods=['POST'])
def async_sequence():
    payload = request.get_json(force=True)
    status_code = async_sequence_client.invoke(
        sleep=payload['sleep'],
        waiter_config=payload['waiter_config']
    )
    return Response("", status=status_code, mimetype='application/json')

@app.route("/routing_slip", methods=['POST'])
def routing_slip():
    payload = request.get_json(force=True)
    status_code = routing_slip_client.invoke(
        sleep=payload['sleep'],
        waiter_config=payload['waiter_config'],
        composition=payload['composition']
    )
    
    return Response("", status=status_code, mimetype='application/json')

@app.route("/event_sourcing", methods=['POST'])
def event_sourcing():
    payload = request.get_json(force=True)
    status_code = event_sourcing_client.invoke(
        sleep=payload['sleep'],
        input=payload['input'],
    )
    
    return Response("", status=status_code, mimetype='application/json')

@app.route("/blackboard", methods=['POST'])
def blackboard():
    payload = request.get_json(force=True)
    status_code = blackboard_client.invoke()
    
    return Response("", status=status_code, mimetype='application/json')

@app.route("/message_queue", methods=['POST'])
def message_queue():
    payload = request.get_json(force=True)
    status_code = message_queue_client.invoke(
        sleep=payload['sleep'],
        waiter_config=payload['waiter_config'],
        message_attributes=payload['message_attributes']
    )
    
    return Response("", status=status_code, mimetype='application/json')


@app.route("/storage", methods=['POST'])
def storage_based():
    payload = request.get_json(force=True)
    status_code = storage_client.invoke(
        sleep=payload['sleep'],
        workflow=payload['workflow'],
        full_workflow=payload['full_workflow'],
        waiter_config=payload['waiter_config']
    )
    return Response("", status=status_code, mimetype='application/json')

@app.route("/workflow_engine", methods=['POST'])
def workflow_engine():
    payload = request.get_json(force=True)
    status_code = workflow_client.invoke(
        sleep=payload['sleep']
    )
    
    return Response("", status=status_code, mimetype='application/json')

import socket
try:
    from cheroot.wsgi import Server as WSGIServer
except ImportError:
    from cherrypy.wsgiserver import CherryPyWSGIServer as WSGIServer

server = WSGIServer(
    bind_addr=('127.0.0.1', 8000),
    wsgi_app=app,
    request_queue_size=65536,
    server_name=socket.gethostname()
)

if __name__ == '__main__':
    try:
        server.start()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()