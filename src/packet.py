class Packet:
    slotInit = 0  # slot in which the packet is generated
    slotFinal = 0  # slot in which packet leaves the system
    nodeDest = 0  # Destination node

    def __init__(self, si, nd):
        self.slotInit = si
        self.nodeDest = nd
