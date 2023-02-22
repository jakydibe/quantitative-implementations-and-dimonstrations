from math import exp


                        #money,interest_rate,time
def future_discrete_value(x, r, n):
    return x*(1+r)**n

def present_discrete_value(x, r, n):
    return x*(1+r)**(-n) #-n perche se ricordi la formula e' x/quella roba, percio esponente negativo

                        #money,interest_rate,time
def future_continuous_value(x, r, t):
    return x*exp(r*t)

def present_continuous_value(x, r, t):
    return x*exp(-r*t) #-n perche se ricordi la formula e' x/quella roba, percio esponente negativo

if __name__ == '__main__':

    #value of investment in dollars
    x = 100
    #deifne interest rate(r)
    r = 0.05 #5% annuo
    #duration(years)
    n=5

    print("future values (discrete) of x: " + future_discrete_value(x,r,n))
    print("present values (discrete) of x: " + present_discrete_value(x,r,n))
    print("future values (continuou) of x: " + future_continuous_value(x,r,n))
    print("present values (continuous) of x: " + present_continuous_value(x,r,n))

