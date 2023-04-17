# -*- coding: utf-8 -*-
"""
Created on Wed Oct  5 08:59:00 2022
@author: ignacio


The script defines a function called overall_analysis, which takes three 
parameters: Activos (a list of assets), columns_list (a list of column names 
for the resulting dataframe), and Print_results (a boolean to determine if the 
resulting dataframe should be printed).

The function first creates an empty dataframe called resultado using the 
specified columns_list. Then, it iterates over each asset in Activos and 
performs a series of actions.

For each asset, it attempts to download data using the yfinance library, 
renames a column in the resulting dataframe, and extracts various pieces of 
information (such as the asset name, sector, and price) from the yfinance 
Ticker object. It also calculates the MACD and computes some fundamental ratios, 
such as price-to-book and debt-to-equity.

If the asset meets certain criteria (such as a high profit margin and positive 
free cash flow), it is added to a separate dataframe called A_considerar (tbc)

Finally, the function returns two dataframes: resultado (which contains all the
assets) and A_considerar (which contains only the assets that meet the specified 
criteria). If Print_results is True, the function also prints resultado.

Currently, there are some problems with the yfinance library for importing the 
fundamentals for every company data.

"""

import yfinance as yf
import pandas as pd
    
def overall_analysis(Activos, columns_list,Print_results=False):    
    
    resultado = pd.DataFrame(columns=columns_list) 
    A_considerar = resultado     
    
    for Activo in Activos:
        print(Activo)
        
        year_high = target = PB = PS_12 = freeCashFlow = profit_margin = None
        currentRatio = debtToEquity = returnOnEquity = pct_shorted = None         
        
        # try:
        data = yf.download(Activo,start='2019-09-26')
        data.rename(columns={'Adj Close':'Adj_Close'}, inplace=True) 
                    
        # obs_start = datetime.strftime(data.index[0],'%Y-%m-%d')
        
        name = yf.Ticker(Activo).info.keys()
        print(name)
        Name = name['shortName']
        industry = name['industry']
        sector = name['sector']
        Price = data.Adj_Close.iloc[-1]
        volume = data.Volume.iloc[-1]*1e-6
                
        if (name['sharesShort'] != None and name['floatShares'] != None):
            pct_shorted = (name['sharesShort']/name['floatShares'])*100
        
        if name['fiftyTwoWeekHigh'] != None: year_high = name['fiftyTwoWeekHigh']
        if name['targetMeanPrice'] != None: target = name['targetMeanPrice']
        # if name['targetMeanPrice'] != None: target = name['targetMeanPrice']
        # if name['beta'] != None: beta = name['beta']        
               
        ### ----------- MACD ----------- ###   
        data['ema12'] = data.Adj_Close.ewm(span=12, adjust=False).mean()
        data['ema26'] = data.Adj_Close.ewm(span=26, adjust=False).mean()
        data['MACD'] = (data.ema12 - data.ema26)/data.ema12
        MACD = data.MACD.iloc[-1]      
        
        ### ----------- Some fundamentals ----------- ###      
        
        if name['priceToBook'] != None: PB = name['priceToBook']   
        if name['priceToSalesTrailing12Months'] != None: PS_12 = name['priceToSalesTrailing12Months']         
        # if name['trailingPegRatio'] != None: PEG = name['trailingPegRatio']        
        if name['freeCashflow'] != None: freeCashFlow = name['freeCashflow']*1e-9
        if name['profitMargins'] != None: profit_margin = name['profitMargins']*100        
        if name['currentRatio'] != None: currentRatio = name['currentRatio']
        if name['debtToEquity'] != None: debtToEquity = name['debtToEquity']
        if name['returnOnEquity'] != None: returnOnEquity = name['returnOnEquity']

        ### -------- inflacion  -------- ### 
        # Inflacion = inflation(data,obs_start)
        
        # data['Real_Price'] = data['Adj_Close']/Inflacion['Inflacion']
        # data.Real_Price.plot()
        
        # For google sheets 
        if ".DE" in Activo:
            Activo = Activo[:-3]
            if ("AIR" in Activo) or ("ADS" in Activo):
                Activo = "FRA:"+Activo
        if '-' in Activo:
            Activo = Activo.replace("-", ".") 
            print(Activo)
            
        df2 = pd.DataFrame([[Activo,Name,Price, target, year_high, MACD,
                              returnOnEquity, debtToEquity, currentRatio,
                              PS_12, PB, profit_margin, freeCashFlow,
                              volume, pct_shorted,sector,industry]],
                            columns=list(resultado))
        
        resultado = resultado.append(df2)
        
        if (profit_margin > 17 and
            freeCashFlow > 0 and
            (0.8 <= currentRatio <= 3.5) and
            PB < 10 and
            debtToEquity < 50 and
            returnOnEquity>0.15) :  A_considerar = A_considerar.append(df2)
        # except:
            # print('Something is wrong with %s' %Activo)
    
    if Print_results: print(resultado)
    return resultado, A_considerar