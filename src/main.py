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
        decision = random.uniform(0, b)
        if decision >= whichNode*l and decision <= (whichNode+1)*l:   # generate with probability l
            decision = random.randint(0, N-2)
            destinationNode = decision if decision != whichNode else decision + 1    # transmit to all nodes with same probability except the same node, where the probability is 0
            node[whichNode].addPacket(slot, destinationNode)

def endOfPacketTransmition(whichNode, indexP):
    nodes[whichNode].deliverPacket(slot, indexP)

def packetLeavesTheSys(whichNode, indexP):
    node[whichNode].removePacket(indexP)


slot = 0
