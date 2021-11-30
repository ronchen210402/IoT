import os
import os.path as osp
import sys
BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "build/service/")
sys.path.insert(0, BUILD_DIR)
import argparse

import grpc
from concurrent import futures
import log_pb2
import log_pb2_grpc

import paho.mqtt.client as mqtt

import threading

logs = []

def on_message(client, obj, msg):
    global logs
    print(f"TOPIC:{msg.topic}, VALUE:{int(msg.payload)}")
    logs.append(int(msg.payload))

client = mqtt.Client()
client.on_message = on_message
client.connect(host='localhost', port=1883)
client.subscribe('fib_post_order', 0)
def run():
    global client
    try:
        client.loop_forever()
    except KeyboardInterrupt as e:
        pass
t = threading.Thread(target=run)

class LogSaverServicer(log_pb2_grpc.LogSaverServicer):

    def __init__(self):
        pass

    def getLogs(self, request, context):
        global logs
        response = log_pb2.LogResponse()
        for log in logs:
            response.logs.append(log)
        return response


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="0.0.0.0", type=str)
    parser.add_argument("--port", default=8090, type=int)
    args = vars(parser.parse_args())

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    servicer = LogSaverServicer()
    log_pb2_grpc.add_LogSaverServicer_to_server(servicer, server)

    try:
        server.add_insecure_port(f"{args['ip']}:{args['port']}")
        server.start()
        print(f"Run gRPC Server at {args['ip']}:{args['port']}")
        t.start()
        print(f"Run MQTT Subscriber at {'localhost'}:{1883}")
        server.wait_for_termination()
    except KeyboardInterrupt:
        pass
