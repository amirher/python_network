import time
import json
#import threading
from multiprocessing import Process
from flask import Flask, request
from network_lib import NetworkObj


APP = Flask(__name__)


def data_engine():

    while True:

        network = NetworkObj()
        result = network.get_network()

        with open("result.json", "w") as data_file:

            data_file.write(result)

        time.sleep(5)


@APP.route("/")
def front_page():

    return "HELLO ROBOT!"


@APP.route("/network_data")
def get_network_data():

    key = request.args.get("key")

    if key == "mynetwork123456":

        return open("result.json", "r").read()

    return json.dumps({"status": "Error", "error_msg": "Invalid Keys"})


def main():

    """engine_thread = threading.Thread(target=data_engine, args=tuple())
    engine_thread.setDaemon(True)
    engine_thread.start()
    """

    print "Beginning data_engine process..."

    engine_processes = [Process(target=data_engine, args=tuple()) for i in range(2)]
    #engine_process.daemon = True

    for engine in engine_processes:

        engine.start()
        print "data_engine PID: %d" % engine.pid

    APP.run(host='0.0.0.0', debug=True)


if __name__ == '__main__':

    main()
