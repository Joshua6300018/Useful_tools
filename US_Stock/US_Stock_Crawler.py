# -*- coding: utf-8 -*-
"""
Created on Fri Aug 18 08:45:49 2023

@author: vtteam
"""

import pandas as pd 
import numpy as np
import pyodbc
import warnings
from datetime import datetime
from datetime import date
from pandas.tseries.offsets import BDay
import os
import requests
import random
import time
 
delay_list = [0.1, 0.2,0.3]  #延遲的秒數選項

print("[US_Stock Crawler]")
os.getcwd()
os.chdir("\\\\10.220.9.146\\fd\\SHARE\\USER\\心誠\\8. STF組\\US_Stock")


#%%
stock_list = pd.read_csv("nasdaq_screener.csv")
stock_list = stock_list.dropna()
stock_list = stock_list[stock_list['Market Cap']!=0]
stock_list['Symbol'] = [e.replace(" ","") for e in stock_list['Symbol']]
pid_list = stock_list['Symbol'].tolist()

#%%

data_df = pd.DataFrame()
err_list = []
start_time = time.time()
for pid in pid_list:
    #pid = 'ACONW'
    time.sleep(random.choice(delay_list) ) #故意延遲
    try:
        url = "https://finviz.com/quote.ashx?t="+pid+"&ty=c&ta=1&p=m"
        header = {
          "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
          "X-Requested-With": "XMLHttpRequest"
        }
        
        data = pd.read_html(requests.get(url, headers=header).text)
        if len(data)<7:
            err_list.append(pid)
            continue
        data = data[6]
    except:
        err_list.append(pid)
        
    data_dic = {}
    data_dic['Pid'] = pid
    data_dic['Date'] = (date.today()-BDay(1)).strftime("%Y%m%d")
    for i1 in range(0,data.shape[0]-1):
        for i2 in range(0,data.shape[1]-1):    
            if(i1%2==0):
                data_dic[data.iloc[i2,i1]]=data.iloc[i2,i1+1]
    
    data_df = data_df.append(pd.DataFrame(data_dic,index=[0]))
    print(data_df.shape[0])
    print(pd.DataFrame(data_dic,index=[0]))
    
print("執行時間：%f 秒" % (time.time() - start_time))
err_list
data_df

#%%
pd.DataFrame(err_list).to_csv("err_list.csv",index=False,header=False)
data_df.to_csv( "US_stock_" + (date.today()-BDay(1)).strftime("%Y%m%d") + ".csv",index=False )


#%%
import matplotlib.pyplot as plt
data_df = pd.read_csv("US_stock_" + (date.today()-BDay(1)).strftime("%Y%m%d") + ".csv")
data_df

# data-clean
data_df = data_df[data_df["Forward P/E"]!='-']
data_df = data_df[data_df["PEG"]!='-']
data_df = data_df[data_df["ROE"]!='-']
data_df = data_df[data_df["Market Cap"]!='-']
data_df = data_df[data_df["Gross Margin"]!='-']
data_df = data_df[data_df["Profit Margin"]!='-']
data_df = data_df[data_df["EPS next 5Y"]!='-']

data_df["Forward P/E"] = [ float(e) for e in data_df["Forward P/E"]]
data_df["PEG"] = [ float(e) for e in data_df["PEG"]]
data_df["ROE"] = [ float(e.replace("%","")) for e in data_df["ROE"]]
data_df["Gross Margin"] = [ float(e.replace("%","")) for e in data_df["Gross Margin"]]
data_df["Profit Margin"] = [ float(e.replace("%","")) for e in data_df["Profit Margin"]]
data_df["EPS next 5Y"] = [ float(e.replace("%","")) for e in data_df["EPS next 5Y"]]

# filter
data_df = data_df[data_df["ROE"]>10]
data_df = data_df[ (data_df["Forward P/E"]>0) & (data_df["Forward P/E"]<20)]
data_df = data_df[ (data_df["PEG"]>0) & (data_df["PEG"]<2)]
data_df = data_df[data_df["Gross Margin"]>20]
data_df = data_df[data_df["Profit Margin"]>10]
data_df = data_df[data_df["EPS next 5Y"]>10]
print(data_df.shape[0])

def plot_scatter(x,y,pid):
    fig, ax = plt.subplots()
    ax.set_title(x.name + ' vs '+y.name )
    ax.set_xlabel(x.name)
    ax.set_ylabel(y.name)
    x = x.tolist()
    y = y.tolist()
    pid = pid.tolist()
    ax.scatter(x, y)
    for i, txt in enumerate(pid):
        ax.annotate(txt, (x[i], y[i]))

#%%
pid = data_df["Pid"]
ROE = data_df["ROE"]
Fwd_PE = data_df["Forward P/E"]
PEG = data_df["PEG"]

plot_scatter(ROE,Fwd_PE,pid)
plot_scatter(ROE,PEG,pid)
















