import sys
import time

import zmq
# from fastapi import FastAPI

from helper.decorators import repeat
from helper.entities import Command, CommandType
from helper.process import Process

from retrieve_system.engine import Engine

class NetworkLayer():
    def __init__(self, node_name, rep_port, nodes_connections=[], ip="tcp://localhost:") -> None:
        print("Hello, I am %s" % node_name)
        self.ip = ip
        self.myself = node_name
        self.rep_port = rep_port
        self.connected_nodes_names = nodes_connections
        self.dataset =  'data/cran_data.json'
        # self.connected_nodes_req_ports = [nodes_connections[a] for a in range(len(nodes_connections)) if a%2 == 1]
        self._process = []

        self.context = zmq.Context()
        self.poller = None
        self.engine = Engine()

        # State Back-End
        self.statebe = self.context.socket(zmq.PUB)

        # State Front-End
        self.statefe = self.context.socket(zmq.SUB)
        self.statefe.setsockopt(zmq.SUBSCRIBE, b'')

        self.bind_address = u"ipc://%s-state.ipc" % self.myself
        self.statebe.bind(self.bind_address)

    
    def train(self):
        self.engine.train(self.dataset)

    def find(self, query: str) -> list:
        return self.engine.find(query)

    @repeat()
    def ping_to_others_nodes(self) -> None:
        socks = dict(self.poller.poll(1000))

        # Handle incoming status message
        if socks.get(self.statefe) == zmq.POLLIN:
            obj: Command = self.statefe.recv_pyobj()
            if obj.type == CommandType.PING:
                # print('%s Received: from %s COMMAND PING' %
                #       (self.myself, obj.args['bin_address']))
                # print(self.connected_nodes_names)
                # print(self.dataset)
                pass

            if obj.type == CommandType.UPDATE_CONNECTIONS:
                # print('%s Received: from %s COMMAND UPDATE_CONNECTIONS %s' %
                #       (self.myself, obj.args['bin_address'], obj.args['connected_node_names']))
                connections = obj.args['connected_node_names']
                for conn in connections:
                    if conn != self.myself:
                        self.statefe.connect(u"ipc://%s-state.ipc" % conn)
                        if conn not in self.connected_nodes_names:
                            self.connected_nodes_names.append(conn)

            if obj.type == CommandType.CHANGE_DATASET:
                # print('%s Received: from %s COMMAND CHANGE_DATASET %s' %
                #       (self.myself, obj.args['bin_address'], obj.args['dataset']))
                connections = obj.args['connected_node_names']
                dataset = obj.args['dataset']
                self.change_dataset(dataset)

        else:
            # Send our address and a random value
            # for worker availability
            cmd = Command(CommandType.PING, {'bin_address': self.bind_address})
            self.statebe.send_pyobj(cmd)

    @repeat()
    def update_connections(self):
        cmd = Command(CommandType.UPDATE_CONNECTIONS, {
                      'connected_node_names': self.connected_nodes_names, 
                      'bin_address': self.bind_address})
        self.statebe.send_pyobj(cmd)
        time.sleep(1)

    def change_remote_dataset(self, dataset):
        if dataset != self.dataset and dataset in ["data/cran_data.json", "data/cisi_data.json"]:
            cmd = Command(CommandType.CHANGE_DATASET, {
                    'dataset': dataset, 
                    'bin_address': self.bind_address})
            self.statebe.send_pyobj(cmd)
            self.change_dataset(dataset)

    def change_dataset(self, dataset):
        self.dataset = dataset
        self.train()

    def start(self) -> None:
         # train dataset
        self.train()

        # Start the network layer
        for node_name in self.connected_nodes_names:
            self.statefe.connect(u"ipc://%s-state.ipc" % node_name)
            time.sleep(1.0)

        # for node_port in self.connected_nodes_req_ports:
        #     self.socket_req.connect("%s%s" % (self.ip, node_port))
        #     time.sleep(1.0)

        self.poller = zmq.Poller()
        self.poller.register(self.statefe, zmq.POLLIN)

        self._process.append(Process(self, 'ping_to_others_nodes'))
        self._process.append(Process(self, 'update_connections'))
        self._process.append(Process(self, 'run'))
        for proc in self._process:
            proc.start()

    def _join(self, bin_address):
        "Subscribe for receive message from others nodes"
        if bin_address not in self.connected_nodes_names and bin_address != self.myself:
            self.connected_nodes_names.append(bin_address)
            self.statefe.connect(u"ipc://%s-state.ipc" % bin_address)

    def join(self, node_name, req_port) -> None:
        if node_name not in self.connected_nodes_names and node_name != self.myself:
            self.connected_nodes_names.append(node_name)
            self.statefe.connect(u"ipc://%s-state.ipc" % node_name)

        self.socket_req = self.context.socket(zmq.REQ)

        self.socket_req.connect("%s%s" % (self.ip, req_port))

        cmd = Command(CommandType.JOIN, {'bin_address': self.myself})
        self.socket_req.send_pyobj(cmd)

    def run(self):
        self.socket_rep = self.context.socket(zmq.REP)
        self.socket_rep.bind("tcp://*:%s" % self.rep_port)
        while True:
            print('Waiting Request ...')
            request: Command = self.socket_rep.recv_pyobj()
            result = None

            if request.type == CommandType.JOIN:
                bin_address = request.args['bin_address']
                self._join(bin_address)

            self.socket_rep.send_pyobj(result)
            print("Finish Request")


if __name__ == '__main__':
    print(sys.argv)

    if len(sys.argv) == 3:
        node = NetworkLayer(sys.argv[1], sys.argv[2])
        node.start()

    if len(sys.argv) == 5:
        node = NetworkLayer(sys.argv[1], sys.argv[2])
        node.start()
        node.join(sys.argv[3], sys.argv[4])

    if len(sys.argv) == 4 or len(sys.argv) < 3:
        print("Usage: node.py <myself> <port> or node.py <myself> <port> <peer_1> <peer_1_port>....")
        sys.exit(1)

# app = FastAPI()

# @app.get("/")
# async def root():
#     print(node.nodes_connections)
#     return {"message": "Welcome to gateway service"}

# @app.get("/docs")
# async def doc():
#     print(node.nodes_connections)
#     return {"message": "Welcome to gateway service"}
