from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

import os.path as osp
import sys
BUILD_DIR = osp.join(osp.dirname(osp.abspath(__file__)), "../../build/service/")
sys.path.insert(0, BUILD_DIR)
import grpc
import fib_pb2
import fib_pb2_grpc
import log_pb2
import log_pb2_grpc

import paho.mqtt.client as mqtt

client = mqtt.Client()
client.connect(host='localhost', port=1883)
client.loop_start()

# Create your views here.
class FibonacciView(APIView):
    permission_classes = (permissions.AllowAny,)
    
    def post(self, request):
        with grpc.insecure_channel("localhost:8080") as channel:
            stub = fib_pb2_grpc.FibCalculatorStub(channel)

            fib_request = fib_pb2.FibRequest()
            fib_request.order = request.data['order']

            response = stub.Compute(fib_request)
        
        client.publish(topic='fib_post_order', payload=request.data['order'])

        return Response(data={ 'value': response.value }, status=200)

class LogsView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        with grpc.insecure_channel("localhost:8090") as channel:
            stub = log_pb2_grpc.LogSaverStub(channel)

            request = log_pb2.LogRequest()
            request.ask_logs = 1
            response = stub.getLogs(request)
        return Response(data={ 'history': list(response.logs) }, status=200)

