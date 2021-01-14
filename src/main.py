from buffer import Buffer
from statisticsRtdma import Statistics
from protocol import Protocol
from numpy.random import choice
import random

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
    nodes.append(Buffer(4))


def probGenerator(bufferIndex, prob):
    # return random.random() <= (bufferIndex + 1) * prob
    return random.random() <= prob


# returns the index of the destination node
def dimGeneraor(bufferIndex):
    Ms = list(range(N))
    Ms.pop(bufferIndex)
    mProbs = [1 / (N - 1) for k in Ms]  # probability matrix for every dest
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
            # print("Node ", bufferIndex, "Created Packet. | Destination : ", destinationNode)


# Finale slot of packet declared
# Index P --> index of packet
def endOfPacketTransmition(Node, indexP, whichSlot):
    Node.deliverPacket(whichSlot, indexP)


# Packet leaves the buffer and the system
def packetLeavesTheSys(Node, indexP):
    Node.removePacket(indexP)


def showStatus():
    print("\t\tPacket  |  dest")


# *** *** The rTDMA Protocol *** ***#

# which node can transmit according to channel
A = []  # A[k] = {1,2,3,4} --> nodes  1,2,3,4 can transmit through channel k
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

# transmission schedule
schedule = Protocol(N)

# Running the simulation for n slots
n = 1000000
for slot in range(n):

    # print("\n\n Slot : ", slot, "\n")

    # Genarate packets
    index = 0
    for nd in nodes:
        generatePacket(nd, index, slot)
        index += 1

    # the transmission starts in i slot and arrives at i+1
    arrivalSlot = slot + 1

    trans = schedule.algorithm(A, W, N)

    # print("\n\n", trans, "\n\n")

    # choose which packets is going to transmit / declare final slot of packet / remove packet from system
    for i in range(len(nodes)):
        if trans[i] == -1 or not nodes[i].isBusy():  # because 0 is in use / node i have permission to transmit in
            # channel k (-1 ==> have no permission)
            continue
        else:
            indexOfPacket = 0
            for j in nodes[i].packets:  # nodes --> buffer of every node
                if j.nodeDest in B[trans[i]]:  # if the destination of the packet (of node i) is in the set B[k]
                    endOfPacketTransmition(nodes[i], indexOfPacket,
                                           arrivalSlot)  # the slot that packet leaves the system declared
                    # print("\nPacket from Node ", i, " transmitted to Node", j.nodeDest, " through channel", trans[i]," delay of packet : ", j.slotFinal - j.slotInit)
                    # averageDelay += j.slotFinal - j.slotInit  # Delay
                    stat.packetsTransmitted.append(j)
                    packetLeavesTheSys(nodes[i], indexOfPacket)
                    # TP += 1  # packets transmitted
                    break  # each node transmit once in a slot
                indexOfPacket += 1

    stat.addThroughputAndAvDelay(arrivalSlot)

    # plot
    # if arrivalSlot > 1:
    #       try:
    #           stat.x.append(TP / arrivalSlot)  # Average number of transited packets per slot
    #           stat.y.append(averageDelay / TP)
    #           if TP / arrivalSlot == 0:
    #               print(averageDelay / TP)
    #       except ZeroDivisionError:
    #           pass

    # feedback
    # print("\n")

# Print average Delay of packet transmission
# averageDelay = averageDelay / TP
# TP = TP / (n + 1)
# print("Average Delay : ", averageDelay, "slots")
# print("TP : ", TP)
# print("slots : ", n)

stat.plot()
stat.printResults()
# print(stat.x)
# print(stat.y)
