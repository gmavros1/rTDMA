from packet import Packet

class Buffer:
    li = 0 #capacity of buffer
    packets = []

    def __init__(self, l):
        self.li = l

    def isBusy(self):
        return len(self.packets) > 1

    def isFull(self):
        return len(self.packets) >= self.li

    def addPacket(self, si, nd):
        self.packets.append(Packet(si, nd))

    def removePacket(self, index):
        self.packets.pop(index)

    def deliverPacket(self, sf, index):
        self.packets[index].slotFinal = sf
