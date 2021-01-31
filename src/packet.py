class Packet:
    slotInit = 0  # slot in which the packet is generated
    slotFinal = 0  # slot in which packet leaves the system
    nodeDest = 0  # Destination node
    nodeStart = 0  #

    def __init__(self, si, nd, ns):
        self.slotInit = si
        self.nodeDest = nd
        self.nodeStart = ns

    def delayOfTrans(self):
        return int(self.slotFinal - self.slotInit)  # Slot δημιουργείας - slot λήψης
