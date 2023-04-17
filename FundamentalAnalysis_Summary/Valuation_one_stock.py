# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 11:50:35 2022

@author: ignacio
"""
import warnings
warnings.filterwarnings('ignore')

import valinvest
stock = valinvest.Fundamental('META', 'Here_comes_your_own_API')
print(stock.fscore())