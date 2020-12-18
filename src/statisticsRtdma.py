import matplotlib.pyplot as plt


class Statistics:
    x = []
    y = []

    def __init__(self):
        self.x = []
        self.y = []

    def plot(self):

        self.sort()
        plt.plot(self.x, self.y)
        plt.xlabel("Throughput")
        plt.ylabel("Delay")
        plt.title("rTDMA")
        plt.show()


    def sort(self):
        self.x, self.y = zip(*sorted(zip(self.x, self.y)))

