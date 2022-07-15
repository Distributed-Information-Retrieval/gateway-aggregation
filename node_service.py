import sys
import time
import typer
from layers.network_layer import NetworkLayer


def main():
    if len(sys.argv) != 3 and len(sys.argv) != 5:
        print('Usage: python3 node_service.py <node_name> <req_port>')
        print('Usage: python3 node_service.py <node_name> <req_port> <peer_1> <peer_1_port>')

    node = NetworkLayer(sys.argv[1], sys.argv[2])
    node.start()

    if len(sys.argv) == 5:
        node.join(sys.argv[3], sys.argv[4])

    print("")
    print("##############################################################################")
    print("Command Legend:")
    print("1- join")
    print("2- show connections")
    print("3- show dataset")
    print("4- change dataset")
    print("5- find documents")
    print("##############################################################################")
    print("")
    while True:
        # read input and send command 
        command = input('Enter command: ')

        if command == '1':
            node.join(input('Enter node name: '), input('Enter port: '))  
        elif command == '2':
            print("Connections %s" % node.connected_nodes_names)
        elif command == '3':
            print("Dataset %s" % node.dataset)
        elif command == '4':
            node.change_remote_dataset(input('Enter new dataset: ')) 
        elif command == '5':
            documents = node.find(input('Enter quey: '))
            for document in documents:
                typer.echo(
                    f"Id: {document.id}, "
                    + f"Relevancy: {document.relevancy}, "
                    + f"Title: {document.title}",
                )

if __name__ == '__main__':
    main()