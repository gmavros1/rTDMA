from packet import Packet


class Buffer:
    li = 0  # capacity of buffer
    packets = []  # list of packets in buffer

    def __init__(self, l):
        self.li = l
        self.packets = []

    def isBusy(self):
        return len(self.packets) >= 1  # Αν ο buffer έχει τουλάχιστον 1 πακέτο

    def isFull(self):
        if len(self.packets) >= self.li:  # αν ο αριθμός πακέτων είναι στο όριο
            return True

    # add generated packet in Buffer
    def addPacket(self, si, nd, ns):
        self.packets.append(Packet(si, nd, ns))  # δημιουργεία πακέτου και ορισμός slot δημιουργείας, παραλήπτη και
        # αποστολέα

    # packet leaves the system
    def removePacket(self, index):
        self.packets.pop(index)  # Διαγραφή πακετου απο buffer (από λίστα packets)

    def deliverPacket(self, sf, index):
        self.packets[index].slotFinal = sf  # ορισμός slot λήψης πακέτου
