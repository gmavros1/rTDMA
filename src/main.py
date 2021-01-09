from buffer import Buffer
from statisticsRtdma import Statistics
from numpy.random import choice
import random

# import sys

N = 8  # Number of Nodes /
W = 4  # Number of channel (Wavelengths) /
d = 1 / (N - 1)  # transmission probability /
b = 1  # sum of packet-generation probabilities /
li = b / N  # generation-packets probability /

# statistic stuff
stat = Statistics()
averageDelay = 0
TP = 0

nodes = []  # Nodes

# generate N nodes with buffer capacity --> i+1
for i in range(N):
    nodes.append(Buffer(i + 1))
    # nodes.append(Buffer(4))


def probGenerator(bufferIndex, prob):
    return random.random() <= (bufferIndex + 1) * prob


# returns the index of the destination node
def dimGeneraor(bufferIndex):
    Ms = list(range(N))
    Ms.pop(bufferIndex)
    # mProbs = [k * (1 / ((N * (N + 1)) / (bufferIndex + 1))) for k in Ms] # probability matrix for every dest
    mProbs = [1/(N-1) for k in Ms]  # probability matrix for every dest
    destination = choice(Ms, 1, mProbs)
    return destination[0]


# Packet generation /  define destination / define in which slot is generated / define the destination
def generatePacket(Node, bufferIndex, whichSlot):
    if not Node.isFull():
        if probGenerator(bufferIndex, li):
            destinationNode = dimGeneraor(
                bufferIndex)  # transmit to all nodes with same probability except the same node, where the
            # probability is 0
            Node.addPacket(whichSlot, destinationNode)


# Finale slot of packet declared
# Index P --> index of packet
def endOfPacketTransmition(Node, indexP, whichSlot):
    Node.deliverPacket(whichSlot, indexP)


# Packet leaves the buffer and the system
def packetLeavesTheSys(Node, indexP):
    Node.removePacket(indexP)


# *** *** The rTDMA Protocol *** ***#

# which node can transmit according to channel
A = []  # A[i] = {1,2,3,4} --> nodes  1,2,3,4 can transmit to channel i
for i in range(W):
    A.append([])
    for j in range(N):
        A[i].append(j)

# which node can receive according to channel
B = []  # B[i] = {1,2} --> nodes  1,2 can receive from channel i
nds = 0  # nodes in each set
for i in range(W):
    B.append([])
    amountOfNodeInEachSet = int(N / W)
    for j in range(amountOfNodeInEachSet):
        B[i].append(nds)
        nds = nds + 1

# Running the simulation for n slots
# n = int(sys.argv[1])
n = 1000000
for slot in range(n):

    # print("\n\n Slot : ", slot, "\n\n")


    # Genarate packets
    index = 0
    for nd in nodes:
        generatePacket(nd, index, slot)
        index += 1

    # debug
    print("\n\n")
    for nd in range(len(nodes)):
        print("Node : ", nd, "\n")
        for p in range(len(nodes[nd].packets)):
            print("     Capacity : ", nodes[nd].li)
            print("     Packets : ", len(nodes[nd].packets))
            print("     Destination : ", nodes[nd].packets[p].nodeDest)

    # trans[i] = k
    trans = []
    for i in range(N):
        trans.append(-1)  # Initialize trans[i] = -1

    # Trans[k] collision free algorithm -------------------------------------------

    # 1. Set of Channels and A set

    # Ak = A.copy() # We want A set to remain unchanged in the beggining of every slot
    Ak = []
    count = 0
    for aa in A:
        Ak.append([])
        for aaaa in aa:
            Ak[count].append(aaaa)
        count += 1

    # Ω set
    channels = []
    for i in range(W):
        channels.append(i)  # [ channel0, channel1, ..., channeN-1 ]

    while len(channels) != 0:
        # 2. select a random chanel k and remove k from set channels
        k = channels.pop(random.randint(0, len(channels) - 1))

        # 3. select a random node from set A[k]
        i = Ak[k].pop(random.randint(0, len(Ak[k]) - 1))

        # 4. Set trans[i] = k and remove i node from Ak sets
        trans[i] = k
        for r in Ak:
            if i in r:
                r.remove(i)

    # print("\n\n", trans, "\n\n")

    # choose which packets is going to transmit / declare final slot of packet / remove packet from system
    for i in range(len(nodes)):
        if trans[i] == -1:  # because 0 is in use / node i have permission to transmit in channel k (-1 ==> have no
            # permission)
            continue
        else:
            indexOfPacket = 0
            for j in nodes[i].packets:  # nodes --> buffer of every node
                if j.nodeDest in B[trans[i]]:  # if the destination of the packet (of node i) is in the set B[k]
                    endOfPacketTransmition(nodes[i], indexOfPacket,
                                           slot)  # the slot that packet leaves the system declared
                    # print("Packet transmited")
                    # print("Diff : ", j.slotFinal - j.slotInit)
                    averageDelay += j.slotFinal - j.slotInit  # Delay
                    packetLeavesTheSys(nodes[i], indexOfPacket)
                    TP += 1  # packets transmited
                indexOfPacket += 1

    # plot

    if slot%2 == 0:
        stat.x.append(TP / (slot + 1))  # Avarage number of transmited packets per slot
        stat.y.append(averageDelay / (slot + 1))

# Print average Delay of packet transmition
averageDelay = averageDelay / (n + 1)
TP = TP / (n + 1)
print("Average Delay : ", averageDelay, "slots")
print("TP : ", TP)
print("slots : ", n)

stat.plot()
