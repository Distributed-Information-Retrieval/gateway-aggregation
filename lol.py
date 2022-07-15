from node import Node
import time

data = ['DC1', 'DC2', 'DC3']

def filterEqual(data, obj):
    return list(filter(lambda x: x != obj, data))

node1 = Node('DC1')
node1.start()
print('node1', node1.connected_nodes_names)
print('Finsis DC1')

time.sleep(1)
node2 = Node('DC2')
node2.start()
node2.join('DC1')
print('node1', node1.connected_nodes_names)
print('node2', node2.connected_nodes_names)
print('Finsis DC2')
time.sleep(1)
node3 = Node('DC3')
node3.start()
node3.join('DC2')
print('Finsis DC3')

print('node1', node1.connected_nodes_names)
print('node2', node2.connected_nodes_names)
print('node3', node3.connected_nodes_names)