# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: gfs.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'gfs.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\tgfs.proto\x12\x03gfs\"\x0e\n\x0c\x45mptyRequest\"\x1f\n\nIDResponse\x12\x11\n\tclient_id\x18\x01 \x01(\x05\"0\n\rAppendRequest\x12\x11\n\tnew_chunk\x18\x01 \x01(\x05\x12\x0c\n\x04name\x18\x02 \x01(\t\">\n\x11WriteChunkRequest\x12\x0e\n\x06length\x18\x01 \x01(\x05\x12\x0b\n\x03idx\x18\x02 \x01(\x05\x12\x0c\n\x04name\x18\x03 \x01(\t\"\x1b\n\x0b\x46ileRequest\x12\x0c\n\x04name\x18\x01 \x01(\t\">\n\x0c\x46ileResponse\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04size\x18\x02 \x01(\x03\x12\x12\n\ncreated_at\x18\x03 \x01(\t\".\n\x0c\x43hunkRequest\x12\x10\n\x08\x63hunk_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\";\n\tChunkData\x12\x10\n\x08\x63hunk_id\x18\x01 \x01(\t\x12\x0c\n\x04\x64\x61ta\x18\x02 \x01(\t\x12\x0e\n\x06offset\x18\x03 \x01(\x05\"J\n\x16\x43hunkLocationsResponse\x12\x0e\n\x06server\x18\x01 \x03(\x05\x12\x0e\n\x06status\x18\x02 \x01(\x05\x12\x10\n\x08\x63hunk_id\x18\x03 \x01(\t\"H\n\rChunkLocation\x12\x0e\n\x06status\x18\x01 \x01(\x05\x12\x10\n\x08\x63hunk_id\x18\x02 \x01(\t\x12\x15\n\rchunk_servers\x18\x03 \x03(\t\"Z\n\x14\x43hunkDetailsResponse\x12\x10\n\x08\x63hunk_id\x18\x01 \x01(\t\x12\x0c\n\x04size\x18\x02 \x01(\x03\x12\x11\n\tlocations\x18\x03 \x03(\t\x12\x0f\n\x07version\x18\x04 \x01(\x05\"U\n\x10HeartbeatRequest\x12\x11\n\tserver_id\x18\x01 \x01(\t\x12\x15\n\rstored_chunks\x18\x02 \x03(\t\x12\x17\n\x0f\x61vailable_space\x18\x03 \x01(\x03\"B\n\rChunkResponse\x12\x10\n\x08\x63hunk_id\x18\x01 \x01(\t\x12\x0e\n\x06status\x18\x02 \x01(\t\x12\x0f\n\x07version\x18\x03 \x01(\x05\"\x18\n\x06String\x12\x0e\n\x06string\x18\x01 \x01(\t\"\'\n\x06Status\x12\x0c\n\x04\x63ode\x18\x01 \x01(\x05\x12\x0f\n\x07message\x18\x02 \x01(\t2\xe1\x04\n\x0eMasterToClient\x12\x33\n\x0bGetClientID\x12\x11.gfs.EmptyRequest\x1a\x0f.gfs.IDResponse\"\x00\x12-\n\nCreateFile\x12\x10.gfs.FileRequest\x1a\x0b.gfs.Status\"\x00\x12-\n\nDeleteFile\x12\x10.gfs.FileRequest\x1a\x0b.gfs.Status\"\x00\x12\x35\n\tListFiles\x12\x11.gfs.EmptyRequest\x1a\x11.gfs.FileResponse\"\x00\x30\x01\x12\x44\n\x11GetChunkLocations\x12\x10.gfs.FileRequest\x1a\x1b.gfs.ChunkLocationsResponse\"\x00\x12?\n\x0b\x43ommitChunk\x12\x11.gfs.ChunkRequest\x1a\x1b.gfs.ChunkLocationsResponse\"\x00\x12\x36\n\x13GetFileCreateStatus\x12\x10.gfs.FileRequest\x1a\x0b.gfs.Status\"\x00\x12\x41\n\x0fGetChunkDetails\x12\x11.gfs.ChunkRequest\x1a\x19.gfs.ChunkDetailsResponse\"\x00\x12>\n\x0cLocateChunks\x12\x16.gfs.WriteChunkRequest\x1a\x12.gfs.ChunkLocation\"\x00\x30\x01\x12\x43\n\x0c\x41ppendRecord\x12\x12.gfs.AppendRequest\x1a\x1b.gfs.ChunkLocationsResponse\"\x00\x30\x01\x32\xa1\x01\n\rChunkToClient\x12.\n\rAppendToChunk\x12\x0e.gfs.ChunkData\x1a\x0b.gfs.Status\"\x00\x12,\n\x0b\x43reateChunk\x12\x0e.gfs.ChunkData\x1a\x0b.gfs.Status\"\x00\x12\x32\n\tReadChunk\x12\x11.gfs.ChunkRequest\x1a\x0e.gfs.ChunkData\"\x00\x30\x01\x32x\n\x0c\x43hunkToChunk\x12.\n\x0b\x43reateChunk\x12\x0e.gfs.ChunkData\x1a\x0b.gfs.Status\"\x00(\x01\x12\x38\n\x0fReadEntireChunk\x12\x11.gfs.ChunkRequest\x1a\x0e.gfs.ChunkData\"\x00\x30\x01\x32\xdb\x01\n\rChunkToMaster\x12/\n\x0b\x43ommitChunk\x12\x11.gfs.ChunkRequest\x1a\x0b.gfs.Status\"\x00\x12\x32\n\x0c\x44\x65leteChunks\x12\x11.gfs.ChunkRequest\x1a\x0b.gfs.Status\"\x00(\x01\x12\x32\n\x0eReplicateChunk\x12\x11.gfs.ChunkRequest\x1a\x0b.gfs.Status\"\x00\x12\x31\n\tHeartbeat\x12\x15.gfs.HeartbeatRequest\x1a\x0b.gfs.Status\"\x00\x32K\n\rMasterToChunk\x12:\n\x0bQueryChunks\x12\x11.gfs.ChunkRequest\x1a\x12.gfs.ChunkResponse\"\x00(\x01\x30\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'gfs_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_EMPTYREQUEST']._serialized_start=18
  _globals['_EMPTYREQUEST']._serialized_end=32
  _globals['_IDRESPONSE']._serialized_start=34
  _globals['_IDRESPONSE']._serialized_end=65
  _globals['_APPENDREQUEST']._serialized_start=67
  _globals['_APPENDREQUEST']._serialized_end=115
  _globals['_WRITECHUNKREQUEST']._serialized_start=117
  _globals['_WRITECHUNKREQUEST']._serialized_end=179
  _globals['_FILEREQUEST']._serialized_start=181
  _globals['_FILEREQUEST']._serialized_end=208
  _globals['_FILERESPONSE']._serialized_start=210
  _globals['_FILERESPONSE']._serialized_end=272
  _globals['_CHUNKREQUEST']._serialized_start=274
  _globals['_CHUNKREQUEST']._serialized_end=320
  _globals['_CHUNKDATA']._serialized_start=322
  _globals['_CHUNKDATA']._serialized_end=381
  _globals['_CHUNKLOCATIONSRESPONSE']._serialized_start=383
  _globals['_CHUNKLOCATIONSRESPONSE']._serialized_end=457
  _globals['_CHUNKLOCATION']._serialized_start=459
  _globals['_CHUNKLOCATION']._serialized_end=531
  _globals['_CHUNKDETAILSRESPONSE']._serialized_start=533
  _globals['_CHUNKDETAILSRESPONSE']._serialized_end=623
  _globals['_HEARTBEATREQUEST']._serialized_start=625
  _globals['_HEARTBEATREQUEST']._serialized_end=710
  _globals['_CHUNKRESPONSE']._serialized_start=712
  _globals['_CHUNKRESPONSE']._serialized_end=778
  _globals['_STRING']._serialized_start=780
  _globals['_STRING']._serialized_end=804
  _globals['_STATUS']._serialized_start=806
  _globals['_STATUS']._serialized_end=845
  _globals['_MASTERTOCLIENT']._serialized_start=848
  _globals['_MASTERTOCLIENT']._serialized_end=1457
  _globals['_CHUNKTOCLIENT']._serialized_start=1460
  _globals['_CHUNKTOCLIENT']._serialized_end=1621
  _globals['_CHUNKTOCHUNK']._serialized_start=1623
  _globals['_CHUNKTOCHUNK']._serialized_end=1743
  _globals['_CHUNKTOMASTER']._serialized_start=1746
  _globals['_CHUNKTOMASTER']._serialized_end=1965
  _globals['_MASTERTOCHUNK']._serialized_start=1967
  _globals['_MASTERTOCHUNK']._serialized_end=2042
# @@protoc_insertion_point(module_scope)
