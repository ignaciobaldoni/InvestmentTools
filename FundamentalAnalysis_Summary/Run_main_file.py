# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 10:08:28 2022

@author: ignacio

This Python script imports two functions from two different modules 
(to_run_FA.py and Fundamentals_summary.py), and uses them to perform data 
analysis and save the results in an Excel file.

Get_tickers(), takes a series of lists of symbols as arguments and returns a 
pandas dataframe containing financial data for those stocks. The lists 
correspond to different sectors, and the script allows for selecting tickers 
from specific sectors by uncommenting and editing the appropriate lines of code.

overall_analysis(), takes the pandas dataframe returned by Get_tickers() and
some additional arguments and returns a dictionary containing various financial 
ratios and other metrics calculated for each ticker, as well as a list of which
ratios are considered most important. There's an option to print the results.

write_on_Excel() function from to_run_FA.py, takes the dictionary and list of 
important ratios returned by overall_analysis() and saves them in an Excel file 
with the specified name.
"""

from to_run_FA import write_on_Excel, Get_tickers
from Fundamentals_summary import overall_analysis
    
#### -----------  Select the tickers -----------####

## Check to_run_FA.py to understand which companies you want to check. 
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
Particular  = ['NA9.DE']
            

#### ----------- Run all the code -----------####

Activos,columns_list = Get_tickers(Nasdaq , Retail , 
                                   Semis , Otros_SP500 , 
                                   Materials, Energia , 
                                   Beach, Alemania, Arg, Particular, 
                                   All_SP = All_SP500)

Result, A_considerar = overall_analysis(Activos,columns_list,Print_results=(True))


#### ----------- Save to excel with filters -----------####  
Excel_on = True

File = 'Overall_result'

write_on_Excel(Result,A_considerar,File,Excel_on)