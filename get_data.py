

import yfinance as yf

"""
l'ojectif est de tester les stratégie         
"""

class get_data:

    def __init__(self, ticker ,start, end, interval):

        self.ticker = ticker
        self.start = start
        self.end = end 
        self.interval = interval

        
    def get_price_data(self):
        
        price_data = yf.download(tickers= self.ticker, start = self.start, 
                                 end = self.end, interval = self.interval,auto_adjust= True)['Close']
        
        return price_data