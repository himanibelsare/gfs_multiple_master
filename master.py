import logging
from concurrent import futures
import threading
import time

import grpc
import gfs_pb2
import gfs_pb2_grpc
import json

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
        except FileNotFoundError:
            flag = 0
    return [flag, value]

class MasterToClient(gfs_pb2_grpc.MasterToClientServicer) :
    def __init__(self) -> None:
        self.clientIDs = 0
        self.file_chunks_path = "master_data/file_chunks.json"  #file to store mapping for chunks in each file
        self.chunk_locations_path = "master_data/chunk_locations.json"

    def GetClientID(self, request, context):
        self.clientIDs += 1
        return gfs_pb2.IDResponse(client_id = self.clientIDs)
    
    def create_file(self, request, context):
        new_file = {request.string : []}
        flag = update_json(new_file, self.file_chunks_path)
        if flag == 1:
            return gfs_pb2.Status(code = 1)
        elif flag == 2:
            return gfs_pb2.Status(code = 0, message = "File already exists.")

    def delete_file(self, request, context):
        popped = remove_from_json(request.string, self.file_chunks_path)
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


def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    gfs_pb2_grpc.add_MasterToClientServicer_to_server(MasterToClient(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Server running on port {port}")
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
