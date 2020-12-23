import grpc

from concurrent import futures
import logging
from datetime import datetime
import service_pb2, service_pb2_grpc


class Service(service_pb2_grpc.serviceServicer):

    now = datetime.now() # current date and time
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    print("date and time:",date_time)

    def getName(self, request, context):

        now = datetime.now() # current date and time
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        print("date and time:",date_time)

        print("\n----getName method is called-----\n")
        return service_pb2.HandlerName(name="grpcBasedEventHandler")

    def getPriority(self, request, context):

        print("\n----getPriority method is called-----\n")
        return service_pb2.Priority(priority=58)

    def handleEvent(self, request, context):
        now = datetime.now() # current date and time
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        print("date and time:",date_time)
        print("\n----handlerEvent method is called-----\n")
        print(request.eventProperties["user-name"])

        if request.event=="POST_ADD_USER":
            return service_pb2.Log(log=f'{"testing POST_ADD_USER event using GrpcEventHandler on Python gRPC server with UserName- " + request.eventProperties["user-name"] + ", TenantDomain- " + request.eventProperties["tenant-domain"]}')


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
