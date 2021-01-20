from buffer import Buffer
from statisticsRtdma import Statistics
from protocol import Protocol
from numpy.random import choice
import random

# statistic stuff
stat = Statistics()

step = 8
for bs in range(0, 80, step):

    currentSlot = 0
    N = 8  # Number of Nodes /
    W = 4  # Number of channel (Wavelengths) /
    d = 1 / (N - 1)  # transmission probability /
    b = 0  # node load /
    if bs != 0:
        b = 0.1 * bs
    else:
        b = 0.1 * 72
    li = (b / N)  # generation-packets probability /
    # li = b / 36  # generation-packets probability /

    nodes = []  # Nodes

    # generate N nodes with buffer capacity --> 4
    for i in range(N):
        nodes.append(Buffer(4))
        # nodes.append(Buffer(i + 1))


    def probGenerator(bufferIndex, prob):
        # return random.random() <= (bufferIndex + 1) * prob
        return random.random() <= prob


    # returns the index of the destination node
    def dimGeneraor(bufferIndex):
        Ms = list(range(N))
        Ms.pop(bufferIndex)
        mProbs = [1 / (N - 1) for k in Ms]  # probability matrix for every dest
        # mProbs = [m / (((N * (N + 1)) / 2) - (bufferIndex + 1)) for m in Ms]  # probability matrix for every dest
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

    stat.sumsOfDelays = 0
    stat.howManySuccessfulTrans = 0

    # Running the simulation for n slots
    n = 1000000
    while (currentSlot < n):

        print("\n\n Slot : ", currentSlot, "\n")

        # Genarate packets
        index = 0
        for nd in nodes:
            generatePacket(nd, index, currentSlot)
            index += 1

        # packet trans starts in i slot and arrives at i+1
        currentSlot += 1

        trans = schedule.algorithm(A, W, N)

        # print("\n\n", trans, "\n\n")

        # choose which packets is going to transmit / declare final slot of packet / remove packet from system
        for i in range(len(nodes)):
            if trans[i] == -1 or not nodes[i].isBusy():  # because 0 is in use / node i have permission to transmit in
                # channel k (-1 ==> have no permission)
                continue

            indexOfPacket = 0
            for j in nodes[i].packets:  # nodes --> buffer of every node
                if j.nodeDest in B[trans[i]]:  # if the destination of the packet (of node i) is in the set B[k]
                    endOfPacketTransmition(nodes[i], indexOfPacket,
                                           currentSlot)  # the slot that packet leaves the system declared
                    #print("\nPacket from Node ", i, " transmitted to Node",
                    #j.nodeDest, " through channel", trans[i]," delay of packet : ", j.slotFinal - j.slotInit)

                    # stat.packetsTransmitted.append(j)
                    stat.howManySuccessfulTrans += 1
                    stat.sumsOfDelays += j.slotFinal - j.slotInit

                    packetLeavesTheSys(nodes[i], indexOfPacket)
                    trans[i] = -1
                    break  # each node transmit once in a slot
                indexOfPacket += 1

    # Print average Delay of packet transmission
    # averageDelay = averageDelay / TP
    # TP = TP / (n + 1)

    stat.addThroughputAndAvDelay(n)
    stat.b.append(b)
    print("\nLoad  : ", b)
    stat.printResults(n)

stat.plot()
