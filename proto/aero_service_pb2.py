# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: aero_service.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'aero_service.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12\x61\x65ro_service.proto\x12\x04\x61\x65ro\"?\n\nAudioChunk\x12\x0f\n\x07samples\x18\x01 \x01(\x0c\x12\x13\n\x0bsample_rate\x18\x02 \x01(\x05\x12\x0b\n\x03\x65ou\x18\x03 \x01(\x08\"L\n\x12\x45nhancedAudioChunk\x12\x0f\n\x07samples\x18\x01 \x01(\x0c\x12\x13\n\x0bsample_rate\x18\x02 \x01(\x05\x12\x10\n\x08is_final\x18\x03 \x01(\x08\x32R\n\x0f\x41\x65roEnhancement\x12?\n\rEnhanceStream\x12\x10.aero.AudioChunk\x1a\x18.aero.EnhancedAudioChunk(\x01\x30\x01\x62\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'aero_service_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_AUDIOCHUNK']._serialized_start=28
  _globals['_AUDIOCHUNK']._serialized_end=91
  _globals['_ENHANCEDAUDIOCHUNK']._serialized_start=93
  _globals['_ENHANCEDAUDIOCHUNK']._serialized_end=169
  _globals['_AEROENHANCEMENT']._serialized_start=171
  _globals['_AEROENHANCEMENT']._serialized_end=253
# @@protoc_insertion_point(module_scope)
