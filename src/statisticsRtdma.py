import matplotlib.pyplot as plt
from numpy import arange
from pandas import read_csv
from scipy.optimize import curve_fit


class Statistics:
    x = []
    y = []
    x_to_plot = []
    y_to_plot = []


    def __init__(self):
        self.x = []
        self.y = []

    def plot(self):

        self.sort()
        self.regression()
        plt.plot(self.x, self.y, color='red')
        #plt.plot(self.x_to_plot, self.y_to_plot, color='green')
        plt.xlabel("Throughput")
        plt.ylabel("Delay")
        plt.title("rTDMA")
        plt.show()


    def sort(self):
        self.x, self.y = zip(*sorted(zip(self.x, self.y)))


    def regression(self):
        popt, _ = curve_fit(self.objective, self.x, self.y)

        # summarize the parameter values
        a, b, c = popt

        self.x_to_plot = arange(min(self.x), max(self.x), 1)
        self.y_to_plot = self.objective(self.x_to_plot, a, b, c)

    def objective(self, x, a, b, c):
        return a * x + b * x ** 2 + c