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

    def take_snapshot(self, stub):
        print("Taking snapshot")
        response = stub.CreateSnapshot(gfs_pb2.EmptyRequest())
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
        print(len(content))
        content_covered = 0
        num_chunks = int(len(content)//CHUNK_SIZE)
        servers = stub.AppendRecord(gfs_pb2.AppendRequest(new_chunk=num_chunks,name=file_name))
        content_covered = 0  # Track how much content has been processed

        for server in servers:
            if content_covered >= len(content):
                break  # Exit if all content has been covered
            
            chunk_id = server.chunk_id
            chunk_locations = server.server
            
            while True:
                till = int(CHUNK_SIZE // 4)
                remaining_content = len(content) - content_covered
                
                # Determine how much content to write in this iteration
                if remaining_content < till:
                    till = remaining_content
                
                record = content[content_covered:content_covered + till]
                response = self.chunk_stubs[chunk_locations[0]].AppendToChunk(
                    gfs_pb2.ChunkData(
                        chunk_id=chunk_id,
                        data=record
                    )
                )
                
                if response.code == 0:
                    break  # Move to the next chunk if AppendToChunk fails
                
                # Update content_covered based on successful write
                content_covered += till
                
                if content_covered >= len(content):
                    break  # Exit loop if all content has been written

        if content_covered < len(content):
            # print("here")
            server = stub.CommitChunk(gfs_pb2.AppendRequest(new_chunk=1,name=file_name))
            chunk_id = server.chunk_id
            chunk_locations = server.server
            record = content[content_covered:]
            response = self.chunk_stubs[chunk_locations[0]].AppendToChunk(
                            gfs_pb2.ChunkData(
                                chunk_id=chunk_id,
                                data=record
                            )
                        )
        return


    def run(self, server):
        print("Running on server", server, sep=" ")
        while True:
            action = input("Enter 1 to create file, 2 to delete file, 3 to append to file, 4 to take a snapshot, q to quit: ")
            if action == "1":
                self.create_file(self.master_stub)
            elif action == "2":
                self.delete_file(self.master_stub)
            elif action == "3":
                self.append(self.master_stub)
            elif action == "4":
                self.take_snapshot(self.master_stub)
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