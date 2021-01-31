import random


class Protocol:
    trans = []

    def __init__(self, N):
        self.trans = []
        # trans[i] = k
        for i in range(N):
            self.trans.append(-1)  # Initialize trans[i] = -1

    def algorithm(self, A, W, N):

        # Trans[k] collision free algorithm -------------------------------------------
        for t in range(N):
            self.trans[t] = -1

        # 1. Set of Channels and A set

        # Ένα αντίγραφο που πίνακα Α της main
        # Ak = A.copy() # We want A set to remain unchanged in the beginning of every slot
        Ak = []
        count = 0
        for aa in A:
            Ak.append([])
            for aaaa in aa:
                Ak[count].append(aaaa)
            count += 1

        # Σύνολο καναλιών : [0, 1, 2, 3] στο παραδειγμά μας
        # Ω set
        channels = []
        for i in range(W):
            channels.append(i)  # [ channel0, channel1, ..., channeN-1 ]

        # Υλοποίηση αλγορίθμου
        while len(channels) != 0:
            # 2. select a random chanel k and remove k from set channels
            k = channels.pop(random.randint(0, len(channels) - 1))

            # 3. select a random node from set A[k]
            i = Ak[k].pop(random.randint(0, len(Ak[k]) - 1))

            # 4. Set trans[i] = k and remove i node from Ak sets
            self.trans[i] = k
            for r in Ak:
                if i in r:
                    r.remove(i)

        return self.trans  # επιστρέφει το trans, στις θέσεις των κόμβων που δεν μεταδίδουν υπάρχει η τιμή 1
