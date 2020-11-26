from buffer import Buffer
import random

N = 8       # Number of Nodes /
W = 4       # Number of channel (Wavelengths) / 
d = 1/(N-1) # transmition probability /
b = 0.8     # sum of packet-generation probabilities / 
l = b/N     # generation-packets probability / 

nodes = []  # Nodes
 
# generate N nodes with buffer capacity --> 4
for i in range(N):
    nodes.append(Buffer(i+1)) 

# Packet generation /  define destination / define in which slot is generated / define the destination
def generatePacket(whichNode):
    if not nodes[whichNode].isFull:     # check if buffer is full
        decission = random.uniform(0, b)
        if decission >= whichNode*l and decission <= (whichNode+1)*l:   # generate with probability l
            decission = random.randint(0, N-2)
            destinationNode = decission if decission != whichNode else decission + 1    # transmit to all nodes with same probability except the same node, where the probability is 0
            node[whichNode].addPacket(slot, destinationNode)

slot = 0
