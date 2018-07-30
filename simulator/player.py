# Copyright (c) 2018 IoTeX
# This is an alpha (internal) release and is not suitable for production. This source code is provided 'as is' and no
# warranties are given as to title or non-infringement, merchantability or fitness for purpose and, to the extent
# permitted by law, all liability for your use of the code is disclaimed. This source code is governed by Apache
# License 2.0 that can be found in the LICENSE file.

"""This module defines the Player class, which represents a player in the network and contains functionality to make transactions, propose blocks, and validate blocks.
"""

import random

import grpc
import numpy as np

from proto import simulator_pb2_grpc
from proto import simulator_pb2
import solver
import consensus_client
import consensus_failurestop

# enum for defining the consensus types
class CTypes:
    Honest         = 0
    FailureStop    = 1
    ByzantineFault = 2
    
class Player:
    id = 0 # player id
    
    MEAN_TX_FEE    = 0.2                                 # mean transaction fee
    STD_TX_FEE     = 0.05                                # std of transaction fee
    DUMMY_MSG_TYPE = 1999                                # if there are no messages to process, dummy message is sent to consensus engine
    
    msgMap         = {(DUMMY_MSG_TYPE, bytes()): "dummy msg"} # maps message to message name for printing

    correctHashes  = [] # hashes of blocks proposed by HONEST consensus types
    
    def __init__(self, consensusType):
        """Creates a new Player object"""

        self.id = Player.id # the player's id
        Player.id += 1                 

        self.blockchain   = []    # blockchain (simplified to a list)
        self.connections  = []    # list of connected players
        self.inbound      = []    # inbound messages from other players in the network at heartbeat r
        self.outbound     = []    # outbound messages to other players in the network at heartbeat r
        self.seenMessages = set() # set of seen messages

        if consensusType == CTypes.Honest or consensusType == CTypes.ByzantineFault:
            self.consensus = consensus_client.Consensus()
        elif consensusType == CTypes.FailureStop:
            self.consensus = consensus_failurestop.ConsensusFS()

        self.consensusType      = consensusType
        self.consensus.playerID = self.id
        self.consensus.player   = self
        
        self.nMsgsPassed = [0]
        self.timeCreated = []

    def action(self, heartbeat):
        """Executes the player's actions for heartbeat r"""

        print("player %d action started at heartbeat %f" % (self.id, heartbeat))

        # self.inbound: [sender, (msgType, msgBody), timestamp]
        # print messages
        for sender, msg, timestamp in self.inbound:
            print("received %s from %s with timestamp %f" % (Player.msgMap[msg], sender, timestamp))

        # if the Player received no messages before the current heartbeat, add a `dummy` message so the Player still pings the consensus in case the consensus has something it wants to return
        # an example of when this is useful is in the first round when consensus proposes a message; the Player needs to ping it to receive the proposal
        if len(list(filter(lambda x: x[2] <= heartbeat, self.inbound))) == 0:
            self.inbound += [[-1, (Player.DUMMY_MSG_TYPE, bytes()), heartbeat]]

        # process each inbound message
        for sender, msg, timestamp in self.inbound:
            # note: msg is a tuple: (msgType, msgBody)
            # cannot see the message yet if the heartbeat is less than the timestamp
            if timestamp > heartbeat: continue

            if msg[0] != Player.DUMMY_MSG_TYPE and msg in self.seenMessages: continue
            self.seenMessages.add(msg)

            print("sent %s to consensus engine" % Player.msgMap[msg])
            received = self.consensus.processMessage(sender, msg)
            
            for recipient, mt, v in received:
                # if mt = 2, the msgBody is comprised of message|blockHash
                # recipient is the recipient of the message the consensus sends outwards
                # mt is the message type (0 = view state change message, 1 = block committed, 2 = special case)
                # v is message value

                # TODO: fix this
                '''if "|" in v[1]:
                    separator = v[1].index("|")
                    blockHash = v[1][separator+1:]
                    v = (v[0], v[1][:separator])'''

                if v not in Player.msgMap:
                    Player.msgMap[v] = "msg "+str(len(Player.msgMap))
                print("received %s from consensus engine" % Player.msgMap[v])
                
                if mt == 0: # view state change message
                    self.outbound.append([recipient, v, timestamp])
                elif mt == 1: # block to be committed
                    self.blockchain.append(v[1]) # append block hash
                    self.nMsgsPassed.append(0)
                    self.timeCreated.append(timestamp)
                    print("committed %s to blockchain" % Player.msgMap[v])
                else: # newly proposed block
                    self.outbound.append([recipient, v, timestamp])
                    print("PROPOSED %s BLOCK"%("HONEST" if self.consensusType == CTypes.Honest else "BYZANTINE"))
                    if self.consensusType != CTypes.ByzantineFault:
                        Player.correctHashes.append(blockHash)
                    else:
                        Player.correctHashes.append("")

            # also gossip the current message
            # I think this is not necessary for tendermint so I am commenting it out
            '''if msg[0] != Player.DUMMY_MSG_TYPE and self.consensusType != CTypes.FailureStop:
                self.outbound.append([msg, timestamp])'''
            
        self.inbound = list(filter(lambda x: x[2] > heartbeat, self.inbound)) # get rid of processed messages
        
        return self.sendOutbound()

    def sendOutbound(self):
        """Send all outbound connections to connected nodes.
           Returns list of nodes messages have been sent to"""

        if len(self.outbound) == 0:
            sentMsgs = False
        else:
            sentMsgs = True

        ci = set()

        for recipient, message, timestamp in self.outbound:
            recipient = list(filter(lambda x: x.id == recipient, self.connections))[0] # recipient is an id; we want to find the player which corresponds to this id in the connections
            ci.add(recipient)

            sender = self.id
            self.nMsgsPassed[-1] += 1
            dt = np.random.lognormal(self.NORMAL_MEAN, self.NORMAL_STD) # add propagation time to timestamp
            print("sent %s to %s" % (Player.msgMap[message], recipient.id))
            recipient.inbound.append([sender, message, timestamp+dt])

        self.outbound.clear()
        print()

        return list(ci), sentMsgs

    def __str__(self):
        return "player %s" % (self.id)

    def __repr__(self):
        return "player %s" % (self.id)

    def __hash__(self):
        return self.id
        

            
