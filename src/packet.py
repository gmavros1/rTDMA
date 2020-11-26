class Packet:
   slotInit = 0
   slotFInal = 0
   nodeDest = 0

   def __init__(self, si, sf, nd):
       self.slotInit = si
       self.slotFinal = sf
       self.nodeDest = nd

