import logging

import grpc
import gfs_pb2
import gfs_pb2_grpc
import json
from threading import Lock

import config as cfg


class Client:
    def __init__(self, master_ip, master_port):

        self.master_channel = grpc.insecure_channel(master_ip + ":" + master_port)
        self.master_stub = gfs_pb2_grpc.MasterToClientStub(self.master_channel)
        self.client_id = self.get_client_id()



        self.master_channel = grpc.insecure_channel(cfg.MASTER_IP + ":" + cfg.MASTER_PORT)
        self.master_stub = hybrid_dfs_pb2_grpc.MasterToClientStub(self.master_channel)
        self.chunk_channels = [grpc.insecure_channel(cfg.CHUNK_IPS[i] + ":" + cfg.CHUNK_PORTS[i]) for i in
                                range(cfg.NUM_CHUNK_SERVERS)]
        self.chunk_stubs = [hybrid_dfs_pb2_grpc.ChunkToClientStub(channel) for channel in self.chunk_channels]
        self.chunk_stubs = {cfg.CHUNK_LOCS[i]: hybrid_dfs_pb2_grpc.ChunkToClientStub(self.chunk_channels[i]) for i in
                            range(cfg.NUM_CHUNK_SERVERS)}




def create_file(stub):
    file_name = input("Enter file name: ")
    response = stub.create_file(gfs_pb2.FileName(string=file_name))
    if response.code:
        print("Success.")
    else:
        print(response.message)

def delete_file(stub):
    file_name = input("Enter file name: ")
    response = stub.delete_file(gfs_pb2.FileName(string=file_name))
    if response.code:
        print("File deleted.")
    else:
        print(response.message)


def run(server):
    channel = grpc.insecure_channel(server)
    print("Running on server", server, sep=" ")
    stub = gfs_pb2_grpc.MasterToClientStub(channel)
    while True:
        action = input("Enter 1 to create file, 2 to delete file, q to quit: ")
        if action == "1":
            create_file(stub)
        elif action == "q":
            break

def clientID(server):
    channel = grpc.insecure_channel(server)
    stub = gfs_pb2_grpc.MasterToClientStub(channel)
    response = stub.GetClientID(gfs_pb2.EmptyRequest())
    print("Client ID =", response.client_id, sep=" ")
    return response.client_id

if __name__ == "__main__":



    logging.basicConfig()
    master_servers = ['localhost:50051', 'localhost:50052', 'localhost:50053']
    chunk_servers = ['localhost:50054', 'localhost:50055', 'localhost:50056', 'localhost:50057', 'localhost:50058']
    id_ = clientID(master_servers[0])
    idx = int(id_ % len(master_servers))
    run(master_servers[idx])

