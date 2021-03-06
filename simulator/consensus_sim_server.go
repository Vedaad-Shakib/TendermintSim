package main

import (
	"context"
	"flag"
	"fmt"
	"net"
	"os"
	"time"
	"sync"
	"os/exec"
	"bytes"
	"strconv"

	"google.golang.org/grpc"
	"google.golang.org/grpc/reflection"

	pbsim "github.com/tendermint/tendermint/simulator/proto/simulator"
	"github.com/tendermint/tendermint/consensus"
	"github.com/tendermint/tendermint/config"
	"github.com/tendermint/tendermint/types"
	"github.com/tendermint/tendermint/privval"
	sm "github.com/tendermint/tendermint/state"
	dbm "github.com/tendermint/tendermint/libs/db"
	"github.com/tendermint/tendermint/abci/example/kvstore"
	bc "github.com/tendermint/tendermint/blockchain"
	"github.com/tendermint/tendermint/abci/client"
	mempl "github.com/tendermint/tendermint/mempool"
	"github.com/tendermint/tendermint/evidence"
	"github.com/tendermint/tendermint/libs/log"
	"github.com/tendermint/tendermint/p2p"
)

const (
	port         = ":50051"
	dummyMsgType = 1999
)

// server is used to implement message.SimulatorServer.
type (
	server struct {
		nodes []*consensus.ConsensusReactor
		peers [][]p2p.Peer
		peerState [][]*consensus.PeerState
		connections [][]int
	}
)

// Ping implements simulator.SimulatorServer
func (s *server) Init(in *pbsim.InitRequest, stream pbsim.Simulator_InitServer) error {
	nPlayers   := int(in.NBF) + int(in.NFS) + int(in.NHonest)
	s.nodes     = make([]*consensus.ConsensusReactor, nPlayers)
	s.peers     = make([][]p2p.Peer, nPlayers)
	s.peerState = make([][]*consensus.PeerState, nPlayers)

	for i := 0; i < nPlayers; i++ {
		s.peers[i] = make([]p2p.Peer, nPlayers)
		s.peerState[i] = make([]*consensus.PeerState, nPlayers)
	}

	// make connections double array
	for i := 0; i < len(in.Connections); i++ {
		var nodes []int
		for j := 0; j < int(in.NConnections); j++ {
			nodes = append(nodes, int(in.Connections[i].Nodes[j]))
		}
		s.connections = append(s.connections, nodes)
	}

	// create the genesis, private validator, config files
	cmd := exec.Command("tendermint", "testnet", "--v", strconv.Itoa(nPlayers))
	var out bytes.Buffer
	var stderr bytes.Buffer
	cmd.Stdout = &out
	cmd.Stderr = &stderr
	err := cmd.Run()
	if err != nil {
		fmt.Println(err, stderr.String())
	}

	// create peers and peerStates
	for i := 0; i < nPlayers; i++ {
		for j := 0; j < nPlayers; j++ {
			peer := p2p.CreateRandomPeer(true)
			peerState := consensus.NewPeerState(peer)
			peer.SetLogger(log.NewTMLogger(log.NewSyncWriter(os.Stdout)))
			peerState.SetLogger(log.NewTMLogger(log.NewSyncWriter(os.Stdout)))
			peer.Set(types.PeerStateKey, peerState)

			s.peers[i][j] = peer
			s.peerState[i][j] = peerState
		}
	}

	// create consensusReactors
	for i := 0; i < nPlayers; i++ {
		fmt.Printf("initializing ConsensusReactor %d\n", i)
		cfgSim := config.DefaultConfig()
		cfgSim.SetRoot(fmt.Sprintf("/Users/vedaad/go/src/github.com/tendermint/tendermint/simulator/mytestnet/node%d/config", i))
		cfgSim.Consensus.SkipTimeoutCommit = true
		cfgSim.FastSync = false

		genDoc, err := types.GenesisDocFromFile(fmt.Sprintf("/Users/vedaad/go/src/github.com/tendermint/tendermint/simulator/mytestnet/node%d/config/genesis.json", i))
		if err != nil {
			fmt.Println("cannot read genesis file")
		}
		pv := privval.LoadFilePV(fmt.Sprintf("/Users/vedaad/go/src/github.com/tendermint/tendermint/simulator/mytestnet/node%d/config/priv_validator.json", i))
		state, err := sm.MakeGenesisState(genDoc)
		if err != nil {
			fmt.Println("error making state")
		}
		stateDB := dbm.NewMemDB() // each state needs its own db
		blockDB := dbm.NewMemDB()
		blockStore := bc.NewBlockStore(blockDB)

		app := kvstore.NewKVStoreApplication()

		// one for mempool, one for consensus
		mtx := new(sync.Mutex)
		proxyAppConnMem := abcicli.NewLocalClient(mtx, app)
		proxyAppConnCon := abcicli.NewLocalClient(mtx, app)

		// Make Mempool
		mempool := mempl.NewMempool(cfgSim.Mempool, proxyAppConnMem, 0)
		store := evidence.NewEvidenceStore(dbm.NewMemDB())
		evpool := evidence.NewEvidencePool(stateDB, store)

		blockExec := sm.NewBlockExecutor(stateDB, log.TestingLogger(), proxyAppConnCon, mempool, evpool)
		cs := consensus.NewConsensusState(cfgSim.Consensus, state, blockExec, blockStore, mempool, evpool)
		cs.SetPrivValidator(pv)
		cs.SetLogger(log.NewTMLogger(log.NewSyncWriter(os.Stdout)))

		eventBus := types.NewEventBus()
		eventBus.SetLogger(log.NewTMLogger(log.NewSyncWriter(os.Stdout)))
		if err := eventBus.Start(); err != nil {
			panic(fmt.Sprintf("error starting eventBus", err))
		}
		cs.SetEventBus(eventBus)

		cr := consensus.NewConsensusReactor(cs, false)
		cr.SetLogger(log.NewTMLogger(log.NewSyncWriter(os.Stdout)))

		sw := p2p.NewSwitch(cfgSim.P2P)
		sw.Start()
		cr.SetSwitch(sw)

		if err := cr.Start(); err != nil {
			panic(fmt.Sprintf("error starting consensusReactor", err))
		}

		// wait until new round is started
		out := make(chan interface{}, 1)
		err = eventBus.Subscribe(context.Background(), fmt.Sprintf("node%d", i), types.EventQueryNewRound, out)
		if err != nil {
			fmt.Println("cannot susbcribe to new round event")
		}
		<-out

		// when new peers are added, this function is called
		for _, v := range s.connections[i] {
			cr.SendNewRoundStepMessages(s.peers[v], v)
		}

		s.nodes[i] = cr
		fmt.Printf("initialized ConsensusReactor %d\n", i)
	}

	time.Sleep(10*time.Second)
	return nil
}

// Ping implements simulator.SimulatorServer
func (s *server) Ping(in *pbsim.Request, stream pbsim.Simulator_PingServer) error {
	fmt.Println()
	fmt.Printf("Node %d pinged; opened message stream\n", in.Recipient)

	rec := int(in.Recipient)
	conR := s.nodes[rec]

	conR.SetStream(&stream)

	// if it's a dummy message, don't pass it to consensus
	if in.InternalMsgType != dummyMsgType {
		conR.Receive(byte(in.InternalMsgType), s.peers[rec][int(in.Sender)], in.Value)
	}

	time.Sleep(100*time.Millisecond) // TODO: change this to a wait-until
	conR.SendUnsent()

	for _, v := range s.connections[int(in.Recipient)] {
		conR.GossipDataRoutine(s.peers[rec][v], s.peerState[rec][v], v)
		conR.GossipVotesRoutine(s.peers[rec][v], s.peerState[rec][v], v)
		conR.QueryMaj23Routine(s.peers[rec][v], s.peerState[rec][v], v)
	}

	conR.SetStream(nil)
	fmt.Println("closed message stream")

	return nil
}

func (s *server) Exit(context context.Context, in *pbsim.Empty) (*pbsim.Empty, error) {
	defer os.Exit(0)
	return &pbsim.Empty{}, nil
}

func main() {
	flag.Parse()

	lis, err := net.Listen("tcp", port)
	if err != nil {
		fmt.Println("failed to listen: %v", err)
	}
	s := grpc.NewServer()
	pbsim.RegisterSimulatorServer(s, &server{})
	// Register reflection service on gRPC server.
	reflection.Register(s)
	if err := s.Serve(lis); err != nil {
		fmt.Println("failed to serve: %v", err)
	}
}
