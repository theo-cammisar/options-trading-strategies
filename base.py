#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 15:26:32 2025

@author: theo.cammisar
"""

from abc import ABC, abstractmethod

class OptionStrategy(ABC):
    def __ini__(self, S, T, r, sigma):
        
        self.S = S
        self.T = T
        self.r = r
        self.sigma = sigma
        
        self.verif()
        
    @abstractmethod
    def verif(self):
        pass
    
    @abstractmethod
    def get_greeks(self):
        pass
    
    @abstractmethod
    def get_payoff(self):
        pass
    