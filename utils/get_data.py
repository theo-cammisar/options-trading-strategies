import yfinance as yf

class get_data:

    def __init__(self, ticker ,start, end, interval):

        self.ticker = ticker
        self.start = start
        self.end = end 
        self.interval = interval

        
    def get_price_data(self):
        
        price_data = yf.download(tickers= self.ticker, start = self.start, 
                                 end = self.end, interval = self.interval,auto_adjust= True)
        
        return price_data
