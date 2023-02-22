import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt

RISK_FREE_RATE=0.05
MONTHS_IN_YEAR=12


class CAPM:
    def __init__(self,stocks,start_date,end_date):
        self.data=None
        self.stocks=stocks
        self.start_date=start_date
        self.end_date=end_date

    def download_data(self):
        data = {}

        for stock in self.stocks:
            ticker = yf.download(stock,self.start_date,self.end_date)
            data[stock] = ticker['Adj Close'] #non e' una normale close, ma una close ponderata con altri fattori come dividendi, stock split e altre robe, e' un po' piu' accurato della close 
        return pd.DataFrame(data)

    def initialize(self):
        stock_data=self.download_data()
        stock_data = stock_data.resample('M').last() #li resiza a mesi invece che giorni

        self.data=pd.DataFrame({'s_adjclose':stock_data[self.stocks[0]],
                                'm_adjclose': stock_data[self.stocks[1]]})
        
        self.data[['s_returns','m_returns']] = np.log(self.data[['s_adjclose','m_adjclose']]/self.data[['s_adjclose','m_adjclose']].shift(1))
        #remove the NaN
        self.data=self.data[1:]
        print(self.data)

    def calculate_beta(self): #ricordiamo la formula per la beta e' cov(asset,mercato)/var(mercato)
        #covariance matrix: le diagonali sono le varianze
        #quelle non diagonali sono le covarianze
        #la matrice e' percio' simmetrice, cov[0,1] = cov[1,0] !!!!
        covariance_matrix = np.cov(self.data['s_returns'],self.data['m_returns'])
        beta=covariance_matrix[0,1]/covariance_matrix[1,1] #covariance tra IBM e SP500 diviso varianza di sp500)

        print("beta from formula: ", beta)

    def regression(self):
        #usiamo la regressione lineare
        
        beta,alpha=np.polyfit(self.data['m_returns'],self.data['s_returns'],deg=1) #polyfit cerca una regressione con grado deg, quindi se metto deg=3 in pratica me trova una cubica che fa la regressione di quel dataset
        print("beta from regression: ", beta)
        #calcoliamo gli expected returns con la CAPM formula

        expected_return = RISK_FREE_RATE + beta*(self.data['m_returns'].mean()*MONTHS_IN_YEAR - RISK_FREE_RATE) 
        print("Expected return: ",expected_return)

        self.plot_regression(alpha,beta)

    def plot_regression(self,alpha,beta):
        fig, axis = plt.subplots(1, figsize=(20, 10))
        axis.scatter(self.data["m_returns"], self.data['s_returns'],
                     label="Data Points")
        axis.plot(self.data["m_returns"], beta * self.data["m_returns"] + alpha,
                  color='red', label="CAPM Line")
        plt.title('Capital Asset Pricing Model, finding alpha and beta')
        plt.xlabel('Market return $R_m$', fontsize=18)
        plt.ylabel('Stock return $R_a$')
        plt.text(0.08, 0.05, r'$R_a = \beta * R_m + \alpha$', fontsize=18)
        plt.legend()
        plt.grid(True)
        plt.show()

    def dist_check()

        

if __name__ == '__main__':
    #il secondo simbolo e' l' S&P500
    capm = CAPM(['IBM','^GSPC'],'2010-01-01','2017-01-01')
    capm.initialize()
    capm.calculate_beta()
    capm.regression()