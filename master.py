import logging
from concurrent import futures
import threading
import time
import math

import grpc
import gfs_pb2
import gfs_pb2_grpc
import json

CHUNK_SIZE = 16

data_lock = threading.Lock()

# add to json/modify existing values
def update_json(data_update, file_path):
    flag = 1
    with data_lock:
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

            keys = list(data_update.keys())
            if keys[0] in data:
                flag = 2

            data.update(data_update)

            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
        except FileNotFoundError:
            with open(file_path, 'w') as file:
                json.dump(data_update, file, indent=4)
    return flag

# returns value corresponding to given key
def read_from_json(key, file_path):
    flag = 2
    record = []
    with data_lock:
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            if key in data:
                flag = 1
                record = data[key]
        except FileNotFoundError:
            flag = 0
    return [flag, record]

# delete from json and return popped value
def remove_from_json(key, file_path):
    flag = 1
    value = None
    with data_lock:
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

            if key not in data:
                flag = 2
            else:
                value = data.pop(key)
            
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
        except FileNotFoundError:
            flag = 0
    return [flag, value]




class MasterToClient(gfs_pb2_grpc.MasterToClientServicer) :
    def __init__(self) -> None:
        self.clientIDs = 0
        self.file_chunks_path = "metadata/file_chunks.json"  #file to store mapping for chunks in each file
        self.chunk_locations_path = "metadata/chunk_locations.json"

    def GetClientID(self, request, context):
        self.clientIDs += 1
        return gfs_pb2.IDResponse(client_id = self.clientIDs)
    
    def CreateFile(self, request, context):
        new_file = {request.name : []}
        flag = update_json(new_file, self.file_chunks_path)
        if flag == 1:
            return gfs_pb2.Status(code = 1)
        elif flag == 2:
            return gfs_pb2.Status(code = 0, message = "File already exists.")

    def DeleteFile(self, request, context):
        popped = remove_from_json(request.name, self.file_chunks_path)
        if popped[0] == 1:
            chunks = popped[1]
            for chunk in chunks:
                servers = remove_from_json(chunk, self.chunk_locations_path)
                # TODO: handle deleting all chunks from chunkservers
            return gfs_pb2.Status(code = 1)
        elif popped[0] == 2:
            return gfs_pb2.Status(code = 0, message = "File does not exist.")
        elif popped[0] == 0:
            return gfs_pb2.Status(code = 0, message = "No files have been created yet.")
        


        



    # def LocateChunks(self, request, context):
    #     file_name = request.name
    #     start_idx = request.idx
    #     content_length = request.length
    #     chunks = read_from_json(file_name, self.file_chunks_path)
    #     if chunks[0] == 0 or chunks[0] == 2:
    #         yield gfs_pb2.ChunkLocation(status=0)
    #     else:
    #         num_chunks = None
    #         if len(chunks[1]) == 0:
    #             start_idx = 0
    #             num_chunks = math.ceil(content_length/CHUNK_SIZE)
    #         elif len(chunks[1])*CHUNK_SIZE <= start_idx:
    #             start_idx = len(chunks[1])*CHUNK_SIZE
    #             num_chunks = math.ceil(content_length/CHUNK_SIZE)
    #         elif (start_idx+content_length-1)/CHUNK_SIZE > len(chunks[1]):
    #             num_chunks = math.ceil((start_idx+content_length-1-len(chunks[1])*CHUNK_SIZE)/CHUNK_SIZE)
    #         if num_chunks != None:

class ChunkToMaster():
    def __init__(self, chunk_servers) -> None:
        self.chunk_channels = [grpc.insecure_channel(chunkserver) for chunkserver in chunk_servers]
        self.chunk_stubs = [gfs_pb2_grpc.ChunkToMasterStub(self.chunk_channels[i]) for i in range(len(self.chunk_channels))]
        # for stub in self.chunk_stubs:
        #     print(stub)
        #     print()
        
        self.heartbeats_done = 0

    def send_heartbeat(self):
        print("Sending heartbeat")

        for stub in self.chunk_stubs:
            try:
                response = stub.Heartbeat(gfs_pb2.EmptyRequest())
                print(response.message)
            except Exception as e:
                print(f"Error sending heartbeat to {stub}: {e}")
    




def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    gfs_pb2_grpc.add_MasterToClientServicer_to_server(MasterToClient(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Server running on port {port}")
    

    chunk = ChunkToMaster([
        "localhost:50054",
        "localhost:50055",
        "localhost:50056", 
        "localhost:50057",
        "localhost:50058"
    ])
    chunk.send_heartbeat()
    server.wait_for_termination()

if __name__ == "__main__":
    ports = [50051, 50052, 50053]
    threads = []
    for port in ports:
        thread = threading.Thread(target=serve, args=(port,))
        thread.start()
        threads.append(thread)

    for thread in threads:  
        thread.join()

       
