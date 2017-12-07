import os
import Queue
import json
import time
from multiprocessing import Process
from multiprocessing import Queue as PQueue
import pyspeedtest


CONF_FILE = json.loads(open("network_conf.json", "r").read())
SPEEDTEST_URL = CONF_FILE["SPEEDTEST"]["Address"]


class NetworkObj(object):

    def __init__(self):

        self.task_queue = PQueue()
        self.speed_test = pyspeedtest.SpeedTest()
        self.procs = list()

    def _send_ping(self, server_name, ip_address):

        respond = os.system("ping -c2 " + ip_address + " > /dev/null")
        status = "DIED!"

        if respond == 0:

            status = "ALIVE!"

        self.task_queue.put({"Network": {server_name: status}})

    def _get_speedtest(self):

        try:
            self.speed_test.connect(SPEEDTEST_URL)

            self.procs.append(Process(target=self.task_queue.put, args=(
                {"Speed_Test": {"Ping": "%.2f ms" % self.speed_test.ping()}},)
                                     )
                             )

            self.procs.append(Process(target=self.task_queue.put, args=(
                {"Speed_Test":{"Download": pyspeedtest.pretty_speed(self.speed_test.download())}},)
                                     )
                             )
            self.procs.append(Process(target=self.task_queue.put, args=(
                {"Speed_Test":{"Upload": pyspeedtest.pretty_speed(self.speed_test.upload())}},)
                                     )
                             )

        except:

            self.procs.append(
                Process(target=self.task_queue.put, args=(
                    {
                        "Speed_Test":{"Download": "0.0 Mbps",
                                      "Upload": "0.0 Mbps",
                                      "Ping": "0.0 ms"
                                     }
                    },)
                       )
            )

    def get_network(self):

        ip_addresses = CONF_FILE["PING"]

        for ip_address in ip_addresses:

            proc = Process(target=self._send_ping, args=(ip_address, ip_addresses[ip_address]))
            self.procs.append(proc)

        self._get_speedtest()

        for proc in self.procs:

            proc.start()

        for proc in self.procs:

            proc.join()

        result = {
            "Time": time.ctime(time.time()),
            "Speed_Test": {"URL": SPEEDTEST_URL},
            "Network": dict()
        }

        while True:

            try:

                msg = self.task_queue.get(timeout=2)

                if msg.has_key("Speed_Test"):

                    result["Speed_Test"].update(msg["Speed_Test"])

                elif msg.has_key("Network"):

                    if len(result["Network"].keys()) == 0:

                        result["Network"] = msg["Network"]

                    else:

                        result["Network"].update(msg["Network"])

            except Queue.Empty:

                break

        return json.dumps(result, indent=4, sort_keys=True)


#tb_network = TBNetwork()
#print tb_network.get_network()
