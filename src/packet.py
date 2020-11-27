class Packet:
   slotInit = 0
   slotFinal = 0
   nodeDest = 0

   def __init__(self, si,  nd):
       self.slotInit = si
       self.nodeDest = nd

