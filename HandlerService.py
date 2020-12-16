import grpc

from concurrent import futures
import logging

import service_pb2, service_pb2_grpc


class Service(service_pb2_grpc.serviceServicer):

    def getName(self, request, context):

        print("\n----getName method is called-----\n")
        return service_pb2.HandlerName(name=f'{"customEvent"}')

    def getPriority(self, request, context):

        print("\n----getPriority method is called-----\n")
        return service_pb2.Priority(priority=58)

    def handleEvent(self, request, context):
        print("\n----handlerEvent method is called-----\n")

        if request.event=="PRE_ADD_USER":
            return service_pb2.Log(log=f'{"testing PRE_ADD_USER event on Python grpc server"}')
        if request.event=="POST_ADD_USER":
            return service_pb2.Log(log=f'{"testing POST_ADD_USER event on Python grpc server"}')


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_serviceServicer_to_server(Service(), server)
    server.add_insecure_port('[::]:8010')
    server.start()
    print("Server starts at port :8010")
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
