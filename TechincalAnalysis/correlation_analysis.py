# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 20:44:10 2023

@author: ignacio

The correlation coefficient will tell us how closely the daily returns of the 
two assets are related. If the correlation coefficient is close to 1, it means 
that the two assets move together, and if it is close to -1, it means that they 
move in opposite directions. If the coefficient is close to 0, it means that 
there is no relationship between their returns.

Note that we are comparing the daily returns of the assets, rather than their 
prices, because this gives us a better indication of how closely they are 
related. Prices can be influenced by many factors, but returns are a more 
direct measure of the performance of the assets.

We can also plot the daily returns of the two assets to get a better idea of 
how they are related.

"""


import numpy as np

import matplotlib.pyplot as plt

import yfinance as yf

# Get historical data for gold futures
gold_futures = yf.Ticker('GC=F')
gold_futures_data = gold_futures.history(period='2y')

# Get historical data for Barrick Gold
barrick_gold = yf.Ticker('GOLD')
barrick_gold_data = barrick_gold.history(period='2y')


# Plot the adjusted close price for both assets
plt.plot(gold_futures_data['Close'], label='Gold Futures')
plt.plot(barrick_gold_data['Close']*100, label='Barrick Gold')
plt.legend()
plt.show()


# Calculate the correlation coefficient between the assets' daily returns
gold_futures_returns = np.log(gold_futures_data['Close']).diff()
barrick_gold_returns = np.log(barrick_gold_data['Close']).diff()
corr = gold_futures_returns.corr(barrick_gold_returns)

print(f"Correlation coefficient: {corr}")

# Plot the daily returns for both assets
plt.plot(barrick_gold_returns, label='Barrick Gold')
plt.plot(gold_futures_returns, label='Gold Futures')

plt.legend()
plt.show()
