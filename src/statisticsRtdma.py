import matplotlib.pyplot as plt
from numpy import arange
from pylab import *
from numpy import *


class Statistics:
    x = []
    y = []
    y_to_plot = []


    def __init__(self):
        self.x = []
        self.y = []

    def plot(self):

        self.sort()
        self.regression()
        plot(self.x, self.y, color='red')
        plot(self.x, self.y_to_plot, color='green')
        xlabel("Throughput")
        ylabel("Delay")
        title("rTDMA")
        show()


    def sort(self):
        self.x, self.y = zip(*sorted(zip(self.x, self.y)))


    def regression(self):
        for i in self.x:
            self.y_to_plot.append(self.minimum_sqr3(i))

    def P_update(self, m, a, b):
        temp = []
        for i in range(len(m)):
            temp.append(m[a][i])
        for i in range(len(m)):
            m[a][i] = m[b][i]
        for i in range(len(m)):
            m[b][i] = temp[i]

    def PALU(self, A, b):
        len_m = len(A)
        p_matrix = eye(len_m)
        L = ([])
        U = ([])

        # print(A)

        for k in range(len(A) - 1):
            temp = A[k][k]

            # ελεγχος για οδηγητή
            for i in range(k, len(A)):
                for j in range(k, k + 1):
                    if A[i][k] > temp:
                        temp_index = i
                        temp = A[i][k]

                        self.P_update(p_matrix, k, temp_index)  # update τον πινακα P
                        self.P_update(A, k, temp_index)  # Αντίστοιχη αντιμετάθεση των γραμμών του Α

            # εκτέλεση gauss
            for i in range(k + 1, len(A)):  # αποθήκευση συντελεστών
                for j in range(k, k + 1):
                    A[i][k] = A[i][j] / A[j][j]

            for i in range(k + 1, len(A)):
                for j in range(k + 1, len(A)):
                    A[i][j] = A[i][j] - A[k][j] * A[i][k]

        for i in range(len(A)):
            L.append(([]))
            for j in range(len(A)):
                if j == i:
                    L[i].append(1)
                elif j > i:
                    L[i].append(0)
                else:
                    L[i].append(A[i][j])

        L = array(L)

        for i in range(len(A)):
            U.append(([]))
            for j in range(len(A)):
                if j >= i:
                    U[i].append(A[i][j])
                else:
                    U[i].append(0)

        U = array(U)

        z = dot(p_matrix, b)  # το z δημιουργείται απο τον πολλ/μο p και b

        y = [0.0 for x in range(len(z))]
        y = array(y)

        # L*y = z
        for i in range(len(L)):
            y[i] += z[i]
            for j in range(len(L)):
                if i == j:
                    continue
                else:
                    y[i] -= L[i][j] * y[j]
            y[i] /= L[i][i]

        x = [0.0 for x in range(len(z))]
        x = array(x)

        # U*x=y
        for i in reversed(range(len(L))):
            x[i] += y[i]
            for j in reversed(range(len(L))):
                if i == j:
                    continue
                else:
                    x[i] -= U[i][j] * x[j]
            x[i] /= U[i][i]

        return x

    def minimum_sqr3(self, x):

        # y = a + b*x +cx^2 + dx^3
        n = len(self.x)
        a = []
        b = []
        for i in range(n):
            a.append(1.0)
        for i in range(n):
            b.append(self.x[i])

        # build A
        matrixa = []
        for i in range(n):
            matrixa.append([])
            matrixa[i].append(a[i])
            matrixa[i].append(b[i])
            matrixa[i].append(pow(b[i], 2))

        # build b
        matrixb = []
        for i in range(n):
            matrixb.append(self.y[i])

        matrixa = array(matrixa)
        matrixb = array(matrixb)

        TransAmultiplyA = dot(transpose(matrixa), matrixa)
        TransAmultiplyb = dot(transpose(matrixa), matrixb)

        # TransAmultiplyA * x = TransAmultiplyb
        z = self.PALU(TransAmultiplyA, TransAmultiplyb)

        return z[0] + x * z[1] + pow(x, 2) * z[2]