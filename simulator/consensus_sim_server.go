package main

import (
	"context"
	"flag"
	"fmt"
	"net"
	"os"
	"google.golang.org/grpc"
	"google.golang.org/grpc/reflection"

	pb "github.com/tendermint/tendermint/simulator/proto/simulator"
	"github.com/tendermint/tendermint/consensus"
	"github.com/tendermint/tendermint/config"
	"github.com/tendermint/tendermint/types"
	"github.com/tendermint/tendermint/privval"
	sm "github.com/tendermint/tendermint/state"
	dbm "github.com/tendermint/tendermint/libs/db"
	"github.com/tendermint/tendermint/abci/example/kvstore"
	bc "github.com/tendermint/tendermint/blockchain"
	"github.com/tendermint/tendermint/abci/client"
	"sync"
	mempl "github.com/tendermint/tendermint/mempool"
	"github.com/tendermint/tendermint/evidence"
	"github.com/tendermint/tendermint/libs/log"
	"os/exec"
	"bytes"
	"strconv"
)

const (
	port         = ":50051"
	dummyMsgType = 1999
)

// server is used to implement message.SimulatorServer.
type (
	server struct {
		nodes []*consensus.ConsensusReactor
	}
)

// Ping implements simulator.SimulatorServer
func (s *server) Init(in *pb.InitRequest, stream pb.Simulator_InitServer) error {
	nPlayers := int(in.NBF) + int(in.NFS) + int(in.NHonest)
	//nConnections := in.NConnections

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

	for i := 0; i < int(nPlayers); i++ {
		cfgSim := config.DefaultConfig()
		cfgSim.SetRoot(fmt.Sprintf("/Users/vedaad/go/src/github.com/tendermint/tendermint/simulator/mytestnet/node%d/config", i))

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

		eventBus := types.NewEventBus()
		eventBus.Start()
		cs.SetEventBus(eventBus)

		cr := consensus.NewConsensusReactor(cs, false)

		s.nodes[i] = cr
	}

	return nil
}

// Ping implements simulator.SimulatorServer
func (s *server) Ping(in *pb.Request, stream pb.Simulator_PingServer) error {
	fmt.Println()


	fmt.Println("closed message stream")
	return nil
}

func (s *server) Exit(context context.Context, in *pb.Empty) (*pb.Empty, error) {
	defer os.Exit(0)
	return &pb.Empty{}, nil
}

func main() {
	flag.Parse()

	lis, err := net.Listen("tcp", port)
	if err != nil {
		fmt.Println("failed to listen: %v", err)
	}
	s := grpc.NewServer()
	pb.RegisterSimulatorServer(s, &server{})
	// Register reflection service on gRPC server.
	reflection.Register(s)
	if err := s.Serve(lis); err != nil {
		fmt.Println("failed to serve: %v", err)
	}
}
