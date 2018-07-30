# Copyright (c) 2018 IoTeX
# This is an alpha (internal) release and is not suitable for production. This source code is provided 'as is' and no
# warranties are given as to title or non-infringement, merchantability or fitness for purpose and, to the extent
# permitted by law, all liability for your use of the code is disclaimed. This source code is governed by Apache
# License 2.0 that can be found in the LICENSE file.

"""This module defines a consensus client which interfaces with the RollDPoS consensus engine in Go"""

import grpc

from proto import simulator_pb2_grpc
from proto import simulator_pb2

class Consensus:
    def __init__(self):
        self.channel = grpc.insecure_channel('localhost:50051')
        self.stub = simulator_pb2_grpc.SimulatorStub(self.channel)

    @staticmethod
    def initConsensus(nHonest, nFS, nBF, nConnections, connections):
        """Static message which sends a request to initialize n consensus schemes on the consensus server"""

        print("sent init request with %d honest nodes, %d failure stop nodes, and %d byzantine fault nodes to consensus engine" % (nHonest, nFS, nBF))
        channel = grpc.insecure_channel('localhost:50051')
        stub = simulator_pb2_grpc.SimulatorStub(channel)

        connectionsRequest = [simulator_pb2.InitRequest.Connection(nodes=nodes) for nodes in connections]
        response = stub.Init(simulator_pb2.InitRequest(nHonest=nHonest,
                                                       nFS=nFS,
                                                       nBF=nBF,
                                                       nConnections=nConnections,
                                                       connections=connectionsRequest))
        response = [[r.playerID, (r.internalMsgType, r.value)] for r in response]

        return response

    def processMessage(self, sender, msg):
        """Sends a view state change message to consensus engine and returns responses"""

        # note: msg is a tuple: (msgType, msgBody)
        internalMsgType, value = msg
        
        response = self.stub.Ping(simulator_pb2.Request(sender=sender,
                                                        recipient=self.playerID,
                                                        internalMsgType=internalMsgType,
                                                        value=value))

        response = [[r.recipient, r.messageType, (r.internalMsgType, r.value)] for r in response]

        return response

    @staticmethod
    def close():
        print("closing consensus server")
        
        channel = grpc.insecure_channel('localhost:50051')
        stub = simulator_pb2_grpc.SimulatorStub(channel)
        
        stub.Exit(simulator_pb2.Empty())
        
