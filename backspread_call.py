#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 09:48:18 2025

@author: theo.cammisar
"""

from utils.black_scholes_model_oop import bs_model
from utils.base import OptionStrategy
import pandas as pd
import numpy as np


class backspread_call(OptionStrategy):
    
    def __init__(self, K1, K2, T,S, r, sigma, a, b, step, model = bs_model):
        self.K1 = K1
        self.K2 = K2
        self.T = T
        self.S = S
        self.r = r
        self.model = model
        self.sigma = sigma
        self.a = a
        self.b = b
        self.step = step
        
        self.verif() 
    
    def verif(self):
        if self.S < 0:
            raise ValueError(f"Problem S: {self.S}")
            
        if self.T <=0:
           raise ValueError(f"Problem T: {self.T}")
        
        if self.sigma <= 0:
            raise ValueError(f"Problem sigma: {self.sigma}")
        
        if self.K1 >= self.K2: 
            raise ValueError("should have K1 < K2")
        
        if self.step <= 0:
            raise ValueError(f"Problem step: {self.step}")
            
    def get_model(self):
        
        bk1 = self.model(self.K1, self.S, self.T, self.r, self.sigma)
        bk2 = self.model(self.K2, self.S, self.T, self.r, self.sigma)
        
        result_bk1 = bk1.summary()
        result_bk2 = bk2.summary()
        
        return result_bk1, result_bk2
    
    def get_price(self):
        result_bk1, result_bk2 = self.get_model()
        
        price_short_call = result_bk1.loc[0,'Prix']
        price_long_call = result_bk2.loc[0,'Prix']
        
        return price_short_call, price_long_call
    
    def get_delta(self):
        result_bk1, result_bk2 = self.get_model()
        
        d_short_call = result_bk1.loc[0,'Delta']
        d_long_call = result_bk2.loc[0,'Delta']
        
        return d_short_call, d_long_call
        
    def neutral_delta(self):
        d_short_call, d_long_call = self.get_delta()
        
        if abs(d_short_call - d_long_call) < 1e-3:
            n_long_call = 1
        else:
            n_long_call = d_short_call / d_long_call
        
        return n_long_call
    
    def premium_diff(self):
        n_long_call = self.neutral_delta()
        price_short_call, price_long_call = self.get_price()
        
        diff = price_short_call - price_long_call * n_long_call
        
        if diff < 0:
            raise ValueError(f"Problem diff :{diff}")
        
        return diff

    def get_ech_price(self):
        ech_price = np.arange(self.a,self.b,self.step)

        return ech_price
        
    def get_payoff(self, S_T = None):
        ech_price = self.get_ech_price()
        diff = self.premium_diff()
        n_long_call = self.neutral_delta()
        
        if S_T is None:
            payoff = diff - np.maximum(ech_price - self.K1, 0) + n_long_call * np.maximum(ech_price - self.K2, 0)
        else:
            payoff = diff - np.maximum(S_T - self.K1, 0) + n_long_call * np.maximum(S_T - self.K2, 0)

        return payoff
    
    def get_greeks(self):
        result_bk1, result_bk2 = self.get_model()
        n_long_call = self.neutral_delta()
        d_short_call, d_long_call = self.get_delta()
        
        bk_delta = d_short_call - n_long_call * d_long_call
        bk_gamma = (result_bk1.loc[0,'Gamma'] - n_long_call * result_bk2.loc[0,'Gamma']) * 100
        bk_theta = (result_bk1.loc[0,'Theta'] - n_long_call * result_bk2.loc[0,'Theta']) * 100
        bk_vega = (result_bk1.loc[0,'Vega'] - n_long_call * result_bk2.loc[0,'Vega']) * 100
        bk_rho = (result_bk1.loc[0,'Rho'] - n_long_call * result_bk2.loc[0,'Rho']) * 100
        
        return {
            'D': bk_delta,
            'G': bk_gamma,
            'T': bk_theta,
            'V': bk_vega,
            'R': bk_rho
                }
        
    def summary(self):
        greeks = self.get_greeks()
        price_short_call, price_long_call = self.get_price()
        n_long_call = self.neutral_delta()
        
        data = [{
            'price SC': f"{price_short_call:.2f}",
            'price LC':f"{price_long_call:.2f}",
            'nbr LC': f"{n_long_call:.2f}",
            'Delta': greeks['D'],
            'Gamma': f"{greeks['G']:.4f}",
            'Theta': f"{greeks['T']:.4f}",
            'Vega': f"{greeks['V']:.4f}",
            'Rho': f"{greeks['R']:.4f}"
            }]
            
        return pd.DataFrame(data)