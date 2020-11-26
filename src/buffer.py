from packet import Packet

class Buffer:
    li = 0 #capacity of buffer
    packets = []

    def __init__(self, l):
        self.li = l

    def isBusy(self):
        return len(packets) > 1

    def isFull(self):
        return len(packets) >= li

    def addPacket(self, si, nd):
        packets.append(Packet(si, nd))

    def removePacket_delivered(self, index):
        packets.remove(index)

    def deliverPacket(self, sf):
        packets.slotFinal = sf
