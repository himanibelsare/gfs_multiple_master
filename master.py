import logging
from concurrent import futures
import threading
import time
import math

import grpc
import gfs_pb2
import gfs_pb2_grpc
import json
from json_functions import update_json, read_from_json, remove_from_json

CHUNK_SIZE = 16
NUM_SERVERS = 5

data_lock = threading.Lock()

class MasterToClient(gfs_pb2_grpc.MasterToClientServicer) :
    def __init__(self, port) -> None:
        self.clientIDs = 0
        self.file_chunks_path = "metadata/file_chunks.json"  #file to store mapping for chunks in each file
        self.chunk_locations_path = "metadata/chunk_locations.json"
        self.chunk_ID = f'{port}:0'
        self.server_tracker = 0

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

    def GetNewChunkID(self):
        chunkID = ''
        IDnum = ''
        for i in range(len(self.chunk_ID)):
            if self.chunk_ID[i] == ':':
                chunkID += self.chunk_ID[i]
                i += 1
                break
            chunkID += self.chunk_ID[i]
        while i < len(self.chunk_ID):
            IDnum += self.chunk_ID[i]
            i += 1
        num = int(IDnum)
        num += 1
        chunkID += str(num)
        self.chunk_ID = chunkID

    def CreateChunk(self, file_name):
        self.GetNewChunkID()
        servers = []
        for i in range(3):
            servers.append((self.server_tracker+i)%NUM_SERVERS)
        self.server_tracker += 1
        new_chunk = {self.chunk_ID : servers}
        update_json(new_chunk, self.chunk_locations_path)
        file_data = read_from_json(file_name, self.file_chunks_path)
        new_file_data = file_data[1]
        new_file_data.append(self.chunk_ID)
        file = {file_name : new_file_data}
        update_json(file, self.file_chunks_path)
        return servers
    
    def AppendRecord(self, request, context):
        file_name = request.name
        num_chunks = request.new_chunk
        chunks = read_from_json(file_name, self.file_chunks_path)
        if chunks[0] == 0 or chunks[0] == 2:
            yield gfs_pb2.ChunkLocationsResponse(status=0)
        else:
            if len(chunks[1]) == 0 and num_chunks == 0:
                num_chunks = 1
            else:
                response = gfs_pb2.ChunkLocationsResponse(status=2,chunk_id=chunks[1][-1])
                servers = read_from_json(chunks[1][-1], self.chunk_locations_path)
                response.server.extend(servers[1])
                yield response
            for i in range(num_chunks):
                servers = self.CreateChunk(file_name)
                response = gfs_pb2.ChunkLocationsResponse(status=1,chunk_id=self.chunk_ID)
                response.server.extend(servers)
                yield response

    def CommitChunk(self, request, context):
        file_name = request.name
        servers = self.CreateChunk(file_name)
        response = gfs_pb2.ChunkLocationsResponse(status=1,chunk_id=self.chunk_ID)
        response.server.extend(servers)
        return response
    
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
    gfs_pb2_grpc.add_MasterToClientServicer_to_server(MasterToClient(port), server)
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

    try:
        while True:
            chunk.send_heartbeat()
            time.sleep(20)
    except KeyboardInterrupt:
        print("Shutting down...")
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
