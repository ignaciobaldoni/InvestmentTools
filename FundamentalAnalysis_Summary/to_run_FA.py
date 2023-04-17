# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 09:34:08 2022

@author: ignacio

This Python script defines several functions and a method to perform financial 
analysis on a list of stocks. Here is an overview of the functions:

inflation(df,obs_start): This function takes a DataFrame df and a date 
obs_start as inputs. It retrieves inflation data from the FRED database using 
the CPIAUCSL series and adjusts the values by multiplying them by 0.01. It then 
concatenates the inflation data with the Adj_Close column of the input DataFrame 
and drops the Adj_Close column. Finally, it renames the resulting column to 
Inflacion and returns the resulting DataFrame.

write_on_Excel(Result,A_considerar,File, Excel_on=True): This function takes 
three DataFrames (Result, A_considerar, and File) and a Boolean variable 
Excel_on as inputs. If Excel_on is True, the function writes the Result and 
A_considerar DataFrames to an Excel file with the filename specified in File. 
The function also formats the Excel file with tables and column widths.

Get_tickers(Nasdaq=[], Retail=[], Semis=[], Otros_SP500=[], Materials=[], 
Energia=[], Beach=[], Alemania=[], Arg=[], Particular=[], All_SP=False): 
This function takes several lists of tickers for different sectors as inputs 
(Nasdaq, Retail, Semis, Otros_SP500, Materials, Energia, Beach, Alemania, Arg, 
Particular) and a Boolean variable All_SP. Depending on the inputs, it generates 
a list of ticker symbols for stocks to analyze. If All_SP is True, it includes
all stocks in the S&P 500 in the list.

The script also imports the Fred class from the fredapi module and the pandas
module. It creates an instance of the Fred class with an API key, which is used 
in the inflation function.
"""

from fredapi import Fred    
import pandas as pd
fred = Fred(api_key='Get_your_own_FRED_api_key')

def inflation(df,obs_start):
    fed_inflacion  = fred.get_series('CPIAUCSL',observation_start=obs_start).mul(0.01) 
    inflacion = pd.concat([df['Adj_Close'],fed_inflacion],axis= 1).fillna(method='ffill')
    inflacion = inflacion.drop(['Adj_Close'],axis=1)
    inflacion.columns = ['Inflacion']
    return inflacion[1:]


def write_on_Excel(Result,A_considerar,File, Excel_on = True):
    if Excel_on:
        writer = pd.ExcelWriter(str(File)+'.xlsx', engine='xlsxwriter')
        workbook = writer.book
        
        if len(Result)>0:
            
            Result.to_excel(writer, sheet_name='Report', startrow=1, header=False,
                            index=False)    
            
            worksheet = writer.sheets['Report']    
            (max_row, max_col) = Result.shape   	# Dimensions of the dataframe.    
            column_settings = [{'header': column} for column in Result.columns]    
            worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings, 
                                                             'style': 'Table Style Medium 2'})
            worksheet.set_column(0,  max_col - 1, 15)
        
        if len(A_considerar)>0:
            
            A_considerar.to_excel(writer, sheet_name='To consider', startrow=1, header=False,
                            index=False)
            worksheet2 = writer.sheets['To consider']    
            (max_row, max_col) = A_considerar.shape   	# Dimensions of the dataframe.    
            column_settings = [{'header': column} for column in A_considerar.columns]    
            worksheet2.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings, 
                                                             'style': 'Table Style Medium 2'})    
            worksheet2.set_column(0,  max_col - 1, 15)
        
        writer.save()

def Get_tickers(Nasdaq=[],
                Retail=[],
                Semis=[],
                Otros_SP500=[],
                Materials=[],
                Energia=[],
                Beach=[],
                Alemania=[],
                Arg=[],
                Particular = [],
                All_SP=False):
    
    if Nasdaq!=[]: Nasdaq = ['AAPL','MSFT','META','ZM','GOOG','BNTX','GLOB','TSLA','PANW',
               'EA','ADBE','SONY','DELL']
    if Retail!=[]: Retail = ['ETSY','MELI','FTCH','AMZN']
    if Semis!=[]: Semis = ['AMD','MU','INTC','NVDA','ASML','SWKS']
    if Otros_SP500!=[]: Otros_SP500   = ['BRK-B','F','V','DIS','MA','GOLD','KO','DE',
                                   'BA','NKE','GM','UPS','SBUX','FDX','JNJ','MCD']     
    if Materials!=[]: Materials = ['SLI','ALB','CCJ']
    if Energia!=[]: Energia = ['UEC','ENPH','MRO','CTRA','AR','OXY','MPN']
    if Beach!=[]: Beach = ['RCL','IHG','ABNB','BKNG','UAL','DAL','LVS','NCLH']
    if Alemania!=[]: Alemania = ['LHA.DE','BMW.DE','ADS.DE','AIR.DE','NA9.DE']
    if Arg!=[]: Arg = ['YPF','PAM','GGAL','CEPU']
    
    
    Activos = Otros_SP500 + Nasdaq + Retail + Semis +\
                Energia + Materials + Beach +\
                Alemania + Arg + Particular
                

    
    if All_SP:
        # get the full stock list of S&P 500 
        payload=pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
        stock_list = payload[0]['Symbol'].values.tolist()
        Stock_SP500 = [i.replace(".", "-") for i in stock_list]
    
        Nasdaq  = ['MELI','ZM','BNTX','GLOB','SONY','DELL','ASML']    
        Energia = ['SLI','UEC','CCJ','AR']
        Beach = ['IHG','ABNB']
        Alemania = ['LHA.DE','BMW.DE','ADS.DE','AIR.DE','NA9.DE']
        Arg = ['YPF','PAM','GGAL','CEPU']
        Activos = Nasdaq + Energia + Beach + Alemania + Stock_SP500 +  Arg + Particular
                
    columns_list = ['Ticker','Name','Price','Mean Target','52 week high','MACD',
                    'ReturnOnEquity','DebtToEquity','CurrentRatio',
                    'P/S (Tr.12)','P/B','Profit margin','Free Cash Flow (B)',
                    'Volume (M)','Shorted (%)','Sector','Industry'] # PEG Tr.12
    
    return Activos, columns_list
    
    