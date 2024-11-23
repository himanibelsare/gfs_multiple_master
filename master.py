import logging
from concurrent import futures
import threading
import time

import grpc
import gfs_pb2
import gfs_pb2_grpc
import json

data_lock = threading.Lock()

def update_json(data_update, file_path):
    with data_lock:
        try:
            # Read the existing data
            with open(file_path, 'r') as file:
                data = json.load(file)

            # Update the data
            data.update(data_update)

            # Write back the updated data
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
        except FileNotFoundError:
            # Handle the case where the file doesn't exist
            with open(file_path, 'w') as file:
                json.dump(data_update, file, indent=4)

class MasterToClient(gfs_pb2_grpc.MasterToClientServicer) :
    def __init__(self) -> None:
        self.clientIDs = 0
        self.file_data_path = "files.json"  #file to store mapping for chunks in each file

    def get_id(self, request, context):
        self.clientIDs += 1
        return gfs_pb2.IDResponse(client_id = self.clientIDs)
    
    # def create_file(self, request, context):
        

def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
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
