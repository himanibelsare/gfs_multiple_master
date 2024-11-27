import grpc
from concurrent import futures
import time
import os
from datetime import datetime
import threading

import gfs_pb2
import gfs_pb2_grpc
import json
from json_functions import update_json, read_from_json, remove_from_json
from utils import Status

CHUNK_SIZE = 16

def heartbeat():
    return Status(0, "Alive!")

class ChunkServer(gfs_pb2_grpc.ChunkToClientServicer, 
                 gfs_pb2_grpc.ChunkToChunkServicer,
                 gfs_pb2_grpc.ChunkToMasterServicer):
    def __init__(self, chunk_file):
        
        # Store chunk metadata
        self.chunks = {}  # chunk_id -> {version, size, etc}
        self.chunk_file = chunk_file
        
        # # Connect to master
        # self.master_channel = grpc.insecure_channel(master_address)
        # self.master_stub = gfs_pb2_grpc.ChunkToMasterStub(self.master_channel)
        
        # Start heartbeat
        # self.start_heartbeat()

    def Heartbeat(self, request, context):
        return gfs_pb2.Status(
            code=0,  # 0 typically indicates success
            message="Heartbeat received successfully"
        )        

    def _get_available_space(self):
        # Get available disk space in chunk directory
        import shutil
        return shutil.disk_usage(self.chunk_dir).free
    
    def AppendToChunk(self, request, context):
        chunk_id = request.chunk_id
        content = request.data
        curr_data = read_from_json(chunk_id, self.chunk_file)
        if curr_data[1] != None:
            if len(curr_data[1]+content) > CHUNK_SIZE:
                return gfs_pb2.Status(code=0,message="Not enough space.")
            new_data = {chunk_id : curr_data[1]+content}
        else:
            new_data = {chunk_id : content}
        update_json(new_data, self.chunk_file)
        return gfs_pb2.Status(code=1)

    # ChunkToClient Service methods
    def CreateChunk(self, request, context):
        chunk_id = request.chunk_id
        content = request.data
        new_data = {chunk_id : content}
        update_json(new_data, self.chunk_file)
        return gfs_pb2.Status(code=1)

    def ReadChunk(self, request, context):
        chunk_id = request.chunk_id
        flag, curr_data = read_from_json(chunk_id, self.chunk_file)
        return gfs_pb2.ChunkData(data=curr_data)

    def DeleteChunk(self, request, context):
        chunk_id = request.chunk_id
        remove_from_json(chunk_id, self.chunk_file)
        return gfs_pb2.Status()

    def ReplicateChunk(self, request, context):
        # Handle chunk replication
        pass




def serve(port):
    chunk_file = f'{chunk_dir}/{port}.json'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=6))
    gfs_pb2_grpc.add_ChunkToClientServicer_to_server(ChunkServer(chunk_file), server)
    gfs_pb2_grpc.add_ChunkToChunkServicer_to_server(ChunkServer(chunk_file), server)
    gfs_pb2_grpc.add_ChunkToMasterServicer_to_server(ChunkServer(chunk_file), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Server running on port {port}")
    server.wait_for_termination()

if __name__ == "__main__":
    chunk_dir = "chunkservers"
    os.makedirs(chunk_dir, exist_ok=True)
    ports = [50054, 50055, 50056, 50057, 50058]
    threads = []
    for port in ports:
        thread = threading.Thread(target=serve, args=(port,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
