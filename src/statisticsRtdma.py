from pylab import *
from numpy import *
from tabulate import tabulate


class Statistics:
    x = []
    y = []
    b = []
    sumsOfDelays = 0
    howManySuccessfulTrans = 0

    def __init__(self):
        self.x = []
        self.y = []
        self.b = []

    def printResults(self, n):
        # print(tabulate({"Throughput": self.x, "Delay": self.y}))
        print("Average Delay : ", self.sumsOfDelays/self.howManySuccessfulTrans, "slots")
        print("TP : ", self.howManySuccessfulTrans/n)
        print("slots : ", n)



    def addThroughputAndAvDelay(self,n):
        self.x.append(self.howManySuccessfulTrans/n)
        self.y.append(self.sumsOfDelays/self.howManySuccessfulTrans)




    def plot(self):
        self.sort()
        plot(self.x, self.y, color='red')
        xlabel("Throughput")
        ylabel("Delay")
        title("rTDMA")
        ylim(7, 15)
        xlim(0, 4)
        show()
        with open('/home/gmavros/Desktop/Sxolhtemp/communication networks/project/rTDMA/src/test.txt', 'w') as r:
            for n in range(len(self.x)):
                r.write('{} {} {}\n'.format(self.x[n], self.y[n], self.b[n]))
        r.close()

    def sort(self):
        self.x, self.y = zip(*sorted(zip(self.x, self.y)))

        # self.x.sort()
        # self.y.sort()
