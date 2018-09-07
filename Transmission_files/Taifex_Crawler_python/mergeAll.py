# coding=UTF-8

import datetime
import os
import pandas as pd

## 確認要合併的檔名
fl = list(set(os.listdir("current_data/")).intersection(set(os.listdir("history_data/"))))

## 逐檔合併
errMsg = ""
for fname in fl:
    # fname = fl[2]
    NewData = pd.read_csv("current_data/"+fname,header=None,names=["date","OI"])
    data = pd.read_csv("history_data/"+fname,header=None,names=["date","OI"])
    
    # 合併後去除重複值和OI為0的值
    combData = data.append(NewData).drop_duplicates()
    combData = combData[combData.OI != 0]
    
    # 查看有無當天資料
    if( datetime.datetime.now().date() == datetime.datetime.strptime(combData.date.iloc[-1],"%Y/%m/%d").date() ):
        if( combData.OI.iloc[-1]!=0 ):
            haveToday = 1
        else:
            haveToday = 0
    else:
        haveToday = 0    
    
    # 看看新舊資料有沒有同一天不同值的錯誤
    combData
    different_data = (combData.groupby(['date'],as_index=False).count().OI != 1).all() #全部日期count的次數皆為1-->正確
    different_data
    
    # 確認無錯誤值 => 寫csv檔
    if( different_data==0 and haveToday==1 ):
        combData.to_csv("history_data/"+fname,index=False,header=False)
        print(fname," ","success_yesToday(All)\n")
        errMsg = "success_yesToday(All)\n"
    elif( different_data==0 and haveToday==0 ):
        combData.to_csv("history_data/"+fname,index=False,header=False)
        print(fname," ","success_noToday(All)\n")
        errMsg = "success_noToday(All)\n"
    else:
        #有錯誤的話 => 顯示出錯誤的日期 
        dateCount = combData.groupby(['date'],as_index=False).count()
        wrongD = dateCount.loc[dateCount['OI']==0].date.astype(str)
        print( "There have same wrong data in " + wrongD + "in" + fname + "\n" )
        print( "error(All)" + fname + "\n" )
        errMsg = "error(All)" + fname + "\n"


print(errMsg);













