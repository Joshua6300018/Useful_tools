# coding=UTF-8

import datetime
import urllib.request
import os 
import re
import pandas as pd
import sys

args = sys.argv
id = args[1]
os.chdir(args[2])

#id = "TXF"
#os.chdir("//10.220.9.146/fd/SHARE/USER/心誠/Taifex_Crawler/")
#os.getcwd()
filename = "Temp_data/"+id+"_Big3OI_tmp.csv"

#%%
## 下載三大法人未平倉檔案
i=0
while(not os.path.isfile(filename) or i==0):
    
    # 設定日期參數
    ED = datetime.datetime.now()  #End day
    SD = ED - datetime.timedelta(days=365*3)  #Start day
    ED = ED - datetime.timedelta(days=i)  #new end day
    
    SD_str = SD.strftime(format="%Y/%m/%d")
    ED_str = ED.strftime(format="%Y/%m/%d")
    
#    SYear = str(SD.year)
#    SMonth = str(SD.month)
#    SDay = str(SD.day)
#    EYear = str(ED.year)
#    EMonth = str(ED.month)
#    EDay = str(ED.day)
    #print(SD,ED)
    
    # 下載檔案
    para = "?queryStartDate=" + SD_str + "&queryEndDate=" + ED_str + "&commodityId=" + id
    url = 'http://www.taifex.com.tw/cht/3/dlFutContractsDateDown'+para
    
#    http://www.taifex.com.tw/cht/3/dlTotalTableDateDown?queryStartDate=2018/10/01&queryEndDate=2018/10/09
    
    urllib.request.urlretrieve(url,filename)
    
    # 下載失敗的時候只能用utf-8讀,下載成功時只能用cp950讀
    try:
        with open(filename,'r',encoding='cp950') as file:
            content = file.read()
    except:
        with open(filename,'r',encoding='utf8') as file:
            content = file.read()
    
    # 若判斷下載失敗-->移除檔案        
    if( len(re.findall("</html>",content)) >= 1):
        os.remove(filename)
    
    # 遞增回扣天數
    i = i +1
    if(i>15):
        print("File URL error!!! please check ~~ ")
        #exit() #跳出腳本
        
print("Load data finished~~~")

#%%
## 把檔案拆成 {外資、自營、投信}
data = pd.read_csv(filename,encoding="cp950",header=0,usecols=[0,2,13],names=["Date","side","OI"])
#data.head()
Foreign = pd.DataFrame([row for index, row in data.iterrows() if len(row['side'])==5])
Dealer = pd.DataFrame([row for index, row in data.iterrows() if len(row['side'])==3])
InvestTrust = pd.DataFrame([row for index, row in data.iterrows() if len(row['side'])==2])

## 輸出檔案
currentFilename = "current_data/" + id
Foreign[["Date","OI"]].to_csv(currentFilename + "_Foreign.csv",index=False,header=False)      
Dealer[["Date","OI"]].to_csv(currentFilename + "_Dealer.csv",index=False,header=False)
InvestTrust[["Date","OI"]].to_csv(currentFilename + "_InvestTrust.csv",index=False,header=False)

print("  From Python: ",id," Big3_OI ~~ Completed\n")

## End


