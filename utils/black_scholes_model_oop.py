import pandas as pd
import numpy as np
from scipy.stats import norm




"""
Implémentation du modèle de Black-Scholes-Merton en programmation orientée objet.
Output : prix, greeks

"""

class bs_model:
    
    def __init__(self,K,S,t,r,sigma):
        
        self.K = K
        self.S = S
        self.t = t
        self.r = r
        self.sigma = sigma
    
    def compute(self):
        
        d1 = ((np.log(self.S/self.K) + (self.r + 0.5*self.sigma**2)*self.t) / 
              (self.sigma*np.sqrt(self.t)))
        d2 = d1 - self.sigma*np.sqrt(self.t)
        
        return d1, d2

        
    def get_price(self):
        
        d1, d2 = self.compute()
        
        N_d1 = norm.cdf(d1)
        N_d2 = norm.cdf(d2)
        
        call = self.S*N_d1-self.K*np.exp(-self.r*self.t)*N_d2
        put = self.K*np.exp(-self.r*self.t)*norm.cdf(-d2)-self.S*norm.cdf(-d1)
        
        return {'Call':call, 'Put': put}
    
    def get_greeks(self):
        
        d1, d2 = self.compute()
   
        delta_call = norm.cdf(d1)
        delta_put = norm.cdf(d1)-1
        
        gamma = norm.pdf(d1)/ (self.S*self.sigma*np.sqrt(self.t))
        
        vega = (self.S*norm.pdf(d1)*np.sqrt(self.t))/100
        
        theta_call = (-((self.S*norm.cdf(d1)*self.sigma)/(2*np.sqrt(self.t))) - 
                      self.r*self.K*np.exp(-self.r*self.t)*norm.cdf(d2))/365
        theta_put = (-((self.S*norm.cdf(d1)*self.sigma)/(2*np.sqrt(self.t))) + 
                     self.r*self.K*np.exp(-self.r*self.t)*norm.cdf(-d2))/365
        
        rho_call = (self.K * self.t * np.exp(-self.r * self.t) * norm.cdf(d2))/100
        rho_put = (-self.K * self.t * np.exp(-self.r * self.t) * norm.cdf(-d2))/100
        
        """
        delta: how the option price moves when the underlying price moves
        gamma: how delta changes when the underlying moves
        vega: measures the variation of the option price with respect to volatility
        theta: loss of value per unit of time (here 1 day)
        rho: variation of the option price with respect to the risk-free rate
        """
        
        return {'Delta_call': delta_call,
                'Delta_put': delta_put, 
                'Gamma':gamma,
                'Vega': vega,
                'Theta_call': theta_call,
                'Theta_put': theta_put,
                'Rho_call': rho_call,
                'Rho_put': rho_put}
    
    def summary(self):

        price = self.get_price()
        greeks = self.get_greeks()
        
        data1 = [
      {
          'Type': 'Call',
          'Prix': price['Call'],
          'Delta': greeks['Delta_call'],
          'Gamma': greeks['Gamma'],
          'Vega': greeks['Vega'],
          'Theta': greeks['Theta_call'],
          'Rho': greeks['Rho_call']
      },
      {
          'Type': 'Put',
          'Prix': price['Put'],
          'Delta': greeks['Delta_put'],
          'Gamma': greeks['Gamma'],
          'Vega': greeks['Vega'],
          'Theta': greeks['Theta_put'],
          'Rho': greeks['Rho_put']
      }
  ]
        
        return pd.DataFrame(data1)

""" 
Objectif : pricer des options vanilles avec la vol implicite, le strike et l'échéance associée
Besoin : strike, impleid vol et échéance se trouve dans volatility_smile.py et S ke prix spot
se trouve dans get_data.py
"""

