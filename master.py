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
import os
import datetime
import shutil
import random

CHUNK_SIZE = 16
NUM_SERVERS = 5

data_lock = threading.Lock()

class MasterToClient(gfs_pb2_grpc.MasterToClientServicer) :
    def __init__(self, port, prev_id) -> None:
        self.clientIDs = 0
        self.file_chunks_path = "metadata/file_chunks.json"  #file to store mapping for chunks in each file
        self.chunk_locations_path = "metadata/chunk_locations.json"

        self.chunk_ID = f'{port}:{prev_id}'
        self.server_tracker = 0
        self.snapshot_dir = "snapshot"
        self.metadata_dir = "metadata"
        self.chunk_dir = "chunkservers"

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
            if len(chunks) == 0:
                yield gfs_pb2.ChunkLocationsResponse(status=2)
            else:
                for chunk in chunks:
                    servers = remove_from_json(chunk, self.chunk_locations_path)
                    response = gfs_pb2.ChunkLocationsResponse(chunk_id=chunk, status=1)
                    response.server.extend(servers[1])
                    yield response
        elif popped[0] == 2:
            yield gfs_pb2.ChunkLocationsResponse(status=0, message = "File does not exist.")
        elif popped[0] == 0:
            yield gfs_pb2.ChunkLocationsResponse(status = 0, message = "No files have been created yet.")


    def GetNewChunkID(self):
        chunkID = ''
        IDnum = ''
        print(self.chunk_ID)
        for i in range(len(self.chunk_ID)):
            print(i)
            if self.chunk_ID[i] == ':':
                chunkID += self.chunk_ID[i]
                i += 1
                
                break
            chunkID += self.chunk_ID[i]
        print("out")
        print(i)
        print(len(self.chunk_ID))
        print(self.chunk_ID)
        while i < len(self.chunk_ID):
            IDnum += self.chunk_ID[i]
            i += 1

        print(IDnum)
        num = int(IDnum)
        num += 1
        # Write the updated num to chunk_id_tracker.txt
        with open("chunk_id_tracker.txt", "w") as file:
            file.write(str(num))

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
        # print("here")
        file_name = request.name
        num_chunks = request.new_chunk
        chunks = read_from_json(file_name, self.file_chunks_path)
        if chunks[0] == 0 or chunks[0] == 2:
            yield gfs_pb2.ChunkLocationsResponse(status=0)
        else:
            if len(chunks[1]) == 0:
                num_chunks += 1
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
    

    def GetChunkLocations(self, request, context):
        file_name = request.name
        flag, chunks = read_from_json(file_name, self.file_chunks_path)
        if flag == 0 or flag == 2:
            yield gfs_pb2.ChunkLocationsResponse(status=0)
        else:
            for chunk in chunks:
                response = gfs_pb2.ChunkLocationsResponse(chunk_id=chunk, status=1)
                servers = read_from_json(chunk, self.chunk_locations_path)
                response.server.extend(servers[1])
                yield response


    def CreateSnapshot(self, request, context):
        print("Creating snapshot")
        if not os.path.exists(self.snapshot_dir):
            os.makedirs(self.snapshot_dir)
    
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        snapshot_path = os.path.join(self.snapshot_dir, timestamp)
        
        try:
            os.makedirs(snapshot_path)
            
            metadata_snapshot = os.path.join(snapshot_path, 'metadata')
            if os.path.exists(self.metadata_dir):
                shutil.copytree(self.metadata_dir, metadata_snapshot)
            
            chunks_snapshot = os.path.join(snapshot_path, 'chunkservers')
            if os.path.exists(self.chunk_dir):
                shutil.copytree(self.chunk_dir, chunks_snapshot)
                
            print(f"Created snapshot at {snapshot_path}")
            return gfs_pb2.Status(
            code=0,  # 0 typically indicates success
            message="Snapshot taken successfully"
        )   
            
        except Exception as e:
            print(f"Error creating snapshot: {e}")
            # Clean up failed snapshot attempt
            if os.path.exists(snapshot_path):
                shutil.rmtree(snapshot_path)
            return gfs_pb2.Status(
            code=1,  # 0 typically indicates success
            message="Snapshot failed"
        )   
class ChunkToMaster():
    def __init__(self, chunk_servers) -> None:
        self.chunk_servers = chunk_servers
        self.chunk_channels = [grpc.insecure_channel(chunkserver) for chunkserver in chunk_servers]
        self.chunk_stubs = [gfs_pb2_grpc.ChunkToMasterStub(self.chunk_channels[i]) for i in range(len(self.chunk_channels))]
        
        self.heartbeats_done = 0
        self.file_chunks_path = "metadata/file_chunks.json"  #file to store mapping for chunks in each file
        self.chunk_locations_path = "metadata/chunk_locations.json"
        self.chunk_servers_path = "chunkservers"
        self.chunk_heart_beats = {}

    def balance_chunks(self):
        # handle load balancing of the chunks
        # check if they are already balanced
        # if all servers have some chunks, then they are balanced
        # if any file is empty, then we balance all the chunks in the orignal order 012, 123, etc


        pass

    def send_heartbeat(self):
        print("Sending heartbeat")

        for chunk_server, stub in zip(self.chunk_servers, self.chunk_stubs):
            # print(chunk_server, stub)
            try:
                response = stub.Heartbeat(gfs_pb2.EmptyRequest())
                print(chunk_server, response.message)
                chunk_num = int(chunk_server.split(":")[1])
                # print(chunk_num)
                self.chunk_heart_beats[chunk_num-50054] = response.code
                
            except Exception as e:
                print(f"Error sending heartbeat to {chunk_server}: {e}")

        self.heartbeats_done += 1
        flag = True
        for server_number, chunk_server in enumerate(self.chunk_servers):
            if self.chunk_heart_beats[server_number] == 1:
                flag = False
                # shuffle the chunks
                chunk_num = int(chunk_server.split(":")[1])
                server_path = os.path.join(self.chunk_servers_path, f"{chunk_num}.json")
                with open (server_path, 'r') as file:
                    data = json.load(file)
                    print(data)
                    # make this chunk_num.json file empty
                    with open(server_path, 'w') as file:
                        json.dump({}, file, indent=4)
                    for key, value in data.items():
                        print(f"Chunk ID: {key}, Data: {value}")
                        with open (self.chunk_locations_path, 'r') as file:
                            chunk_locations_data = json.load(file)
                            # print(chunk_locations_data)
                            if key in chunk_locations_data:
                                servers = chunk_locations_data[key]
                                print(servers)
                                servers.remove(server_number)
                                while True:
                                    good_server = math.floor(random.random()*5)
                                    if good_server not in servers and self.chunk_heart_beats[good_server] == 0:
                                        # add chunk_id and data to this servers json.
                                        update_json({key: value}, os.path.join(self.chunk_servers_path, f"5005{good_server+4}.json"))
                                        servers.append(good_server)
                                        break
                                chunk_locations_data[key] = servers
                                with open(self.chunk_locations_path, 'w') as file:
                                    json.dump(chunk_locations_data, file, indent=4)

        if flag:
            self.balance_chunks()


def read_chunk_id():
    try:
        with open("chunk_id_tracker.txt", "r") as file:
            return int(file.read().strip())
    except FileNotFoundError:
        return 0
    except ValueError:
        print("Invalid value in chunk_id_tracker.txt, defaulting to 0")
        return 0
    
def serve(port):
    prev_id = read_chunk_id()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    gfs_pb2_grpc.add_MasterToClientServicer_to_server(MasterToClient(port, prev_id=prev_id), server)
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

    if(port == 50051): # primary master
        try:
            while True:
                chunk.send_heartbeat()
                time.sleep(30)
        except KeyboardInterrupt:
            pass        
    server.wait_for_termination()

if __name__ == "__main__":
    os.makedirs("metadata", exist_ok=True)
    ports = [50051, 50052, 50053]
    threads = []
    for port in ports:
        thread = threading.Thread(target=serve, args=(port,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
