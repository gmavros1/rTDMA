from buffer import Buffer
import random

N = 8       # Number of Nodes /
W = 4       # Number of channel (Wavelengths) / 
d = 1/(N-1) # transmition probability /
b = 0.8     # sum of packet-generation probabilities / 
l = b/N     # generation-packets probability / 

nodes = []  # Nodes
 
# generate N nodes with buffer capacity --> i+1
for i in range(N):
    nodes.append(Buffer(i+1)) 

# Packet generation /  define destination / define in which slot is generated / define the destination
def generatePacket(whichNode, slot):
    if not nodes[whichNode].isFull:     # check if buffer is full
        decision = random.uniform(0, b)
        if decision >= whichNode*l and decision <= (whichNode+1)*l:   # generate with probability l
            decision = random.randint(0, N-2)
            destinationNode = decision if decision != whichNode else decision + 1    # transmit to all nodes with same probability except the same node, where the probability is 0
            node[whichNode].addPacket(slot, destinationNode)

# Finale slot of packet declared
def endOfPacketTransmition(whichNode, indexP, slot):
    nodes[whichNode].deliverPacket(slot, indexP)

# Packet leaves the buffer and the system
def packetLeavesTheSys(whichNode, indexP):
    node[whichNode].removePacket(indexP)
            

#*** *** The rTDMA Protocol *** ***#

# which node can transmit according to channel
A = []  # A[i] = {1,2,3,4} --> nodes  1,2,3,4 can transmit to channel i
for i in range(W):
    A.append([])
    for j in range(N):
        A[i].append(j)



# which nodecan receive according to channel
B = []  # B[i] = {1,2} --> nodes  1,2 can receive from channel i
nds = 0 # nodes in each set
for i in range(W):
    B.append([])
    amountOfNodeInEachSet = int(N/4)
    for j in range(amountOfNodeInEachSet):
        B[i].append(nds)
        nds = nds + 1


# Running the simulation for n slots
n = 10
for slot in range (n):

    # Ak = A.copy() # We want the A set unchanged in the beggining of every slot
    Ak = []
    count = 0
    for aa in A:
        Ak.append([])
        for aaaa in aa:
            Ak[count].append(aaaa)
        count += 1


    # Genarate packets
    for nd in range(N):
        generatePacket(nd, slot)

    # trans[i] = k
    trans = []
    for i in range(N):
        trans.append(0) # Initialize trans[i] = 0


    # Trans[k] colision free algorithm

    # 1. Set of Channels
    channels = []
    for i in range(W):
        channels.append(i) # [ channel0, channel1, ..., channeN-1 ]
        

    while len(channels) != 0:
        # 2. select a random chanel k and remove k from set channels 
        k = channels.pop(random.randint(0, len(channels)-1))

        # 3. select a random node from set A[k]
        i = Ak[k].pop(random.randint(0, len(Ak[k])-1))


        # 4. Set trans[i] = k and remove i node from Ak sets
        trans[i] = k
        for r in Ak:
            if i in r:
                r.remove(i)

    # choose which packets is going to transmit
    for i in range(len(trans)):
        pass

