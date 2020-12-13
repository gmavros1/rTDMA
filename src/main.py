from buffer import Buffer
from statisticsRtdma import Statistics
import random

N = 8  # Number of Nodes /
W = 4  # Number of channel (Wavelengths) /
d = 1 / (N - 1)  # transmition probability /
b = 1  # sum of packet-generation probabilities /
l = b / N  # generation-packets probability /

# statistic stuff
stat = Statistics()
averageDelay = 0
TP = 0

nodes = []  # Nodes

# generate N nodes with buffer capacity --> i+1
for i in range(N):
    nodes.append(Buffer(i + 1))
    #nodes.append(Buffer(4))


def probsGenerator(bufferIndex):
    pass


# Packet generation /  define destination / define in which slot is generated / define the destination
def generatePacket(Node, index, slot):
    if not Node.isFull():  # check if buffer is full
        decision = random.uniform(0, b)  # to be or not to be generated
        if decision >= index * l and decision <= (index + 1) * l:  # generate with probability l
            decision = random.randint(0, N - 2)  # to choose destination
            destinationNode = decision if decision != index else decision + 1  # transmit to all nodes with same probability except the same node, where the probability is 0
            Node.addPacket(slot, destinationNode)
            # print("packet generated. From : ", index, "To : ", destinationNode)


# Finale slot of packet declared
# Index P --> index of packet
def endOfPacketTransmition(Node, indexP, slot):
    Node.deliverPacket(slot, indexP)


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

# which nodecan receive according to channel
B = []  # B[i] = {1,2} --> nodes  1,2 can receive from channel i
nds = 0  # nodes in each set
for i in range(W):
    B.append([])
    amountOfNodeInEachSet = int(N / W)
    for j in range(amountOfNodeInEachSet):
        B[i].append(nds)
        nds = nds + 1

# Running the simulation for n slots
n = 25
for slot in range(n):

    # print("\n\n Slot : ", slot, "\n\n")

    # Ak = A.copy() # We want A set to remain unchanged in the beggining of every slot
    Ak = []
    count = 0
    for aa in A:
        Ak.append([])
        for aaaa in aa:
            Ak[count].append(aaaa)
        count += 1

    # Genarate packets
    index = 0
    for nd in nodes:
        generatePacket(nd, index, slot)
        index += 1

    #### debug ###
    #
    # for nd in range(len(nodes)):
    #    print("Node : ", nd, "\n")
    #    for p in range(len(nodes[nd].packets)):
    #        print("     Capacity : ", nodes[nd].li)
    #        print("     Packets : ", len(nodes[nd].packets))
    #        print("     Destination : ", nodes[nd].packets[p].nodeDest)

    ### debug ###

    # trans[i] = k
    trans = []
    for i in range(N):
        trans.append(-1)  # Initialize trans[i] = -1

    # Trans[k] colision free algorithm

    # 1. Set of Channels
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

    # choose which packets is going to transmit / declare final slot of packet / remove paclet from system
    for i in range(len(nodes)):
        if trans[i] == -1:  # because 0 is in use / node i have permission to transmit in channel k (-1 ==> have no
            # permission)
            continue
        else:
            indexOfPacket = 0
            for j in nodes[i].packets:  # nodes --> buffer of every node
                if j.nodeDest in B[trans[i]]:  # if the destination of the packet is in the set B[k]
                    endOfPacketTransmition(nodes[i], indexOfPacket,
                                           slot)  # the slot that packet leaves the system declared
                    # print("Packet transmited")
                    # print("Diff : ", j.slotFinal - j.slotInit)
                    averageDelay += j.slotFinal - j.slotInit  # Delay
                    packetLeavesTheSys(nodes[i], indexOfPacket)
                    TP += 1  # packets transmited
                indexOfPacket += 1

    # plot
    stat.x.append(TP / (n + 1))
    stat.y.append(averageDelay / (n + 1))

# Print average Delay of packet transmition
averageDelay = averageDelay / (n + 1)
TP = TP / (n + 1)
print("Average Delay : ", averageDelay, "slots")
print("TP : ", TP)

stat.plot()