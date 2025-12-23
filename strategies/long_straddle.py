"""
Created on Sun Dec 14 20:33:58 2025

@author: theo.cammisar
"""

from utils.black_scholes_model_oop import bs_model
from utils.base import OptionStrategy
import pandas as pd
import numpy as np

class LongStraddle(OptionStrategy):
    
    def __init__(self, K, S, T, r, sigma, a, b, step,model = bs_model):
        
        self.K = K
        self.S = S
        self.T = T
        self.r = r
        self.sigma = sigma
        self.model_class = model
        self.a = a
        self.b = b
        self.step = step
        
        self.verif()
        
        """
        Ce qu il faut faire c'est qu'il faut créer des objets directement pour pouvoir les réutiliser
        
        """
        
    def verif(self):
        if self.S <= 0:
            raise ValueError(f"Problem S: {self.S}")
        
        if self.T <=0:
           raise ValueError(f"Problem T: {self.T}")
        
        if self.sigma <= 0:
            raise ValueError(f"Problem sigma: {self.sigma}")

        if self.step <= 0:
            raise ValueError(f"Problem step: {self.step}")

    def get_model(self):
        call_import = bs_model(self.K,self.S,self.T, self.r,self.sigma)
        put_import = bs_model(self.K,self.S,self.T, self.r,self.sigma)

        call_summary = call_import.summary()
        put_summary = put_import.summary()

        return call_summary, put_summary

    def get_price(self):
        call_summary, put_summary = self.get_model()

        call = call_summary.iloc[0,1]
        put = put_summary.iloc[1,1]

        return call, put

    def get_cost(self):
        call,put = self.get_price()

        cost = call + put

        return cost

    def get_ech_price(self):
        ech_price = np.arange(self.a,self.b,self.step)

        return ech_price
       
    def get_payoff(self, S_T = None):
        call, put = self.get_price()
        ech_price = self.get_ech_price()

        if S_T is None:
            payoff = - (call + put) + np.maximum(ech_price - self.K, 0) + np.maximum(self.K - ech_price, 0)
        else:
            payoff = - (call + put) + np.maximum(S_T - self.K, 0) + np.maximum(self.K - S_T, 0)

        return payoff,S_T

    def get_greeks(self):
        call_summary, put_summary = self.get_model()
        
        Lsdelta = (call_summary.iloc[0,2] + put_summary.iloc[1,2]) * 100
        Lsgamma = (call_summary.iloc[0,3] + put_summary.iloc[1,3]) * 100
        Lstheta = (call_summary.iloc[0,4] + put_summary.iloc[1,4]) * 100
        Lsvega = (call_summary.iloc[0,5] + put_summary.iloc[1,5]) * 100
        Lsrho = (call_summary.iloc[0,6] + put_summary.iloc[1,6]) * 100

        return Lsdelta, Lsgamma,Lstheta,Lsvega,Lsrho

    def summary(self):
        Lsdelta, Lsgamma, Lstheta, Lsvega, Lsrho = self.get_greeks()
        call, put = self.get_price()
        cost = self.get_cost()

        data = [{
            'Cost': f"{cost:.2f}",
            'CP': f"{call:.2f}",
            'PP': f"{put:.2f}",
            'Delta': f"{Lsdelta:.2f}",
            'Gamma': f"{Lsgamma:.2f}",
            'Theta': f"{Lstheta:.2f}",
            'Vega': f"{Lsvega:.2f}",
            'Rho': f"{Lsrho:.2f}"
            }]
        
        return pd.DataFrame(data)
