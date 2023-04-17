# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 21:59:00 2023

@author: ignacio

Python script to calculate and visualize the Sharpe ratios for a set of stock 
tickers. 

The script starts by defining a set of ticker symbols for various sectors and 
regions, as well as a boolean flag for selecting all S&P 500 stocks. It then 
calls the function Get_tickers from another module with the selected parameters 
to retrieve the full list of tickers.

We use the yfinance library to retrieve the stock price history for each ticker 
over the past 5 years and past 2 years. It then calculates the Sharpe ratio for 
each ticker and time period using the formula 
(mean return / standard deviation of return) * sqrt(252), where 252 is the 
number of trading days in a year. The Sharpe ratios are stored in a dictionary.

The script then identifies the Sharpe ratios of the S&P 500 index for the past 
2 years and past 5 years. It creates a list of tickers that have higher Sharpe 
ratios than the S&P 500 in both periods.

Finally, the script visualizes the Sharpe ratios of all tickers in a scatter 
plot with the x-axis representing the Sharpe ratio for the past 2 years and the 
y-axis representing the Sharpe ratio for the past 5 years. The S&P 500 is 
represented as a single orange dot, while the other tickers are represented as 
yellow dots with their ticker symbols annotated next to them. 
The script also includes horizontal and vertical lines to represent the Sharpe 
ratios of the S&P 500 and a regression line (if Regression == True).
"""

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


from to_run_FA import write_on_Excel, Get_tickers
from Fundamentals_summary import overall_analysis
    
#### -----------  Select the tickers -----------####

All_SP500   = False    
Nasdaq      = []
Retail      = []
Semis       = []
Otros_SP500 = []
Materials   = []
Energia     = []
Beach       = []
Alemania    = []
Arg         = []
Particular  = ["V","GOOG","NFLX","META","DIS","TSLA","AMZN","ABNB","MELI",
               "BMW.DE","BKNG","MCD","ADS.DE","SBUX","NKE","MOH.F","KO","CTRA",
               "PXD","OXY","MPC","V","PYPL","BRK.B","MA","JNJ","AIR.DE","LHA.DE",
               "DE","BA","GLOB","AMD","AAPL","MU","TSM","NA9.DE","INTC","ZM",
               "MSFT","ASML","CSCO","ADBE","CRM","^GSPC"]

limit_to_quad2 = False     

#### ----------- Run all the code -----------####

Activos,columns_list = Get_tickers(Nasdaq , Retail , 
                                   Semis , Otros_SP500 , 
                                   Materials, Energia , 
                                   Beach, Alemania, Arg, Particular, 
                                   All_SP = All_SP500)




plt.style.use('dark_background')

tickers = Activos
# Get data for last 5 years and last 2 years for each ticker
data = {}
for ticker in tickers:
    stock = yf.Ticker(ticker)
    hist_data = stock.history(period="5y")
    data[ticker] = {"5y": hist_data, "2y": hist_data.tail(504)}
    
# Calculate Sharpe ratios for each ticker and period
sharpe_ratios = {}
for ticker in tickers:
    sr_5y = (data[ticker]["5y"]["Close"].pct_change().mean() / data[ticker]["5y"]["Close"].pct_change().std()) * (252 ** 0.5)
    sr_2y = (data[ticker]["2y"]["Close"].pct_change().mean() / data[ticker]["2y"]["Close"].pct_change().std()) * (252 ** 0.5)
    sharpe_ratios[ticker] = {"5y": sr_5y, "2y": sr_2y}

sp500_sr_2y = sharpe_ratios['^GSPC']['2y']
sp500_sr_5y = sharpe_ratios['^GSPC']['5y']

tickers_with_high_sr = []
for ticker in tickers:
    sr_2y = sharpe_ratios[ticker]['2y']
    sr_5y = sharpe_ratios[ticker]['5y']
    if sr_2y > sp500_sr_2y and sr_5y > sp500_sr_5y:
        tickers_with_high_sr.append(ticker)

print("Tickers with higher Sharpe Ratios than SP500 in both 2y and 5y:")
print(tickers_with_high_sr)


fig, ax = plt.subplots()
for ticker in tickers:
    if ticker == "^GSPC":
        ax.plot(sharpe_ratios[ticker]["2y"], sharpe_ratios[ticker]["5y"], "o", color="orange", markersize=10)
        ax.annotate("SP500", xy=(sharpe_ratios[ticker]["2y"], sharpe_ratios[ticker]["5y"]), xytext=(0, 0), textcoords="offset points", ha="center", va="center", fontsize=10)
        sp500_sr_5y = sharpe_ratios[ticker]["5y"]
        sp500_sr_2y = sharpe_ratios[ticker]["2y"]
    else:
        ax.plot(sharpe_ratios[ticker]["2y"], sharpe_ratios[ticker]["5y"], "o", color="y", alpha=0.5, markersize=20)
        ax.annotate(ticker, xy=(sharpe_ratios[ticker]["2y"], sharpe_ratios[ticker]["5y"]), xytext=(0,0), textcoords="offset points", ha="center", va="center", fontsize=10)
ax.axhline(sp500_sr_5y, color="orange", linestyle=":")
ax.axvline(sp500_sr_2y, color="orange", linestyle=":")
ax.set_xlabel("Sharpe Ratio (Last 2 Years)")
ax.set_ylabel("Sharpe Ratio (Last 5 Years)")
ax.grid(zorder=0,alpha=0.5)

if limit_to_quad2:    
    ax.set_ylim(bottom=sp500_sr_5y)
    ax.set_xlim(left=sp500_sr_2y)
   
Regression = False
if Regression:                                                                                   
    import numpy as np
    from scipy.stats import linregress
    
    # Get x and y values from sharpe_ratios dictionary
    x = [sharpe_ratios[ticker]["2y"] for ticker in tickers if ticker != "^GSPC"]
    y = [sharpe_ratios[ticker]["5y"] for ticker in tickers if ticker != "^GSPC"]
    
    # Calculate linear regression coefficients
    slope, intercept, rvalue, pvalue, stderr = linregress(x, y)
    
    # Create x and y values for regression line
    reg_x = np.array([min(x), max(x)])
    reg_y = slope * reg_x + intercept
    ## Add regression line to plot
    ax.plot(reg_x, reg_y, color="green")



### Here we make some backtesting
### Define tickers and allocation
tickers = ["AAPL", "MSFT", "GOOG", "AMZN"]
allocation = [0.25, 0.25, 0.25, 0.25]

# Download data from Yahoo Finance
data = yf.download(tickers, start="2017-01-01", end=pd.Timestamp.today())

# Calculate daily returns
returns = data["Adj Close"].pct_change()

# Calculate daily portfolio returns
port_returns = (returns * allocation).sum(axis=1)

# Calculate cumulative portfolio returns
port_cum_returns = (port_returns + 1).cumprod()

# Calculate cumulative SP500 returns
sp500 = yf.download("^GSPC", start="2017-01-01", end=pd.Timestamp.today())
sp500_cum_returns = (sp500["Adj Close"].pct_change() + 1).cumprod()

# Plot portfolio and SP500 returns
fig, ax = plt.subplots()
ax.plot(port_cum_returns, label="Portfolio")
ax.plot(sp500_cum_returns, label="SP500")
ax.legend()
ax.set_xlabel("Date")
ax.set_ylabel("Cumulative Returns")
ax.set_title("Buy and Hold Portfolio vs. SP500")
plt.show()
