import matplotlib.pyplot as plt


class Statistics:
    x = []
    y = []

    def __init__(self):
        self.x = []
        self.y = []

    def plot(self):
        plt.plot(self.x, self.y)
        plt.xlabel("Throughput")
        plt.ylabel("Delay")
        plt.title("rTDMA")
        plt.show()
