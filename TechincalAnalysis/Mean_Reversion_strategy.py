# -*- coding: utf-8 -*-
"""
Created on Wed Jan 11 11:19:40 2023

@author: ignacio

MEAN REVERSION STRATEGY

https://raposa.trade/blog/how-to-build-your-first-mean-reversion-trading-strategy-in-python/

This Python script defines a starting date and a DataFrame called "resultado" 
with four columns. The script also defines two functions.

"SMAMeanReversion" takes five arguments: 
ticker (a string that specifies the stock ticker), sma (an integer that specifies
the moving average period), threshold (a float that specifies the buy/sell 
threshold), shorts (a Boolean that specifies whether or not to allow short 
positions), and start_date (a string that specifies the start date for the data).

This function retrieves historical price data from yfinance, calculates the SMA,
and then computes an "extension" value by subtracting the SMA from the closing 
price and dividing the result by the SMA. Based on the "extension" value and 
the buy/sell threshold, the function calculates a position for each data point. 
The function then calculates the returns and some statistics related to the 
trategy, such as cumulative returns and peak returns. Finally, it returns a 
filtered DataFrame without any missing values.

The second function is called "SMAMeanReversionSafety" and has the same 
arguments as the first function, plus an additional argument called 
safety_threshold (a float that specifies a safety threshold to prevent entering 
into a position that is too risky). This function works similarly to the first 
function but calculates the position based on both the buy/sell threshold and 
the safety threshold.

The script then defines a list called "Cartera" that contains a single string 
with a stock ticker. It also defines some variables, such as the SMA period, 
the buy/sell threshold, and a Boolean for allowing short positions. Finally, it 
loops through the "Cartera" list, calls the "SMAMeanReversion" function for 
each stock ticker, and saves the resulting DataFrame in the "resultado" 
DataFrame. The script can also plot the price data, the SMA, and the long 
positions if the "plots" variable is set to True.


"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf

# end_date='2020-12-31'
Start_Date = '2018-01-01' #'2000-01-01'

def SMAMeanReversion(ticker, sma, threshold, shorts=False,
    start_date=Start_Date):
    yfObj = yf.Ticker(ticker)
    data = yfObj.history(start=start_date)#, end=end_date)
    data['SMA'] = data['Close'].rolling(sma).mean()
    data['extension'] = (data['Close'] - data['SMA']) / data['SMA']
    
    data['position'] = np.nan
    data['position'] = np.where(data['extension']<-threshold,
        1, data['position'])
    if shorts:
        data['position'] = np.where(
            data['extension']>threshold, -1, data['position'])
        
    data['position'] = np.where(np.abs(data['extension'])<0.01,
        0, data['position'])
    data['position'] = data['position'].ffill().fillna(0)
    
    # Calculate returns and statistics
    data['returns'] = data['Close'] / data['Close'].shift(1)
    data['log_returns'] = np.log(data['returns'])
    data['strat_returns'] = data['position'].shift(1) * \
        data['returns']
    data['strat_log_returns'] = data['position'].shift(1) * \
        data['log_returns']
    data['cum_returns'] = np.exp(data['log_returns'].cumsum())
    data['strat_cum_returns']  = np.exp(data['strat_log_returns'].cumsum())
    data['peak'] = data['cum_returns'].cummax()
    data['strat_peak'] = data['strat_cum_returns'].cummax()
    
    return data.dropna()




def SMAMeanReversionSafety(ticker, sma, threshold, 
    safety_threshold=0.25, shorts=False, 
    start_date=Start_Date):
    yfObj = yf.Ticker(ticker)
    data = yfObj.history(start=start_date)#, end=end_date)
    data['SMA'] = data['Close'].rolling(sma).mean()
    data['extension'] = (data['Close'] - data['SMA']) / data['SMA']
    
    data['position'] = np.nan
    data['position'] = np.where(
        (data['extension']<-threshold) & 
        (data['extension']>-safety_threshold), 
        1, data['position'])
    
    if shorts:
        data['position'] = np.where(
            (data['extension']>threshold) & 
            (data['extension']<safety_threshold),
            -1, data['position'])
        
    data['position'] = np.where(np.abs(data['extension'])<0.01,
        0, data['position'])
    data['position'] = data['position'].ffill().fillna(0)
    
    # Calculate returns and statistics
    data['returns'] = data['Close'] / data['Close'].shift(1)
    data['log_returns'] = np.log(data['returns'])
    data['strat_returns'] = data['position'].shift(1) * \
        data['returns']
    data['strat_log_returns'] = data['position'].shift(1) * data['log_returns']
    data['cum_returns'] = np.exp(data['log_returns'].cumsum())
    data['strat_cum_returns'] =\
        np.exp(data['strat_log_returns'].cumsum())
    data['peak'] = data['cum_returns'].cummax()
    data['strat_peak'] = data['strat_cum_returns'].cummax()
    
    return data.dropna()



ticker = 'DIS'
SMA = 50
threshold = 0.1
shorts = False
data = SMAMeanReversion(ticker, SMA, threshold, shorts)
plots = True

if plots:
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
    fig, ax = plt.subplots(3, figsize=(10, 8), sharex=True)
    long = data.loc[data['position']==1]['Close']
    ax[0].plot(data['Close'], label='Price', linestyle=':', color=colors[1])
    ax[0].plot(data['SMA'], label='SMA', linestyle='--', color=colors[0])
    ax[0].scatter(long.index, long, label='Long', c=colors[2])
    ax[0].legend(bbox_to_anchor=[1, 0.75])
    ax[0].set_ylabel('Price ($)')
    ax[0].set_title(f'{ticker} Price and Positions with {SMA}-Day Moving Average')
    ax[1].plot(data['extension']*100, label='Extension', color=colors[0])
    ax[1].axhline(threshold*100, linestyle='--', color=colors[1])
    ax[1].axhline(-threshold*100, label='Threshold', linestyle='--', color=colors[1])
    ax[1].axhline(0, label='Neutral', linestyle=':', color='k')
    ax[1].set_title('Price Extension and Buy/Sell Thresholds')
    ax[1].set_ylabel('Extension (%)')
    ax[1].legend(bbox_to_anchor=[1, 0.75])
    ax[2].plot(data['position'])
    ax[2].set_xlabel('Date')
    ax[2].set_title('Position')
    ax[2].set_yticks([-1, 0, 1])
    ax[2].set_yticklabels(['Short', 'Neutral', 'Long'])
    plt.tight_layout()
    plt.show()
#########################################################


safety_threshold = 0.15

data = SMAMeanReversion(ticker, SMA, threshold, shorts)
data_safe = SMAMeanReversionSafety(ticker, SMA, threshold, safety_threshold, shorts)
fig, ax = plt.subplots(figsize=(12, 5))
ax.plot(data_safe['strat_cum_returns'], label='Mean Reversion Strategy with Safety')
ax.plot(data['strat_cum_returns'], label='Mean Reversion Strategy')
ax.plot(data_safe['cum_returns'], label=f'{ticker}')
ax.set_xlabel('Date')
ax.set_ylabel('Returns (%)')
ax.set_title('Cumulative Returns for Mean Reversion and Buy and Hold Strategies')
ax.legend()
plt.show()

print('Strategy Safe:\t',data_safe['strat_cum_returns'].iloc[-1])
print('Strategy:\t\t',data['strat_cum_returns'].iloc[-1])
print('Buy and Hold:\t',data_safe['cum_returns'].iloc[-1])
