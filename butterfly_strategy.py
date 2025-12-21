#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  1 20:50:20 2025

@author: theo.cammisar
"""

from utils.black_scholes_model_oop import bs_model
from utils.base import OptionStrategy
import pandas as pd
import numpy as np

class butterfly_strategy(OptionStrategy):
    
    def __init__(self,K1,K2,K3,S,T,r,sigma,a,b,step, model = bs_model):
        
        self.K1 = K1
        self.K2 = K2
        self.K3 = K3
        self.S = S
        self.T = T
        self.r = r
        self.sigma = sigma
        self.a = a
        self.b = b
        self.step = step
        self.model = model
        
        self.verif()

    
    def verif(self):
        if not 0 < self.K1 < self.K2 < self.K3:
            raise ValueError(f'Problem on K1, K2, K3: {self.K1},{self.K2},{self.K3}')
        
        #if self.S <=0:
            #raise ValueError(f'Problem S: {self.S}')
            
        if self.T <= 0:
            raise ValueError(f'Problem T: {self.T}')
        
        if self.sigma < 0:
            raise ValueError(f'Problem sigma: {self.sigma}')
            
        if not 0 <= self.a <= self.b:
            raise ValueError(f'Problem a, b: {self.a}, {self.b}')
    
    def get_model(self):
        bt_1 = self.model(self.K1, self.S, self.T, self.r, self.sigma) # call ITM
        bt_2 = self.model(self.K2, self.S, self.T, self.r, self.sigma) # call ATM
        bt_3 = self.model(self.K3, self.S, self.T, self.r, self.sigma) # call OTM
        
        result_bt_1 = bt_1.summary()
        result_bt_2 = bt_2.summary()
        result_bt_3 = bt_3.summary()
        
        return result_bt_1, result_bt_2, result_bt_3
    
    def get_price(self):
        result_bt_1,result_bt_2, result_bt_3 = self.get_model()
        
        price_ITM = result_bt_1.loc[0,'Prix']
        price_ATM = result_bt_2.loc[0,'Prix']
        price_OTM = result_bt_3.loc[0,'Prix']
        
        return price_ITM, price_ATM, price_OTM
    
    def strategy_cost(self):
        price_ITM, price_ATM, price_OTM = self.get_price()
        
        cost = price_ITM + price_OTM - 2 * price_ATM
        
        return cost
        
    def get_payoff(self, S_T = None):
        cost = self.strategy_cost()
        
        if S_T is None:
            S_T = np.arange(self.a,self.b, self.step)
        
        payoff = np.maximum(S_T - self.K1,0) + np.maximum(S_T - self.K3,0) - 2 * np.maximum(S_T - self.K2,0) - cost
            
        return payoff

    
    def get_greeks(self):
        result_bt_1,result_bt_2, result_bt_3 = self.get_model()
        
        btdelta = (result_bt_1.loc[0,'Delta'] + result_bt_3.loc[0,'Delta'] - 2 * result_bt_2.loc[0,'Delta']) * 100
        btgamma = (result_bt_1.loc[0,'Gamma'] + result_bt_3.loc[0,'Gamma'] - 2 * result_bt_2.loc[0,'Gamma']) * 100
        btvega = (result_bt_1.loc[0,'Vega'] + result_bt_3.loc[0,'Vega'] - 2 * result_bt_2.loc[0,'Vega']) * 100
        bttheta = (result_bt_1.loc[0,'Theta'] + result_bt_3.loc[0,'Theta'] - 2 * result_bt_2.loc[0,'Theta']) * 100
        btrho = (result_bt_1.loc[0,'Rho'] + result_bt_3.loc[0,'Rho'] - 2 * result_bt_2.loc[0,'Rho']) * 100
        
        return {
                'Delta': btdelta,
                'Gamma': btgamma,
                'Vega': btvega,
                'Theta': bttheta,
                'Rho': btrho
                }
    
    def bt_summary(self):
        btgreeks = self.get_greeks()
        cost = self.strategy_cost()
        payoff = self.get_payoff()
        
        data = [{
            'Cost': f"{cost:.2f}",
            'Delta': f"{btgreeks['Delta']:.2f}",
            'Gamma': f"{btgreeks['Gamma']:.2f}",
            'Vega': f"{btgreeks['Vega']:.2f}",
            'Theta': f"{btgreeks['Theta']:.2f}",
            'Rho': f"{btgreeks['Rho']:.2f}",
            }]
        
        return pd.DataFrame(data), payoff
        
bt = butterfly_strategy(95, 100, 105, 100, 1/12, 0.02, 0.4, 80, 120,0.5)
bt.get_graph()
bt.bt_summary()



        
        
        
        
        
