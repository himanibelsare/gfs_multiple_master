# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import gfs_pb2 as gfs__pb2

GRPC_GENERATED_VERSION = '1.66.2'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in gfs_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class MasterToClientStub(object):
    """Interface exported by the master server
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetClientID = channel.unary_unary(
                '/gfs.MasterToClient/GetClientID',
                request_serializer=gfs__pb2.EmptyRequest.SerializeToString,
                response_deserializer=gfs__pb2.IDResponse.FromString,
                _registered_method=True)
        self.CreateFile = channel.unary_unary(
                '/gfs.MasterToClient/CreateFile',
                request_serializer=gfs__pb2.FileRequest.SerializeToString,
                response_deserializer=gfs__pb2.Status.FromString,
                _registered_method=True)
        self.DeleteFile = channel.unary_unary(
                '/gfs.MasterToClient/DeleteFile',
                request_serializer=gfs__pb2.FileRequest.SerializeToString,
                response_deserializer=gfs__pb2.Status.FromString,
                _registered_method=True)
        self.ListFiles = channel.unary_stream(
                '/gfs.MasterToClient/ListFiles',
                request_serializer=gfs__pb2.EmptyRequest.SerializeToString,
                response_deserializer=gfs__pb2.FileResponse.FromString,
                _registered_method=True)
        self.GetChunkLocations = channel.unary_unary(
                '/gfs.MasterToClient/GetChunkLocations',
                request_serializer=gfs__pb2.FileRequest.SerializeToString,
                response_deserializer=gfs__pb2.ChunkLocationsResponse.FromString,
                _registered_method=True)
        self.CommitChunk = channel.unary_unary(
                '/gfs.MasterToClient/CommitChunk',
                request_serializer=gfs__pb2.ChunkRequest.SerializeToString,
                response_deserializer=gfs__pb2.ChunkLocationsResponse.FromString,
                _registered_method=True)
        self.GetFileCreateStatus = channel.unary_unary(
                '/gfs.MasterToClient/GetFileCreateStatus',
                request_serializer=gfs__pb2.FileRequest.SerializeToString,
                response_deserializer=gfs__pb2.Status.FromString,
                _registered_method=True)
        self.GetChunkDetails = channel.unary_unary(
                '/gfs.MasterToClient/GetChunkDetails',
                request_serializer=gfs__pb2.ChunkRequest.SerializeToString,
                response_deserializer=gfs__pb2.ChunkDetailsResponse.FromString,
                _registered_method=True)
        self.LocateChunks = channel.unary_stream(
                '/gfs.MasterToClient/LocateChunks',
                request_serializer=gfs__pb2.WriteChunkRequest.SerializeToString,
                response_deserializer=gfs__pb2.ChunkLocation.FromString,
                _registered_method=True)
        self.AppendRecord = channel.unary_stream(
                '/gfs.MasterToClient/AppendRecord',
                request_serializer=gfs__pb2.AppendRequest.SerializeToString,
                response_deserializer=gfs__pb2.ChunkLocationsResponse.FromString,
                _registered_method=True)


class MasterToClientServicer(object):
    """Interface exported by the master server
    """

    def GetClientID(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateFile(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteFile(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ListFiles(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetChunkLocations(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CommitChunk(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetFileCreateStatus(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetChunkDetails(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def LocateChunks(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def AppendRecord(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MasterToClientServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'GetClientID': grpc.unary_unary_rpc_method_handler(
                    servicer.GetClientID,
                    request_deserializer=gfs__pb2.EmptyRequest.FromString,
                    response_serializer=gfs__pb2.IDResponse.SerializeToString,
            ),
            'CreateFile': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateFile,
                    request_deserializer=gfs__pb2.FileRequest.FromString,
                    response_serializer=gfs__pb2.Status.SerializeToString,
            ),
            'DeleteFile': grpc.unary_unary_rpc_method_handler(
                    servicer.DeleteFile,
                    request_deserializer=gfs__pb2.FileRequest.FromString,
                    response_serializer=gfs__pb2.Status.SerializeToString,
            ),
            'ListFiles': grpc.unary_stream_rpc_method_handler(
                    servicer.ListFiles,
                    request_deserializer=gfs__pb2.EmptyRequest.FromString,
                    response_serializer=gfs__pb2.FileResponse.SerializeToString,
            ),
            'GetChunkLocations': grpc.unary_unary_rpc_method_handler(
                    servicer.GetChunkLocations,
                    request_deserializer=gfs__pb2.FileRequest.FromString,
                    response_serializer=gfs__pb2.ChunkLocationsResponse.SerializeToString,
            ),
            'CommitChunk': grpc.unary_unary_rpc_method_handler(
                    servicer.CommitChunk,
                    request_deserializer=gfs__pb2.ChunkRequest.FromString,
                    response_serializer=gfs__pb2.ChunkLocationsResponse.SerializeToString,
            ),
            'GetFileCreateStatus': grpc.unary_unary_rpc_method_handler(
                    servicer.GetFileCreateStatus,
                    request_deserializer=gfs__pb2.FileRequest.FromString,
                    response_serializer=gfs__pb2.Status.SerializeToString,
            ),
            'GetChunkDetails': grpc.unary_unary_rpc_method_handler(
                    servicer.GetChunkDetails,
                    request_deserializer=gfs__pb2.ChunkRequest.FromString,
                    response_serializer=gfs__pb2.ChunkDetailsResponse.SerializeToString,
            ),
            'LocateChunks': grpc.unary_stream_rpc_method_handler(
                    servicer.LocateChunks,
                    request_deserializer=gfs__pb2.WriteChunkRequest.FromString,
                    response_serializer=gfs__pb2.ChunkLocation.SerializeToString,
            ),
            'AppendRecord': grpc.unary_stream_rpc_method_handler(
                    servicer.AppendRecord,
                    request_deserializer=gfs__pb2.AppendRequest.FromString,
                    response_serializer=gfs__pb2.ChunkLocationsResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'gfs.MasterToClient', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('gfs.MasterToClient', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class MasterToClient(object):
    """Interface exported by the master server
    """

    @staticmethod
    def GetClientID(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/gfs.MasterToClient/GetClientID',
            gfs__pb2.EmptyRequest.SerializeToString,
            gfs__pb2.IDResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def CreateFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/gfs.MasterToClient/CreateFile',
            gfs__pb2.FileRequest.SerializeToString,
            gfs__pb2.Status.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DeleteFile(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/gfs.MasterToClient/DeleteFile',
            gfs__pb2.FileRequest.SerializeToString,
            gfs__pb2.Status.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ListFiles(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/gfs.MasterToClient/ListFiles',
            gfs__pb2.EmptyRequest.SerializeToString,
            gfs__pb2.FileResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetChunkLocations(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/gfs.MasterToClient/GetChunkLocations',
            gfs__pb2.FileRequest.SerializeToString,
            gfs__pb2.ChunkLocationsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def CommitChunk(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/gfs.MasterToClient/CommitChunk',
            gfs__pb2.ChunkRequest.SerializeToString,
            gfs__pb2.ChunkLocationsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetFileCreateStatus(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/gfs.MasterToClient/GetFileCreateStatus',
            gfs__pb2.FileRequest.SerializeToString,
            gfs__pb2.Status.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def GetChunkDetails(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/gfs.MasterToClient/GetChunkDetails',
            gfs__pb2.ChunkRequest.SerializeToString,
            gfs__pb2.ChunkDetailsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def LocateChunks(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/gfs.MasterToClient/LocateChunks',
            gfs__pb2.WriteChunkRequest.SerializeToString,
            gfs__pb2.ChunkLocation.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def AppendRecord(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/gfs.MasterToClient/AppendRecord',
            gfs__pb2.AppendRequest.SerializeToString,
            gfs__pb2.ChunkLocationsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)


class ChunkToClientStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.AppendToChunk = channel.unary_unary(
                '/gfs.ChunkToClient/AppendToChunk',
                request_serializer=gfs__pb2.ChunkData.SerializeToString,
                response_deserializer=gfs__pb2.Status.FromString,
                _registered_method=True)
        self.CreateChunk = channel.unary_unary(
                '/gfs.ChunkToClient/CreateChunk',
                request_serializer=gfs__pb2.ChunkData.SerializeToString,
                response_deserializer=gfs__pb2.Status.FromString,
                _registered_method=True)
        self.ReadChunk = channel.unary_stream(
                '/gfs.ChunkToClient/ReadChunk',
                request_serializer=gfs__pb2.ChunkRequest.SerializeToString,
                response_deserializer=gfs__pb2.ChunkData.FromString,
                _registered_method=True)


class ChunkToClientServicer(object):
    """Missing associated documentation comment in .proto file."""

    def AppendToChunk(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def CreateChunk(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReadChunk(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ChunkToClientServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'AppendToChunk': grpc.unary_unary_rpc_method_handler(
                    servicer.AppendToChunk,
                    request_deserializer=gfs__pb2.ChunkData.FromString,
                    response_serializer=gfs__pb2.Status.SerializeToString,
            ),
            'CreateChunk': grpc.unary_unary_rpc_method_handler(
                    servicer.CreateChunk,
                    request_deserializer=gfs__pb2.ChunkData.FromString,
                    response_serializer=gfs__pb2.Status.SerializeToString,
            ),
            'ReadChunk': grpc.unary_stream_rpc_method_handler(
                    servicer.ReadChunk,
                    request_deserializer=gfs__pb2.ChunkRequest.FromString,
                    response_serializer=gfs__pb2.ChunkData.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'gfs.ChunkToClient', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('gfs.ChunkToClient', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class ChunkToClient(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def AppendToChunk(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/gfs.ChunkToClient/AppendToChunk',
            gfs__pb2.ChunkData.SerializeToString,
            gfs__pb2.Status.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def CreateChunk(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/gfs.ChunkToClient/CreateChunk',
            gfs__pb2.ChunkData.SerializeToString,
            gfs__pb2.Status.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ReadChunk(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/gfs.ChunkToClient/ReadChunk',
            gfs__pb2.ChunkRequest.SerializeToString,
            gfs__pb2.ChunkData.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)


class ChunkToChunkStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CreateChunk = channel.stream_unary(
                '/gfs.ChunkToChunk/CreateChunk',
                request_serializer=gfs__pb2.ChunkData.SerializeToString,
                response_deserializer=gfs__pb2.Status.FromString,
                _registered_method=True)
        self.ReadEntireChunk = channel.unary_stream(
                '/gfs.ChunkToChunk/ReadEntireChunk',
                request_serializer=gfs__pb2.ChunkRequest.SerializeToString,
                response_deserializer=gfs__pb2.ChunkData.FromString,
                _registered_method=True)


class ChunkToChunkServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CreateChunk(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReadEntireChunk(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ChunkToChunkServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CreateChunk': grpc.stream_unary_rpc_method_handler(
                    servicer.CreateChunk,
                    request_deserializer=gfs__pb2.ChunkData.FromString,
                    response_serializer=gfs__pb2.Status.SerializeToString,
            ),
            'ReadEntireChunk': grpc.unary_stream_rpc_method_handler(
                    servicer.ReadEntireChunk,
                    request_deserializer=gfs__pb2.ChunkRequest.FromString,
                    response_serializer=gfs__pb2.ChunkData.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'gfs.ChunkToChunk', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('gfs.ChunkToChunk', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class ChunkToChunk(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CreateChunk(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(
            request_iterator,
            target,
            '/gfs.ChunkToChunk/CreateChunk',
            gfs__pb2.ChunkData.SerializeToString,
            gfs__pb2.Status.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ReadEntireChunk(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_stream(
            request,
            target,
            '/gfs.ChunkToChunk/ReadEntireChunk',
            gfs__pb2.ChunkRequest.SerializeToString,
            gfs__pb2.ChunkData.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)


class ChunkToMasterStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.CommitChunk = channel.unary_unary(
                '/gfs.ChunkToMaster/CommitChunk',
                request_serializer=gfs__pb2.ChunkRequest.SerializeToString,
                response_deserializer=gfs__pb2.Status.FromString,
                _registered_method=True)
        self.DeleteChunks = channel.stream_unary(
                '/gfs.ChunkToMaster/DeleteChunks',
                request_serializer=gfs__pb2.ChunkRequest.SerializeToString,
                response_deserializer=gfs__pb2.Status.FromString,
                _registered_method=True)
        self.ReplicateChunk = channel.unary_unary(
                '/gfs.ChunkToMaster/ReplicateChunk',
                request_serializer=gfs__pb2.ChunkRequest.SerializeToString,
                response_deserializer=gfs__pb2.Status.FromString,
                _registered_method=True)
        self.Heartbeat = channel.unary_unary(
                '/gfs.ChunkToMaster/Heartbeat',
                request_serializer=gfs__pb2.HeartbeatRequest.SerializeToString,
                response_deserializer=gfs__pb2.Status.FromString,
                _registered_method=True)


class ChunkToMasterServicer(object):
    """Missing associated documentation comment in .proto file."""

    def CommitChunk(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def DeleteChunks(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def ReplicateChunk(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Heartbeat(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ChunkToMasterServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'CommitChunk': grpc.unary_unary_rpc_method_handler(
                    servicer.CommitChunk,
                    request_deserializer=gfs__pb2.ChunkRequest.FromString,
                    response_serializer=gfs__pb2.Status.SerializeToString,
            ),
            'DeleteChunks': grpc.stream_unary_rpc_method_handler(
                    servicer.DeleteChunks,
                    request_deserializer=gfs__pb2.ChunkRequest.FromString,
                    response_serializer=gfs__pb2.Status.SerializeToString,
            ),
            'ReplicateChunk': grpc.unary_unary_rpc_method_handler(
                    servicer.ReplicateChunk,
                    request_deserializer=gfs__pb2.ChunkRequest.FromString,
                    response_serializer=gfs__pb2.Status.SerializeToString,
            ),
            'Heartbeat': grpc.unary_unary_rpc_method_handler(
                    servicer.Heartbeat,
                    request_deserializer=gfs__pb2.HeartbeatRequest.FromString,
                    response_serializer=gfs__pb2.Status.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'gfs.ChunkToMaster', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('gfs.ChunkToMaster', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class ChunkToMaster(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def CommitChunk(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/gfs.ChunkToMaster/CommitChunk',
            gfs__pb2.ChunkRequest.SerializeToString,
            gfs__pb2.Status.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def DeleteChunks(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_unary(
            request_iterator,
            target,
            '/gfs.ChunkToMaster/DeleteChunks',
            gfs__pb2.ChunkRequest.SerializeToString,
            gfs__pb2.Status.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def ReplicateChunk(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/gfs.ChunkToMaster/ReplicateChunk',
            gfs__pb2.ChunkRequest.SerializeToString,
            gfs__pb2.Status.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Heartbeat(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/gfs.ChunkToMaster/Heartbeat',
            gfs__pb2.HeartbeatRequest.SerializeToString,
            gfs__pb2.Status.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)


class MasterToChunkStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.QueryChunks = channel.stream_stream(
                '/gfs.MasterToChunk/QueryChunks',
                request_serializer=gfs__pb2.ChunkRequest.SerializeToString,
                response_deserializer=gfs__pb2.ChunkResponse.FromString,
                _registered_method=True)


class MasterToChunkServicer(object):
    """Missing associated documentation comment in .proto file."""

    def QueryChunks(self, request_iterator, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_MasterToChunkServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'QueryChunks': grpc.stream_stream_rpc_method_handler(
                    servicer.QueryChunks,
                    request_deserializer=gfs__pb2.ChunkRequest.FromString,
                    response_serializer=gfs__pb2.ChunkResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'gfs.MasterToChunk', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('gfs.MasterToChunk', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class MasterToChunk(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def QueryChunks(request_iterator,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.stream_stream(
            request_iterator,
            target,
            '/gfs.MasterToChunk/QueryChunks',
            gfs__pb2.ChunkRequest.SerializeToString,
            gfs__pb2.ChunkResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
