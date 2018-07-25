package consensus

import (
	"context"
	"flag"
	"fmt"
	"net"
	"os"
	"runtime/pprof"

	"google.golang.org/grpc"
	"google.golang.org/grpc/reflection"

	pb "github.com/tendermint/tendermint/simulator/proto/simulator"
	"io/ioutil"
	"github.com/tendermint/tendermint/abci/example/kvstore"
	"github.com/tendermint/tendermint/types"
	"github.com/tendermint/tendermint/node"
	cfg "github.com/tendermint/tendermint/config"
	"github.com/tendermint/tendermint/libs/log"
)

const (
	port         = ":50051"
	dummyMsgType = 1999
)

// server is used to implement message.SimulatorServer.
type (
	server struct {
		nodes []*ConsensusState // slice of Consensus objects
	}
)

var cpuprofile = flag.String("cpuprofile", "", "write cpu profile to file")

var cfgSim = cfg.DefaultConfig()

// Ping implements simulator.SimulatorServer
func (s *server) Init(in *pb.InitRequest, stream pb.Simulator_InitServer) error {
	nPlayers := in.NBF + in.NFS + in.NHonest

	css := make([]*ConsensusState, nPlayers)
	logger := log.NewTMLogger(log.NewSyncWriter(os.Stdout))
	for i := 0; i < int(nPlayers); i++ {
		n, err := node.DefaultNewNode(cfgSim, logger)
		if err != nil {
			fmt.Println("Error creating node")
		}
		css[i] = n.ConsensusState()
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
	defer pprof.StopCPUProfile()
	return &pb.Empty{}, nil
}

func main() {
	flag.Parse()

	if *cpuprofile != "" {
		f, err := os.Create(*cpuprofile)
		if err != nil {
			log.Fatal(err)
		}
		err = pprof.StartCPUProfile(f)
		if err != nil {
			log.Fatal(err)
		}
	}

	lis, err := net.Listen("tcp", port)
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	s := grpc.NewServer()
	pb.RegisterSimulatorServer(s, &server{})
	// Register reflection service on gRPC server.
	reflection.Register(s)
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
}
