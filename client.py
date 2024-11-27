import logging

import grpc
import gfs_pb2
import gfs_pb2_grpc
import json
from threading import Lock
import sys

# no. of characters stored
CHUNK_SIZE = 16

class Client:
    def __init__(self, master_server, chunk_servers, id_):
        self.master_channel = grpc.insecure_channel(master_server)
        self.master_stub = gfs_pb2_grpc.MasterToClientStub(self.master_channel)
        self.client_id = id_
        self.chunk_channels = [grpc.insecure_channel(chunkserver) for chunkserver in chunk_servers]
        self.chunk_stubs = [gfs_pb2_grpc.ChunkToClientStub(self.chunk_channels[i]) for i in range(len(self.chunk_channels))]


    def create_file(self, stub):
        file_name = input("Enter file name: ")
        response = stub.CreateFile(gfs_pb2.FileRequest(name=file_name))
        if response.code == 1:
            print("Success.")
        else:
            print(response.message)


    def delete_file(self, stub):
        file_name = input("Enter file name: ")
        response = stub.DeleteFile(gfs_pb2.FileRequest(name=file_name))
        if response.code == 1:
            print("File deleted.")
        else:
            print(response.message)

    
    # def write(self, stub):
    #     file_name = input("Enter name of file to write to: ")
    #     offset = input("Enter offset from where to start writing: ")
    #     content = input("Enter content to be written: ")
    #     chunk_start_idx = offset/CHUNK_SIZE
    #     num_chunks_needed = len(content)/CHUNK_SIZE
    #     locations = stub.LocateChunk(gfs_pb2.WriteChunkRequest(length=len(content), idx=chunk_start_idx, name=file_name))


    def append(self, stub):
        file_name = input("Enter file name: ")
        content = input("Enter content: ")
        content_covered = 0
        num_chunks = int(len(content)//CHUNK_SIZE)
        servers = stub.AppendRecord(gfs_pb2.AppendRequest(new_chunk=num_chunks,name=file_name))
        for server in servers:
            if server.status == 0:
                print("File does not exist.")
                return
            if server.status == 2:
                chunk_id = server.chunk_id
                chunk_locations = server.server
                till = CHUNK_SIZE/4
                if len(content) < till:
                    till = len(content)
                record = content[:till]
                

        while content_covered < len(content):
            if content_covered + CHUNK_SIZE/4 > len(content):
                record = content[content_covered:]
            else:
                record = content[content_covered:content_covered+CHUNK_SIZE/4]
            content_covered += CHUNK_SIZE/4

        return


    def run(self, server):
        print("Running on server", server, sep=" ")
        while True:
            action = input("Enter 1 to create file, 2 to delete file, 3 to append to file, q to quit: ")
            if action == "1":
                self.create_file(self.master_stub)
            elif action == "2":
                self.delete_file(self.master_stub)
            elif action == "3":
                self.append(self.master_stub)
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
    client = Client(master_servers[idx], chunk_servers, id_)
    client.run(master_servers[idx])