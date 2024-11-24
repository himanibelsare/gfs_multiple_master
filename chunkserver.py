import grpc
from concurrent import futures
import time
import os
from datetime import datetime
import threading
# Import the generated gRPC code
import gfs_pb2
import gfs_pb2_grpc

class ChunkServer(gfs_pb2_grpc.ChunkToClientServicer, 
                 gfs_pb2_grpc.ChunkToChunkServicer,
                 gfs_pb2_grpc.ChunkToMasterServicer):
    def __init__(self, server_id, chunk_dir, master_address):
        self.server_id = server_id
        self.chunk_dir = chunk_dir
        self.master_address = master_address
        
        os.makedirs(chunk_dir, exist_ok=True)
        
        # Store chunk metadata
        self.chunks = {}  # chunk_id -> {version, size, etc}
        
        # Connect to master
        self.master_channel = grpc.insecure_channel(master_address)
        self.master_stub = gfs_pb2_grpc.ChunkToMasterStub(self.master_channel)
        
        # Start heartbeat
        self.start_heartbeat()

    def start_heartbeat(self):
        def heartbeat_loop():
            while True:
                try:
                    request = gfs_pb2.HeartbeatRequest(
                        server_id=self.server_id,
                        stored_chunks=list(self.chunks.keys()),
                        available_space=self._get_available_space()
                    )
                    self.master_stub.Heartbeat(request)
                except Exception as e:
                    print(f"Heartbeat failed: {e}")
                time.sleep(10)  # heartbeat every 10 seconds
                
        # Start heartbeat in separate thread
        import threading
        thread = threading.Thread(target=heartbeat_loop, daemon=True)
        thread.start()

    def _get_available_space(self):
        # Get available disk space in chunk directory
        import shutil
        return shutil.disk_usage(self.chunk_dir).free

    # ChunkToClient Service methods
    def CreateChunk(self, request_iterator, context):
        # Handle streaming chunk creation
        chunk_id = None
        chunk_data = bytearray()
        
        try:
            for request in request_iterator:
                if chunk_id is None:
                    chunk_id = request.chunk_id
                chunk_data.extend(request.data)
            
            # Write chunk to disk
            chunk_path = os.path.join(self.chunk_dir, chunk_id)
            with open(chunk_path, 'wb') as f:
                f.write(chunk_data)
            
            # Update metadata
            self.chunks[chunk_id] = {
                'size': len(chunk_data),
                'created_at': datetime.now(),
                'version': 1
            }
            
            return gfs_pb2.Status(code=0, message="Chunk created successfully")
        except Exception as e:
            return gfs_pb2.Status(code=1, message=str(e))

    def ReadChunk(self, request, context):
        chunk_id = request.chunk_id
        chunk_path = os.path.join(self.chunk_dir, chunk_id)
        
        try:
            with open(chunk_path, 'rb') as f:
                while True:
                    data = f.read(4096)  # Read in 4KB chunks
                    if not data:
                        break
                    yield gfs_pb2.ChunkData(
                        chunk_id=chunk_id,
                        data=data
                    )
        except Exception as e:
            context.abort(grpc.StatusCode.NOT_FOUND, str(e))

    # ChunkToChunk Service methods
    def CreateChunk(self, request_iterator, context):
        # Similar to client's CreateChunk but for replication
        pass

    def ReadEntireChunk(self, request, context):
        # Similar to client's ReadChunk but for replication
        pass

    # ChunkToMaster Service methods
    def CommitChunk(self, request, context):
        chunk_id = request.chunk_id
        if chunk_id in self.chunks:
            return gfs_pb2.Status(code=0, message="Chunk committed")
        return gfs_pb2.Status(code=1, message="Chunk not found")

    def DeleteChunks(self, request_iterator, context):
        for request in request_iterator:
            chunk_id = request.chunk_id
            chunk_path = os.path.join(self.chunk_dir, chunk_id)
            try:
                os.remove(chunk_path)
                del self.chunks[chunk_id]
            except Exception as e:
                print(f"Error deleting chunk {chunk_id}: {e}")
        return gfs_pb2.Status(code=0, message="Chunks deleted")

    def ReplicateChunk(self, request, context):
        # Handle chunk replication
        pass




def serve(port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    gfs_pb2_grpc.add_ChunkToClient(ChunkServer(), server)
    gfs_pb2_grpc.add_ChunkToChunk(ChunkServer(), server)
    gfs_pb2_grpc.add_ChunkToMaster(ChunkServer(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Server running on port {port}")
    server.wait_for_termination()

if __name__ == "__main__":
    ports = [50054, 50055, 50056, 50057, 50058]
    threads = []
    for port in ports:
        thread = threading.Thread(target=serve, args=(port,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
