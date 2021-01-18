import grpc

from concurrent import futures
import logging
from datetime import datetime
import service_pb2, service_pb2_grpc


class Service(service_pb2_grpc.serviceServicer):
    now = datetime.now()  # current date and time
    date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
    print("date and time:", date_time)

    def getName(self, request, context):
        now = datetime.now()  # current date and time
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        print("date and time:", date_time)

        print("----getName method is called-----\n")
        return service_pb2.HandlerName(name="grpcBasedEventHandlerPython")

    def getPriority(self, request, context):
        print("----getPriority method is called-----\n")
        return service_pb2.Priority(priority=58)

    def handleEvent(self, request, context):
        now = datetime.now()  # current date and time
        date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
        print("date and time:", date_time)
        print("----handlerEvent method is called-----\n")
        print("UserName: " + request.eventProperties["user-name"])
        print("TenantDomain: " + request.eventProperties["tenant-domain"])

        if request.event == "PRE_ADD_USER":
            return service_pb2.Log(
                log=f'{"testing PRE_ADD_USER event using GrpcEventHandler on Python gRPC server with UserName- " + request.eventProperties["user-name"] + ", TenantDomain- " + request.eventProperties["tenant-domain"]}')


def loadCredentials():
    # read in key and certificate
    with open('/home/nuwanga/wso2/event-handler-server/src/main/java/org/example/server/cert1/server-key.pem',
              'rb') as f:
        private_key = f.read()
    with open('/home/nuwanga/wso2/event-handler-server/src/main/java/org/example/server/cert1/server-cert.pem',
              'rb') as f:
        certificate_chain = f.read()

    # create server credentials
    server_credentials = grpc.ssl_server_credentials(
        ((private_key, certificate_chain,),))

    return server_credentials


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_serviceServicer_to_server(Service(), server)
    #server.add_insecure_port('[::]:8010')
    server.add_secure_port('[::]:8010', loadCredentials())
    server.start()
    print("Server starts at port :8010")
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
