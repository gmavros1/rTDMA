from packet import Packet


class Buffer:
    li = 0  # capacity of buffer
    packets = []  # list of packets in buffer

    def __init__(self, l):
        self.li = l
        self.packets = []

    def isBusy(self):
        return len(self.packets) > 1

    def isFull(self):
        if len(self.packets) >= self.li:
            return True

    # add generated packet in Buffer
    def addPacket(self, si, nd):
        self.packets.append(Packet(si, nd))

    # packet leaves the system
    def removePacket(self, index):
        self.packets.pop(index)

    def deliverPacket(self, sf, index):
        self.packets[index].slotFinal = sf
