from backtesting.get_data import get_data
from strategies.butterfly_strategy import butterfly_strategy
from strategies.backspread_call import backspread_call
from strategies.long_straddle import LongStraddle


class backtester_strategy:
    def __init__(self, ticker,start,end,interval):
        self.ticker = ticker
        self.start = start
        self.end = end
        self.interval = interval
    
    def get_data(self):
        price_data_util = get_data(self.ticker, self.start, self.end, self.interval)
        price_data = price_data_util.get_price_data()[self.ticker].to_numpy()
        S = price_data[0]
        S_T = price_data[-1]
        
        return S, S_T
    
    def backspread_call_tester(self,K2,T,r,sigma,a,b,step):
        S, S_T = self.get_data()
        K1 = S
        
        backspread_strat = backspread_call(K1,K2,T,S,r,sigma,a,b,step)
        backspread_payoff = backspread_strat.get_payoff(S_T)
        
        return {'Strike 1 pour ajustement': K1,
                'Payoff': f"{backspread_payoff:.2f} $"}
    
    def butterfly_tester(self,K1,K3,T,r,sigma,a,b,step,c):
        S, S_T = self.get_data()
        K2 = S + c
        
        butterfly_strat =butterfly_strategy(K1,K2,K3,S,T,r,sigma,a,b,step)
        butterfly_payoff = butterfly_strat.get_payoff(S_T)
        
        return {'K2 pour ajustement:': f'{K2:.2f}',
                'Payoff de la strategie à échéance:': f"{butterfly_payoff:.2f}"}

    def long_straddle_tester(self, T,r,sigma,a,b,step,c):
        S, S_T = self.get_data()
        K = S + c

        LS_strat = LongStraddle(T,r,sigma,a,b,step)
        LS_payoff = LS_strat.get_payoff(S_T)

        return {'Strike 1:': K,
                'Prix Sport': S,
                'Payoff à échéance:': f"{LS_payoff:.2f}"}