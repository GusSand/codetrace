from logging import Logger

from utils.scheduler.tasks import scheduler
from flask import render_template, request, jsonify
from flask_app import app
from utils.songkick_api import sk_api_mgr as api_mgr
from utils.songkick_api.sk_event import Event


log = Logger


@app.route('/events')
def build_response():
    request_ip = request.remote_addr
    print('Request IP: ' + str(request_ip))
    response_data = __tmp1(request)
    return jsonify(response_data), 200


@app.route('/')
def __tmp0():
    return render_template("hello.html")


@app.route('/goodbye')
def __tmp2():
    return render_template("goodbye.html")


def __tmp1(req: <FILL>) :
    # client_ip = req.remote_addr
    #  TODO When running this non-locally: uncomment this line AND comment out the line below
    client_ip = '75.73.22.98'
    log('Events requested from: ' + str(client_ip))
    api_data = api_mgr.search_local_events_for_ip(client_ip)
    events_objects_list = api_mgr.instantiate_events_from_list(api_data)
    serialized_events_list = api_mgr.serialize_event_list(events_objects_list)
    return serialized_events_list


if __name__ == '__main__':
    app.debug = False
    scheduler.start()
    app.run()
