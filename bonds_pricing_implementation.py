import math 

class ZeroCouponBonds:
                       #pagamento finale,tempo rimanente per la scadenza, tassi di interesse di mercato
    def __init__(self, principal, maturity, interest_rate):
        self.principal=principal
        self.maturity=maturity
        self.interest_rate=interest_rate
                           #principal ,anno di possesso(1 anno, 2 anno time-to-maturity)
    def present_value(self,x ,n ):
        return x / (1 + self.interest_rate)**n
    def present_value_continuos_model(self, x ,n):
        return x*math.exp(-self.interest_rate*n)
    def calculate_price(self):
        return self.present_value(self.principal, self.maturity)


class CouponBond:
    def __init__(self,principal,coupon_rate,maturity,interest_rate):
        self.principal=principal
        self.coupon_rate=coupon_rate
        self.maturity=maturity
        self.interest_rate=interest_rate
                           #principal,interest_rate
    def present_value(self,x ,n ):
        return x / (1 + self.interest_rate)**n

    def present_value_continuos_model(self, x ,n):
        return x*math.exp(-self.interest_rate*n)

    def calculate_price(self):
        #discount the coupon payment 1 by one
        price = 0
        for t in range(1, self.maturity+1):
            price = price + self.present_value(self.principal * self.coupon_rate,t)  # ad ogni anno aggiungo il valore del coupon relativo a quel anno

        #discount the principal amount
        price = price + self.present_value(self.principal,self.maturity)
        return price

if __name__ == '__main__':
    zc_bond= ZeroCouponBonds(1000,3,0.04)
    print("prezzo del zc_bond in dollari : "+str(zc_bond.calculate_price()))
    print("guadagno zc_bond in 3 anni: " + str(1000-zc_bond.calculate_price())) #111$ in 3 anni

    c_bond = CouponBond(1000,0.1,3,0.04)
    print("prezzo del c_bond in dollari : "+str(c_bond.calculate_price())) #1167 ovvero se pago oggi 1167, me danno per 3 anni il 10% di 1000 (100 + 100 + 100) e infine me danno il present ovvero 1000$
    print("guadagno c_bond in 3 anni: " + str(1300-c_bond.calculate_price())) #133$ in 3 anni
