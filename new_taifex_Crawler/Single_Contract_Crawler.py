# coding=UTF-8

import datetime
import urllib.request
import os 
import sys
import re
import pandas as pd
import gc
import time

args = sys.argv
id = args[1]
os.chdir(args[2])

#id = "TX"
#os.chdir("//10.220.9.146/fd/SHARE/USER/心誠/Taifex_Crawler/")
#os.getcwd()
filename = "Temp_data/"+id+"_tmp.csv"

# %%
#### 取得一段時間內的data ####
def get_interval(datestart,dateend,id):
    ## 下載檔案
    #datestart = "2018/05/02"
    #dateend = "2018/05/27"
    
    para = '?queryStartDate='+datestart+'&queryEndDate='+dateend+'&commodity_id='+id + '&down_type=1'
    url = 'http://www.taifex.com.tw/cht/3/dlFutDataDown' + para
    
    ## --- 先查一次
    urllib.request.urlretrieve(url,filename)
    # 下載失敗的時候只能用utf-8讀,下載成功時只能用cp950讀
    try:
        with open(filename,'r',encoding='cp950') as file:
            content = file.read()
    except:
        with open(filename,'r',encoding='utf8') as file:
            content = file.read()
    
    ## --- 若查尋失敗 --> 持續查直到查詢成功
    while(len(re.findall("<!DOCTYPE",content)) >= 1):
        urllib.request.urlretrieve(url,filename)
        # 下載失敗的時候只能用utf-8讀,下載成功時只能用cp950讀
        try:
            with open(filename,'r',encoding='cp950') as file:
                content = file.read()
        except:
            with open(filename,'r',encoding='utf8') as file:
                content = file.read()
        time.sleep(0.5)
    
    ## 清理資料(轉為連續月)
    data = pd.read_csv(filename,encoding="cp950",header=0,usecols=[0,1,2,11],names=["Date","contract","expiration","OI"])
    data = data[data.OI != "-"]
        
    wm = [str(len(row['expiration'].strip(' '))).replace('8','W').replace('6','') for index, row in data.iterrows()]
    rk = data.groupby(['Date',wm])['expiration'].apply(lambda x: x.rank()).astype(int).astype(str)
    contin_contract = data.contract.add(wm).add(rk)
    
    fn_data = pd.concat([data['Date'],contin_contract,data['OI']],axis=1)
    fn_data.columns = ['Date','contract','OI']
    fn_data['OI'] = fn_data['OI'].astype(int)
    return(fn_data)

#get_interval(datestart,dateend,id)
#get_interval("2018/05/02","2018/05/27",id)

# %%
#### 更新最近的data ####

def update_recent(id):    
    ## 設定下載參數
    datestart=(datetime.datetime.now()-datetime.timedelta(days=20)).strftime("%Y/%m/%d")  #20天前
    dateend=datetime.datetime.now().strftime("%Y/%m/%d")  #今天
    ## 下載近期資料
    fn_data = get_interval(datestart,dateend,id)
    
    ## 依到期合約分成不同變數
    TX1 = fn_data[fn_data['contract'].isin([id+"1",id+"W1",id+"W2"])].groupby(['Date'])['OI'].agg(sum).reset_index()[['Date','OI']].sort_values(['Date']) # 把週小台期貨加到近月期貨上
    TX1['Date'] = pd.to_datetime(TX1.Date)
    TX1.sort_values(by=['Date'],inplace=True)
    TX1['Date'] = TX1.Date.dt.strftime('%Y/%m/%d')
    TX2 = fn_data[fn_data['contract']==id+"2"][['Date','OI']]
    TX3 = fn_data[fn_data['contract']==id+"3"][['Date','OI']]
    TX4 = fn_data[fn_data['contract']==id+"4"][['Date','OI']]
    TX5 = fn_data[fn_data['contract']==id+"5"][['Date','OI']]
    
    ## 讀取歷史資料
    try:
        if( os.path.isfile("current_data/"+id+"1.csv")):
            TX1_past = pd.read_csv("current_data/"+id+"1.csv",names=["Date","OI"])
            TX2_past = pd.read_csv("current_data/"+id+"2.csv",names=["Date","OI"])
            TX3_past = pd.read_csv("current_data/"+id+"3.csv",names=["Date","OI"])
            TX4_past = pd.read_csv("current_data/"+id+"4.csv",names=["Date","OI"])
            TX5_past = pd.read_csv("current_data/"+id+"5.csv",names=["Date","OI"])
            ## 合併歷史資料與新資料 + distinct
            TX1 = TX1_past.append(TX1).drop_duplicates()
            TX2 = TX2_past.append(TX2).drop_duplicates()
            TX3 = TX3_past.append(TX3).drop_duplicates()
            TX4 = TX4_past.append(TX4).drop_duplicates()
            TX5 = TX5_past.append(TX5).drop_duplicates()
    except:    
        print("Error")
    
    ## 輸出檔案
    TX1.to_csv("current_data/"+id+"1.csv",index=False,header=False)
    TX2.to_csv("current_data/"+id+"2.csv",index=False,header=False)
    TX3.to_csv("current_data/"+id+"3.csv",index=False,header=False)
    TX4.to_csv("current_data/"+id+"4.csv",index=False,header=False)
    TX5.to_csv("current_data/"+id+"5.csv",index=False,header=False)
    ## End

#update_recent("TX")

# %%
#### 取得歷史的data ####
def history_data(id):
      
    ## 分成兩部分: 1.過去的年資料 2.今年1/1到現在的資料
    ## 分別合併到 tt_data中
    tt_data = pd.DataFrame()
    
    ## -------------   1.取年資料   ---------------
    ## 取出指定年資料的檔名
    fl = [x for x in os.listdir("Temp_data/") if '_fut.csv' in x]
    
    ## 逐個檔整理+合併
    for i in fl:
        #i=fl[0]
        his_year = int( i[:4])
        print(his_year,"\n")
        ## 清理資料(轉為連續月)
        data = pd.read_csv("Temp_data/"+i,encoding="cp950",header=0,usecols=[0,1,2,11],names=["Date","contract","expiration","OI"])
        data = data[data.OI != "-"]
        data = data[data.contract == id]
        
        wm = [str(len(row['expiration'])).replace('8','W').replace('6','') for index, row in data.iterrows()]
        rk = data.groupby(['Date',wm])['expiration'].apply(lambda x: x.rank()).astype(int).astype(str)
        contin_contract = data.contract.add(wm).add(rk)
        
        fn_data = pd.concat([data['Date'],contin_contract,data['OI']],axis=1)
        fn_data.columns = ['Date','contract','OI']
        fn_data['OI'] = fn_data['OI'].astype(int)
        tt_data = tt_data.append(fn_data)
        gc.collect()
    
    
    ## ------------ 2.取得當年度之前的資料 ----------
    print("Get current year(",datetime.datetime.now().year,") data\n")
    lastDay = datetime.datetime(datetime.date.today().year,1,1)
    cnt = 0
    ## 上一次的最後日期還沒超過今日 -> 往下取20天
    while( lastDay <= datetime.datetime.today() ):  
        
        now = datetime.datetime.now()
        start_num = datetime.datetime.strptime(str(now.year)+"/01/01","%Y/%m/%d")+datetime.timedelta(days=cnt)
        end_num = start_num + datetime.timedelta(days=20)
        lastDay = end_num
        start_num = start_num.strftime("%Y/%m/%d")
        end_num = end_num.strftime("%Y/%m/%d")
        
        print(start_num," -- ",end_num)
        cnt = cnt + 21
        tt_data = tt_data.append(get_interval(start_num,end_num,id))
        time.sleep(0.5)
    
    ## 依到期合約分成不同變數
    TX1 = tt_data[tt_data['contract'].isin([id+"1",id+"W1",id+"W2"])].groupby(['Date'])['OI'].agg(sum).reset_index()[['Date','OI']] # 把週小台期貨加到近月期貨上
    TX1['Date'] = pd.to_datetime(TX1.Date)
    TX1.sort_values(by=['Date'],inplace=True)
    TX1['Date'] = TX1.Date.dt.strftime('%Y/%m/%d')
    TX2 = tt_data[tt_data['contract']==id+"2"][['Date','OI']]
    TX3 = tt_data[tt_data['contract']==id+"3"][['Date','OI']]
    TX4 = tt_data[tt_data['contract']==id+"4"][['Date','OI']]
    TX5 = tt_data[tt_data['contract']==id+"5"][['Date','OI']]
    ## 輸出檔案
    TX1.to_csv("current_data/"+id+"1.csv",index=False,header=False)
    TX2.to_csv("current_data/"+id+"2.csv",index=False,header=False)
    TX3.to_csv("current_data/"+id+"3.csv",index=False,header=False)
    TX4.to_csv("current_data/"+id+"4.csv",index=False,header=False)
    TX5.to_csv("current_data/"+id+"5.csv",index=False,header=False)
    ## End


# %%

#history_data("TX")
#get_interval("2018/05/02","2018/05/27",id)

# =============================================================================
# mode變依據傳入的第三個參數決定
# 若無第三個參數      => 則只更新最近的資料
# 若第三個參數為"all" => 則包含年度歷史資料一併更新
# =============================================================================

mode = "recent"
if(len(args)==4):
    if(args[3]=="all"):
        mode = "history"

# print(args)
# print(len(args))

if(mode == "recent"):
    update_recent(id)
    print("  From Python: ",id," Total_OI ~~ Completed\n")
elif(mode=="history"):
    history_data(id)
    update_recent(id)
    print("  From Python: ",id," Total_OI ~~ Completed\n")

# update_recent("TX")
# history_data("MTX")

## End



