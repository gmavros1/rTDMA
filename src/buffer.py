from packet.py import Packet

class Buffer:
    li = 0 #capacity of buffer
    packets = []

    def __init__(self, l):
        slef.li = l

    def isBusy(self):
        return len(packets) > 1

    def isFull(self):
        return len(packets) >= li

    def addPacket(self, si, sf, nd):
        packets.append(Packet(si, sf, nd))

    def removePacket_delivered(self, index):
        packets.remove(index)

