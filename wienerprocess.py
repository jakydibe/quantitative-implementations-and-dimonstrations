import numpy.random as npr
import numpy as np
import matplotlib.pyplot as plt

def wiener_process(dt=0.1,x0=0,n=1000):
    #W(t=0) = 0
    #initialize W(t) con zero
    W=np.zeros(n+1)

    #creiamo N=1 timestamp t=0,1,2..........N

    t=np.linspace(x0,n,n+1)

    #dobbiamo usare la somma cumulativa ad ogni step
    #pescare da una distr. normale con media 0 e varianza dt... N(0,dt)
    #N(0,dt) = sqrt(dt) * N(0,1), di solito si usa questa formula

    W[1:n+1] = np.cumsum(np.random.normal(0,np.sqrt(dt),n))

    return t,W

def plot_process(t, W):
    plt.plot(t,W)
    plt.xlabel('Time(t)')
    plt.ylabel('wiener-process W(t)')
    plt.title('Wiener-process')
    plt.show()


if __name__ == '__main__':
    time,data=wiener_process()
    plot_process(time,data)