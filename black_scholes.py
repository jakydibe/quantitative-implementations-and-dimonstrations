from scipy import stats
from numpy import log, exp, sqrt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



#in ordine: Stock price, strike price, time-to-expiry, risk-free rate, volatility  
def call_option_price(S, E, T,rf ,sigma):
    #prima dobbiamo calcolarci i parametri d1 e d2
    d1=(log(S/E) + (rf+sigma*sigma/2.0)*T)/(sigma * sqrt(T))
    d2=d1-sigma*sqrt(T)
    print("d1 and d2: %s, %s" % (d1,d2))
    #usiamo la N(x) distribuzione normale standard per calcolare il prezzo dell' opzione
    #uso la pnorm di R in pratica
    return S*stats.norm.cdf(d1)-E*exp(-rf*T)*stats.norm.cdf(d2)


def put_option_price(S, E, T,rf ,sigma):
    #prima dobbiamo calcolarci i parametri d1 e d2
    d1=(log(S/E) + (rf+sigma*sigma/2.0)*T)/(sigma * sqrt(T))
    d2=d1-sigma*sqrt(T)
    print("d1 and d2: %s, %s" % (d1,d2))
    #usiamo la N(x) distribuzione normale standard per calcolare il prezzo dell' opzione
    #uso la pnorm di R in pratica
    return -S*stats.norm.cdf(-d1)+E*exp(-rf*T)*stats.norm.cdf(-d2)


##############################################################----MONTE CARLO SIMULATION----###################################
NUM_OF_SIMULATIONS = 100

def stock_monte_carlo(S0, mu, sigma, N=252):
    result=[]

    #possibili realizzazione di S(t)
    for _ in range(NUM_OF_SIMULATIONS):
        prices=[S0]
        for _ in range(N):
            #simuliamo il campio day by day quindi t = 1
            t = 1
            stock_price = prices[-1] * np.exp((mu-0.5 * sigma ** 2)*t + 
                                              sigma * np.random.normal()) #np.random.normal e' N(0,1)
            prices.append(stock_price)
        result.append(prices)

    simulation_data = pd.DataFrame(result)
    #faccio la matrice trasposta perche' dopo le colonne avranno le time series, ogni colonna sara' una simulazione
    simulation_data = simulation_data.T

    simulation_data['mean'] = simulation_data.mean(axis=1)
    print(simulation_data)
    print("PREDICTION WITH MONTE CARLO SIMULATION : ",simulation_data['mean'].tail(1)) #uso la .tail() peche' 

    plt.plot(simulation_data)
    plt.show()

    ############ MONTE CARLO CON BLACK SCHOLES E LE OPZIONI ##########################

class OptionPricing:
    def __init__(self,S0,E,T,rf,sigma,iterations):
        self.S0=S0
        self.E=E
        self.T = T
        self.rf=rf
        self.sigma=sigma
        self.iterations=iterations

    def call_option_simulation(self):
        #creiamo due colonne, la prima con 0s e la seconda con i payoff
        #la funzione payoff e' max(0,S-E)
        option_data = np.zeros([self.iterations, 2])

        rand = np.random.normal(0,1,[1,self.iterations]) #cro un array di iterations random values estratti da N(0,1)

        #equazione per S(t) oovero la stock price a T
        stock_price = self.S0 * np.exp(self.T*(self.rf - 0.5 * self.sigma ** 2)
                                       + self.sigma * np.sqrt(self.T) * rand)
        
        #calcoliamo S-E per calcolare max(S-E,0)
        option_data[:, 1] = stock_price - self.E

        #average for mc sim
        average = np.sum(np.amax(option_data,axis=1))/float(self.iterations)
        #print(option_data)

        return np.exp(-1.0 * self.rf*self.T)*average


if __name__=='__main__':
    #underlying stock price at t=0
    S0=100
    #strike price
    E=100
    #expiry = 1 anno, 365 giorni
    Td=365
    T=Td/365
    #risk-free rate
    rf=0.05
    sigma=0.2

    print("call option price according to black-scholes: ", call_option_price(S0,E,T,rf,sigma))
    ##simulazione di monte carlo stock price
    stock_monte_carlo(50,0.0005, 0.01)

    #simulazione di monte carlo opzioni
    model = OptionPricing(100,100,1,0.05,0.2,1000)
    sims=model.call_option_simulation()
    print(sims)
    plt.plot(sims)
    plt.show()