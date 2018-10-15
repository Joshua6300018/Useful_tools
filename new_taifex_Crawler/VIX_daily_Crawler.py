# -*- coding: utf-8 -*-
import datetime
import urllib.request
import os
import pandas as pd


tt_data = pd.DataFrame()

#%%
# 前三個月的每日收盤VIX
urllib.request.urlretrieve("http://www.taifex.com.tw/file/taifex/Dailydownload/vix/log2data/201808new.txt","VIX_tmp.csv")

data = pd.read_csv("VIX_tmp.csv",encoding="cp950",sep='\t',usecols=[0,4],names=["Date","VIX"])
data["Date"] = data["Date"].apply( lambda x: str(x)[:4] + "/" + str(x)[4:6] + "/" + str(x)[6:] )

data


pd.read

#%%
# 最近一個月的每日收盤VIX


urllib.request.urlretrieve("http://www.taifex.com.tw/cht/7/getVixData?filesname=20181006","VIX_tmp.csv")

# 日期不存在會有錯







#%%






