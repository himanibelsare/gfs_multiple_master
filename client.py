import logging

import grpc
import gfs_pb2
import gfs_pb2_grpc
import json
from threading import Lock


def create_file(stub):
    file_name = input("Enter file name: ")
    response = stub.create_file(gfs_pb2.String(string=file_name))
    if response.code:
        print("Success.")
    else:
        print(response.message)


def run(server):
    channel = grpc.insecure_channel(server)
    print("Running on server", server, sep=" ")
    stub = gfs_pb2_grpc.MasterToClientStub(channel)
    while True:
        action = input("Enter 1 to create file, q to quit: ")
        if action == "1":
            create_file(stub)
        elif action == "q":
            break

def clientID(server):
    channel = grpc.insecure_channel(server)
    stub = gfs_pb2_grpc.MasterToClientStub(channel)
    response = stub.get_id(gfs_pb2.EmptyRequest())
    print("Client ID =", response.client_id, sep=" ")
    return response.client_id

if __name__ == "__main__":
    logging.basicConfig()
    servers = ['localhost:50051', 'localhost:50052', 'localhost:50053']
    id_ = clientID(servers[0])
    idx = int(id_ % len(servers))
    run(servers[idx])

