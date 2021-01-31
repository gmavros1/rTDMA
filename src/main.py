from buffer import Buffer
from statisticsRtdma import Statistics
from protocol import Protocol
import random


# γυρίζει true ή false ανάλογα με το αν θα δημιουργηθεί πακέτο, σύμφωνα με την πιθανότητα li (δηλώνεται παρακάτω)
def probGenerator(bufferIndex, prob):
    # return random.random() <= (bufferIndex + 1) * prob
    return random.random() <= prob


# Γυρίζει το index του node-προορισμού του δημιουργημένου πακέτου.
# Γίνεται τυχαία επιλογή από τα στοιχεία του vector Ms(index όλων των nodes) αφού γινει pop το bufferIndex, δηλαδή
# ο κόμβος που πρόκειται να μεταδώσει
# returns the index of the destination node
def dimGenerator(bufferIndex):
    Ms = list(range(N))
    Ms.pop(bufferIndex)
    # mProbs = [1 / (N - 1) for k in Ms]  # probability vector (for every dest)
    # mProbs = [m / (((N * (N + 1)) / 2) - (bufferIndex + 1)) for m in Ms]  # probability matrix for every dest
    # destination = choice(Ms, 1, mProbs)
    # return destination[0]
    return random.choice(Ms)


# Αφού αποφασιστεί αν πρόκειται να δημιουργηθεί πακέτο (κλήση της probGenerator) και ποιός θα είναι ο προορισμός του
# (κλήση της dimGenerator), καλείται η addPacket για να προστεθεί το πακέτο στον buffer του κόμβου με index
# bufferIndex (και στον οποίο αντιστοιχεί το αντικείμενο Node που έρχεται σαν όρισμα) πάντα πληρώντας την προυπόθεση
# πως ο buffer δεν είναι full --> Node.isFull() (Node.isFull() και addPacket() είναι μέθοδοι της κλάσης Buffer)
# Packet generation /  define destination / define in which slot is generated / define the destination
def generatePacket(Node, bufferIndex, whichSlot):
    if probGenerator(bufferIndex, li):
        destinationNode = dimGenerator(
            bufferIndex)  # transmit to all nodes with same probability except the same node, where the
        # probability is 0
        if not Node.isFull():
            Node.addPacket(whichSlot, destinationNode, bufferIndex)  # To ορισμά whichSlot αντιστοιχεί το slot που
            # γίνεται η δημιουργεία
            # print("Node ", bufferIndex, "Created Packet. || Destination : ", destinationNode)


# Καταχωρείται στο πακέτο η τιμή του slot που έγινε η άφιξη
# με την μέθοδο deliverPacket της κλάσης Buffer
# Finale slot of packet declared
# Index P --> index of packet
def endOfPacketTransmition(Node, indexP, whichSlot):
    Node.deliverPacket(whichSlot, indexP)


# Διαγράφεται το πακέτο που μεταδόθηκε απο τον buffer του κόμβου που έκανε μετάδοση
# Packet leaves the buffer and the system
def packetLeavesTheSys(Node, indexP):
    Node.removePacket(indexP)


# statistic stuff
stat = Statistics()  # αντικείμενο της κλάσεις Statistics, υπολογίζει το Throughput και το delay
currentSlot = 0  # μεταβλητή που αυξάνεται σε κάθε slot

# run some simulations with different system load
n = 100000  # αριθμός slot που θα τρέξει κα θα δοκιμαστεί το rtdma για κάθε μια προσομοίωση
step = 8
for bs in range(0, 72, step):  # μέσα σε αυτήν την επανάλυψη θα τρέξουν οι προσομοιώσεις οι οποίο θα έχουν system
    # load b που θα καθορίζεται απο την μεταβλητή bs (bs == 0, 8, 16, 24, 32, ..., 64)

    currentSlot = 0
    N = 8  # Number of Nodes /
    W = 4  # Number of channel (Wavelengths) /
    d = 1 / (N - 1)  # transmission probability /
    b = 0  # system load /
    if bs != 0:
        b = 0.1 * bs
    else:
        b = 0.1  # System load (στην πρώτη προσομοίωση βάζουμε load 0.1)
    li = b / N  # generation-packets probability /
    # li = b / 36  # generation-packets probability /

    nodes = []  # Nodes   Vector που κρατάει αντικείμενα της κλάσης Buffer. Κάθε θέση του vector, το buffer του
    # αντίστοιχου node

    # generate N nodes with buffer capacity --> 4
    for i in range(N):
        nodes.append(Buffer(4))
        # nodes.append(Buffer(i + 1))

    # *** *** The rTDMA Protocol *** ***#

    # Σύμφωνα με το σύστημα 3 καθε κόμβος μπορεί να μεταδώσει σε μέσω όλων των καναλιών
    # Αρα στον δισδιάστατο πίνακα έχουμε το index όλων των κόμβων για κάθε κανάλι
    # which node can transmit according to channel
    A = []  # A[k] = {1,2,3,4} --> nodes  1,2,3,4 can transmit through channel k
    for i in range(W):
        A.append([])
        for j in range(N):
            A[i].append(j)

    # Κάθε κόμβος μπορεί να λάβει πακέτο μόνο από ένα κανάλι
    # άρα μέσω του καναλιού με index 0 μπορούμε να μεταδώσουμε στους κόμβους με index 0 και 1 κλπ...
    # which node can receive according to channel
    B = []  # B[i] = {1,2} --> nodes  1,2 can receive from channel i
    nds = 0  # nodes in each set
    for i in range(W):
        B.append([])
        amountOfNodeInEachSet = int(N / W)
        for j in range(amountOfNodeInEachSet):
            B[i].append(nds)
            nds = nds + 1

    # το schedule γίνεται αντικείμενο της κλάσεις Protocol στην οποία υπολογίζεται το
    # transmission schedule για κάθε slot
    schedule = Protocol(N)

    # Σε κάθε slot κρατούνται τα άθροισμα των επιτυχών μεταδόσεων και το άθροισμα των καθηστερήσεών τους
    stat.sumsOfDelays = 0
    stat.howManySuccessfulTrans = 0

    # print("\n\nSlot ", 0, "\n")
    # Running the simulation for n slots
    # loop που τρέχει για n slots
    while currentSlot <= n:

        # παραγωγή πακέτων για κάθε κόμβο στην αρχή κάθε slot
        # Genarate packets
        index = 0
        for nd in nodes:
            generatePacket(nd, index, currentSlot)
            index += 1

        # στο vector trans αποθηκεύεται το transmission schedule σε κάθε slot
        # πχ trans = [-1, 0, -1, 3, 2, -1, 1, -1]
        # Με αυτό το trans στο συγκεκριμένο slot επιτρεπεται να μεταδώσουν οι κόμβοι με index
        # 1,3,4,6 μέσω των καναλιων 0,3,2,1 αντίστοιχα
        trans = schedule.algorithm(A, W, N)
        # print("\n\tTRANS : ", trans, "\n")

        # print("\n\n", trans, "\n\n")

        # DEBUG
        # nNodes = 0
        # for buffs in nodes:
        #   print("\n\tNode ", nNodes)
        #    nPackets = 0
        #    for pcs in buffs.packets:
        #        if buffs.isBusy():
        #            print("\t\tFrom : ", pcs.nodeStart, "|| Destination : ", pcs.nodeDest, "|| Initial slot : ",
        #                  pcs.slotInit)
        #        else:
        #            print("\t\tEMPTY!!!")
        #        nPackets += 1
        #    nNodes += 1

        # packet trans starts in i slot and arrives at i+1
        # Αύξάνεται το currentSlot αφού η μετάδωση διαρκεί 1 slot
        currentSlot += 1
        # print("\n\n Slot : ", currentSlot)

        # Επιλογή των πακέτων που θα μεταδοθούν
        # choose which packets is going to be transmitted / declare final slot of packet / remove packet from system
        # κεντρικό loop --> έλεγχος για κάθε κόμβο
        for i in range(len(nodes)):
            # Έλεγχος για το αν ο κόμβος με index i επιτρέπεται να μεταδώσει σύμφωνα με το trans, και αν επιτρέπεται
            # θα πρέπει να έχει κάποιο πακέτο στον buffer
            if not trans[i] == -1 and nodes[i].isBusy():  # because 0 is in use / node i have permission to transmit
                # through
                # channel k (-1 ==> have no permission)
                indexOfPacket = 0
                # εξετάζονται ένα ένα τα πακέτα του κόμβου. Αν βρεθεί πακέτο το οποίο έχει προορισμό-κόμβο που
                # λαμβάνει απο το κανάλι που μεταδίδει ο εν λόγω κόμβος (δηλαδη εάν ο κόμβος-προορισμός βρίσκεται
                # μέσα στο Β[κ], όπου κ το κανάλι μετάδοσης), τότε γίνεται μετάδοση
                for j in nodes[i].packets:  # nodes --> buffer of every node
                    if j.nodeDest in B[trans[i]]:  # if the destination of the packet (of node i) is in the set B[k]
                        endOfPacketTransmition(nodes[i], indexOfPacket,
                                               currentSlot)  # the slot that packet leaves the system declared
                        # print("\nPacket from Node ", i, " transmitted to Node",
                        #     j.nodeDest, " through channel", trans[i], " delay of packet : ", j.delayOfTrans(), "\n")

                        stat.howManySuccessfulTrans += 1  # +1 επιτυχημένη μετάδωση
                        stat.sumsOfDelays += j.delayOfTrans()  # προσθήκη delay στο άθροισμα

                        packetLeavesTheSys(nodes[i], indexOfPacket)  # διαγραφή πακέτου απο το buffer του κόμβου
                        break  # each node transmit once in a slot
                    indexOfPacket += 1

    # για κάθε μία προσομοίωση υπολογίζεται το μέσο throughput και το average delay
    stat.addThroughputAndAvDelay(currentSlot)
    stat.b.append(b)
    print("\nLoad  : ", b, "\n")

# Προβολη αποτελεσμάτων και γραφικής παράστασης
stat.printResults(currentSlot)
stat.plot()
