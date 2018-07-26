# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: simulator.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='simulator.proto',
  package='simulator',
  syntax='proto3',
  serialized_pb=_b('\n\x0fsimulator.proto\x12\tsimulator\"C\n\x07Request\x12\x10\n\x08playerID\x18\x01 \x01(\x05\x12\x17\n\x0finternalMsgType\x18\x02 \x01(\r\x12\r\n\x05value\x18\x03 \x01(\t\"N\n\x0bInitRequest\x12\x0f\n\x07nHonest\x18\x01 \x01(\x05\x12\x0b\n\x03nFS\x18\x02 \x01(\x05\x12\x0b\n\x03nBF\x18\x03 \x01(\x05\x12\x14\n\x0cnConnections\x18\x04 \x01(\x05\"D\n\x05Reply\x12\x13\n\x0bmessageType\x18\x01 \x01(\x05\x12\x17\n\x0finternalMsgType\x18\x02 \x01(\r\x12\r\n\x05value\x18\x03 \x01(\t\"D\n\x08Proposal\x12\x10\n\x08playerID\x18\x01 \x01(\x05\x12\x17\n\x0finternalMsgType\x18\x02 \x01(\r\x12\r\n\x05value\x18\x03 \x01(\t\"\x07\n\x05\x45mpty2\xa4\x01\n\tSimulator\x12\x30\n\x04Ping\x12\x12.simulator.Request\x1a\x10.simulator.Reply\"\x00\x30\x01\x12\x37\n\x04Init\x12\x16.simulator.InitRequest\x1a\x13.simulator.Proposal\"\x00\x30\x01\x12,\n\x04\x45xit\x12\x10.simulator.Empty\x1a\x10.simulator.Empty\"\x00\x62\x06proto3')
)




_REQUEST = _descriptor.Descriptor(
  name='Request',
  full_name='simulator.Request',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='playerID', full_name='simulator.Request.playerID', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='internalMsgType', full_name='simulator.Request.internalMsgType', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='simulator.Request.value', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=30,
  serialized_end=97,
)


_INITREQUEST = _descriptor.Descriptor(
  name='InitRequest',
  full_name='simulator.InitRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='nHonest', full_name='simulator.InitRequest.nHonest', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='nFS', full_name='simulator.InitRequest.nFS', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='nBF', full_name='simulator.InitRequest.nBF', index=2,
      number=3, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='nConnections', full_name='simulator.InitRequest.nConnections', index=3,
      number=4, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=99,
  serialized_end=177,
)


_REPLY = _descriptor.Descriptor(
  name='Reply',
  full_name='simulator.Reply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='messageType', full_name='simulator.Reply.messageType', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='internalMsgType', full_name='simulator.Reply.internalMsgType', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='simulator.Reply.value', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=179,
  serialized_end=247,
)


_PROPOSAL = _descriptor.Descriptor(
  name='Proposal',
  full_name='simulator.Proposal',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='playerID', full_name='simulator.Proposal.playerID', index=0,
      number=1, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='internalMsgType', full_name='simulator.Proposal.internalMsgType', index=1,
      number=2, type=13, cpp_type=3, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='value', full_name='simulator.Proposal.value', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=249,
  serialized_end=317,
)


_EMPTY = _descriptor.Descriptor(
  name='Empty',
  full_name='simulator.Empty',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=319,
  serialized_end=326,
)

DESCRIPTOR.message_types_by_name['Request'] = _REQUEST
DESCRIPTOR.message_types_by_name['InitRequest'] = _INITREQUEST
DESCRIPTOR.message_types_by_name['Reply'] = _REPLY
DESCRIPTOR.message_types_by_name['Proposal'] = _PROPOSAL
DESCRIPTOR.message_types_by_name['Empty'] = _EMPTY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Request = _reflection.GeneratedProtocolMessageType('Request', (_message.Message,), dict(
  DESCRIPTOR = _REQUEST,
  __module__ = 'simulator_pb2'
  # @@protoc_insertion_point(class_scope:simulator.Request)
  ))
_sym_db.RegisterMessage(Request)

InitRequest = _reflection.GeneratedProtocolMessageType('InitRequest', (_message.Message,), dict(
  DESCRIPTOR = _INITREQUEST,
  __module__ = 'simulator_pb2'
  # @@protoc_insertion_point(class_scope:simulator.InitRequest)
  ))
_sym_db.RegisterMessage(InitRequest)

Reply = _reflection.GeneratedProtocolMessageType('Reply', (_message.Message,), dict(
  DESCRIPTOR = _REPLY,
  __module__ = 'simulator_pb2'
  # @@protoc_insertion_point(class_scope:simulator.Reply)
  ))
_sym_db.RegisterMessage(Reply)

Proposal = _reflection.GeneratedProtocolMessageType('Proposal', (_message.Message,), dict(
  DESCRIPTOR = _PROPOSAL,
  __module__ = 'simulator_pb2'
  # @@protoc_insertion_point(class_scope:simulator.Proposal)
  ))
_sym_db.RegisterMessage(Proposal)

Empty = _reflection.GeneratedProtocolMessageType('Empty', (_message.Message,), dict(
  DESCRIPTOR = _EMPTY,
  __module__ = 'simulator_pb2'
  # @@protoc_insertion_point(class_scope:simulator.Empty)
  ))
_sym_db.RegisterMessage(Empty)



_SIMULATOR = _descriptor.ServiceDescriptor(
  name='Simulator',
  full_name='simulator.Simulator',
  file=DESCRIPTOR,
  index=0,
  options=None,
  serialized_start=329,
  serialized_end=493,
  methods=[
  _descriptor.MethodDescriptor(
    name='Ping',
    full_name='simulator.Simulator.Ping',
    index=0,
    containing_service=None,
    input_type=_REQUEST,
    output_type=_REPLY,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Init',
    full_name='simulator.Simulator.Init',
    index=1,
    containing_service=None,
    input_type=_INITREQUEST,
    output_type=_PROPOSAL,
    options=None,
  ),
  _descriptor.MethodDescriptor(
    name='Exit',
    full_name='simulator.Simulator.Exit',
    index=2,
    containing_service=None,
    input_type=_EMPTY,
    output_type=_EMPTY,
    options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_SIMULATOR)

DESCRIPTOR.services_by_name['Simulator'] = _SIMULATOR

# @@protoc_insertion_point(module_scope)
