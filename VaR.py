import numpy as np
import yfinance as yf
from scipy.stats import norm
import pandas as pd
import datetime


def download_data(stock, start_date, end_date):
    data = {}
    ticker = yf.download(stock, start_date, end_date)
    data[stock] = ticker['Adj Close']
    return pd.DataFrame(data)


# this is how we calculate the VaR tomorrow (n=1)
def calculate_var(position, c, mu, sigma):
    var = position * (mu - sigma * norm.ppf(1-c))
    return var


# this is how we calculate the VaR for any days in the future
def calculate_var_n(position, c, mu, sigma, n):
    var = position * (mu * n - sigma * np.sqrt(n) * norm.ppf(1-c))
    return var


class ValueAtRiskMonteCarlo:

    def __init__(self, S, mu, sigma, c, n, iterations):
        self.S = S
        self.mu = mu
        self.sigma = sigma
        self.c = c
        self.n = n
        self.iterations = iterations

    def simulation(self):
        stock_data = np.zeros([self.iterations, 1])
        rand = np.random.normal(0, 1, [1, self.iterations])

        # equation for the S(t) stock price
        stock_price = self.S * np.exp(self.n * (self.mu - 0.5 * self.sigma ** 2) + self.sigma * np.sqrt(self.n) * rand)

        # we have to sort the stock prices to determine the percentile
        stock_price = np.sort(stock_price)

        # it depends on the confidence level: 95% -> 5 and 99% -> 1
        percentile = np.percentile(stock_price, (1 - self.c) * 100)

        return self.S - percentile

if __name__ == '__main__':

    start = datetime.datetime(2014, 1, 1)
    end = datetime.datetime(2018, 1, 1)



    stock_data = download_data('C', start, end)

    stock_data['returns'] = np.log(stock_data['C'] / stock_data['C'].shift(1))
    stock_data = stock_data[1:]
    print(stock_data)

    # this is the investment (stocks or whatever)
    S = 1e6
    # confidence level - this time it is 95%
    c = 0.99

    # we assume that daily returns are normally distributed
    mu = np.mean(stock_data['returns'])
    sigma = np.std(stock_data['returns'])

    print('Value at risk is: $%0.2f' % calculate_var_n(S, c, mu, sigma, 1))
    ####################################
    iterations = 100000
    n=1
    model = ValueAtRiskMonteCarlo(S, mu, sigma, c, n, iterations)

    print('Value at risk with Monte-Carlo simulation: $%0.2f' % model.simulation())