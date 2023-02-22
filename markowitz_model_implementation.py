import numpy as np
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import scipy.optimize as optimization


#in media ci sono 252 trading days in un anno...
NUM_TRADING_DAYS=252
#generate random weights of 10000 portfolios
NUM_PORTFOLIOS=10000
#lista di stock che vogliamo analizzare
stocks = ['AAPL','WMT','TSLA','GE','AMZN','DB']

#historical data data inizio e fine
start_date='2012-01-01'
end_date='2017-01-01'

def download_data():
    # name of the stock (key) - stock values (2010-2023) as the values
    stock_data = {}

    for stock in stocks:
        #fetcho le close da yahoo finance
        ticker = yf.Ticker(stock)
        stock_data[stock] = ticker.history(start=start_date, end=end_date)['Close']

    return pd.DataFrame(stock_data)

def show_data(data):
    data.plot(figsize=(10,5))
    plt.show()

def calculate_return(data): #si utilizza il log-daily return per convenienza matematica
    log_return = np.log(data/data.shift(1))  # esmpio  data = 1 2 3 4 5, in pratica shifta l' array e quindi in pratica itera e crea un array 
    print(log_return)                                   #       1 2 3 4 5
    return log_return[1:] #non ritorno la prima riga perche' e' un NaN

def show_statistics(returns):
    print(returns.mean()*NUM_TRADING_DAYS)
    print(returns.cov() * NUM_TRADING_DAYS)

def show_mean_variance(returns,weights):
    portfolio_return = np.sum(returns.mean()*weights) * NUM_TRADING_DAYS #annual portfolio return
    portfolio_volatility = np.sqrt(np.dot(weights.T,np.dot(returns.cov()*NUM_TRADING_DAYS,weights)))  #  weights.T e' la trasposta di weights, dot() moltiplica una matrice per un vettore, assurda
    #riguarda la formula per approfondimenti
    print("Expected portfolio mean(return): ",portfolio_return)
    print("Expected portfolio volatility(standard deviation): ",portfolio_volatility)


def generate_portfolios(returns):
    #array di array
    portfolio_means = []
    portfolio_risks = []
    portfolio_weights = [] 

    for _ in range(NUM_PORTFOLIOS):
        w = np.random.random(len(stocks)) #generate a random 1-dimensional array 
        w /= np.sum(w) # somma totale dell' array 1, in pratica divido il numero random per la somma, easy
        portfolio_weights.append(w)
        portfolio_means.append(np.sum(returns.mean() * w) * NUM_TRADING_DAYS)
        portfolio_risks.append(np.sqrt(np.dot(w.T,np.dot(returns.cov()*NUM_TRADING_DAYS,w))))
    
    return np.array(portfolio_weights),np.array(portfolio_means),np.array(portfolio_risks)

def show_portfolios(returns,volatilities):
    plt.figure(figsize=(10,6))                                              #inizializzo la figura
    plt.scatter(volatilities,returns, c= returns/volatilities,marker='o')   #grafico a scatter, ovvero a punti co dispersione
    plt.grid(True)                                                          #visualizza la griglia nel grafico
    plt.xlabel('Expected Volatility')                                       #label asse delle x
    plt.ylabel("Expected return")
    plt.colorbar(label='Sharpe Ratio')                                      #label barra colorata
    plt.show()

def statistics(weights,returns):
    portfolio_return = np.sum(returns.mean() * weights) * NUM_TRADING_DAYS
    portfolio_volatility = np.sqrt(np.dot(weights.T,np.dot(returns.cov()*NUM_TRADING_DAYS,weights)))
    sharpe_ratio = portfolio_return/portfolio_volatility

    return np.array([portfolio_return,portfolio_volatility,sharpe_ratio])

#scipy optimization puo' trovare il minimo di una funzione\
#il maximum della funzione f(x) e' il minimo di -f(x)
def min_function_sharpe(weights,returns):
    return -statistics(weights,returns)[2]

#le constraints sono la somma dei weights = 1
#sum w - 1 = 0  f(x) = 0, questa e' la funzione da minimizzare
def optimize_portfolio(weights,returns):
    #la somma dei weights e' uguale ad 1
    constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) -1}
    #i weights possono essere max 1
    bounds = tuple((0,1) for _ in range(len(stocks)))

    return optimization.minimize(fun=min_function_sharpe, x0=weights[0], args=returns, method='SLSQP',bounds=bounds, constraints=constraints)

def print_optimal_portfolio(optimum, returns):
    print("Optimum portfolio: ",optimum['x'].round(3))
    print("Expected return, volatility, sharpe ratio: ", statistics(optimum['x'].round(3),returns))

def show_optimal_portfolios(opt,rets,portfolio_rets,portfolio_vols):
    plt.figure(figsize=(10,6))                                              #inizializzo la figura
    plt.scatter(portfolio_vols,portfolio_rets, c= portfolio_rets/portfolio_vols,marker='o')   #grafico a scatter, ovvero a punti co dispersione
    plt.grid(True)                                                          #visualizza la griglia nel grafico
    plt.xlabel('Expected Volatility')                                       #label asse delle x
    plt.ylabel("Expected return")
    plt.colorbar(label='Sharpe Ratio')                                      #label barra colorata
    plt.plot(statistics(opt['x'],rets)[1],statistics(opt['x'],rets)[0],'g*', markersize=20.0)
    plt.show()

if __name__=='__main__':
    dataset=download_data()
    show_data(dataset)
    log_daily_returns=calculate_return(dataset)

    #show_statistics(log_daily_returns)

    weights,means,risks=generate_portfolios(log_daily_returns)
    show_portfolios(means,risks)
    optimum = optimize_portfolio(weights,log_daily_returns)
    print_optimal_portfolio(optimum,log_daily_returns)
    show_optimal_portfolios(optimum, log_daily_returns, means, risks)

