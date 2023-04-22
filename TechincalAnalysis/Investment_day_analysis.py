# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 12:25:24 2023

@author: ignacio
"""
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import calendar

# Define the stock ticker symbol and date range
ticker = "TSM"
start_date = "2018-01-01"
end_date = "2022-03-25"

Weekly_day_analysis = True
Monthy_analysis = False
weekly_portfolio = True
monthly_portfolio = False

# Get the historical data for the stock
stock_data = yf.download(ticker, start=start_date, end=end_date)
# Compute the percentage change in price for each day
stock_data['pct_change'] = stock_data['Adj Close'].pct_change()
    
if Weekly_day_analysis:

    
    # Compute the mean percentage change for each day of the week
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    mean_pct_change = stock_data.groupby(stock_data.index.weekday)['pct_change'].mean()
    mean_pct_change.index = mean_pct_change.index.map(lambda x: weekdays[x])
    
    # Plot the histogram
    fig, ax = plt.subplots()
    ax.bar(mean_pct_change.index, mean_pct_change.values)
    ax.set_xlabel('Day of the Week')
    ax.set_ylabel('Mean % Change')
    ax.set_title(f'Mean % Change in {ticker} by Day of the Week')
    plt.show()

if Monthy_analysis:
    
    # Compute the mean percentage change for each month
    mean_pct_change = stock_data.groupby(stock_data.index.month)['pct_change'].mean()

    # Plot the histogram
    fig, ax = plt.subplots()
    ax.bar(mean_pct_change.index, mean_pct_change.values)
    ax.set_xlabel('Month')
    ax.set_ylabel('Mean % Change')
    ax.set_title(f'Mean % Change in {ticker} by Month')
    plt.show()

# Define a function to create a portfolio for a given weekday
def create_portfolio(day):
    portfolio = stock_data[stock_data.index.weekday == day]
    portfolio['return'] = portfolio['pct_change'] + 1
    portfolio['cum_return'] = portfolio['return'].cumprod()
    return portfolio


# Define a function to create a portfolio for a given day of the month
def create_monthly_portfolio(day):
    
    ''' This function is not working properly'''
    
    # Resample the data to get the last day of each month
    last_days = stock_data.resample('M').apply(lambda x: x.iloc[-1])
    # Filter to only the days with the desired day of the week
    last_days = last_days[last_days.index.dayofweek == day]
    
    # print(stock_data.loc[last_days.index[0:6]])
    
    portfolio = stock_data.loc[last_days.index]

    portfolio['return'] = portfolio['pct_change'] + 1
    portfolio['cum_return'] = portfolio['return'].cumprod()
    return portfolio


if weekly_portfolio:
    # Create portfolios for each weekday
    monday_portfolio = create_portfolio(0)
    tuesday_portfolio = create_portfolio(1)
    wednesday_portfolio = create_portfolio(2)
    thursday_portfolio = create_portfolio(3)
    friday_portfolio = create_portfolio(4)
    
    # Plot the cumulative returns for each portfolio
    fig, ax = plt.subplots()
    ax.plot(monday_portfolio.index, monday_portfolio['cum_return'], label='Monday')
    ax.plot(tuesday_portfolio.index, tuesday_portfolio['cum_return'], label='Tuesday')
    ax.plot(wednesday_portfolio.index, wednesday_portfolio['cum_return'], label='Wednesday')
    ax.plot(thursday_portfolio.index, thursday_portfolio['cum_return'], label='Thursday')
    ax.plot(friday_portfolio.index, friday_portfolio['cum_return'], label='Friday')
    ax.set_xlabel('Date')
    ax.set_ylabel('Cumulative Return')
    ax.set_title('Cumulative Returns by Day of the Week')
    ax.legend()
    plt.show()

if monthly_portfolio:
   
    '''The function to create the portfolio for monthly investing is not working properly'''
    
    # Create portfolios for each day of the month
    monday_last_portfolio = create_monthly_portfolio(0)
    tuesday_last_portfolio = create_monthly_portfolio(1)
    wednesday_last_portfolio = create_monthly_portfolio(2)
    thursday_last_portfolio = create_monthly_portfolio(3)
    friday_last_portfolio = create_monthly_portfolio(4)
    
    # Plot the cumulative returns for each portfolio
    fig, ax = plt.subplots()
    ax.plot(monday_last_portfolio.index, monday_last_portfolio['cum_return'], label='Monday (Last)')
    ax.plot(tuesday_last_portfolio.index, tuesday_last_portfolio['cum_return'], label='Tuesday (Last)')
    ax.plot(wednesday_last_portfolio.index, wednesday_last_portfolio['cum_return'], label='Wednesday (Last)')
    ax.plot(thursday_last_portfolio.index, thursday_last_portfolio['cum_return'], label='Thursday (Last)')
    ax.plot(friday_last_portfolio.index, friday_last_portfolio['cum_return'], label='Friday (Last)')
    ax.set_xlabel('Date')
    ax.set_ylabel('Cumulative Return')
    ax.set_title('Cumulative Returns by Last Day of the Month')
    ax.legend()
    plt.show()
