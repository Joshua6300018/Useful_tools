

# coding=UTF-8

import datetime
import urllib.request
import os 
import re
import pandas as pd
import sys

args = sys.argv
mode = args[1]
os.chdir(args[2])

#os.chdir("//10.220.9.146/fd/SHARE/USER/心誠/Taifex_Crawler/")
#os.getcwd()
filename = "Temp_data/PC_ratio_tmp.csv"

# %%
#### 取得一段時間內的data ####
def get_interval(datestart,dateend):
    ## 下載檔案
    #datestart = "2018/05/02"
    #dateend = "2018/05/27"
    
    para = '?queryStartDate=' + datestart + '&queryEndDate=' + dateend
    url = 'http://www.taifex.com.tw/cht/3/dlPcRatioDown' + para
    
    ## 下載-存檔
    urllib.request.urlretrieve(url,filename)
    
    ## 清理資料(轉為連續月)
    data = pd.read_csv(filename,encoding="cp950",header=0,usecols=[0,6],names=["Date","PC_ratio"]).sort_values(by=['Date'])
    
    return(data)

#get_interval(datestart,dateend)
get_interval("2018/05/02","2018/05/27")

# %%
#### 取得歷史的data ####
def history_data(datestart):
        
    # datestart = "2018/05/02"
    
    datestart = datetime.datetime.strptime(datestart,'%Y/%m/%d')
    datestart = datetime.date(datestart.year,datestart.month,datestart.day)
    dateend = datetime.date.today()
    tt_data = pd.DataFrame()
    
    lastDay = datestart #上一輪的起始日期
    cnt = 0    
    ## 上一次的最後日期還沒超過今日 -> 往下取20天
    while( lastDay <= dateend ):  
               
        start_num = datestart + datetime.timedelta(days=cnt)
        end_num = start_num + datetime.timedelta(days=20)
        lastDay = end_num
        
        start_num = start_num.strftime("%Y/%m/%d")
        end_num = end_num.strftime("%Y/%m/%d")
        
        print(start_num," -- ",end_num)
        cnt = cnt + 21
        tt_data = tt_data.append(get_interval(start_num,end_num))
        tt_data = tt_data.drop_duplicates()
        #time.sleep(0.5)
    
    # tt_data
    return(tt_data.sort_values(by=['Date']))


# history_data("2017/05/02")

#%%

# =============================================================================
# mode變依據傳入的參數決定
# 若第1個參數為"recent"  => 則只更新最近的資料
# 若第1個參數為"all"     => 則包含2015~至今的資料
# =============================================================================

if(mode == "recent"):
    startDate_Str = (datetime.date.today()+datetime.timedelta(-19)).strftime("%Y/%m/%d")
elif(mode=="all"):
    startDate_Str = "2015/01/01"

## 執行-爬蟲
tt_data = history_data(startDate_Str)

## 輸出檔案
currentFilename = "current_data/"+"PC_ratio.csv"
tt_data.to_csv(currentFilename,index=False,header=False)

print("  From Python: ","PC_ratio ~~ Completed\n")

## End















