# coding=UTF-8

# id = "MTX"
# setwd("C:/Users/90813/Desktop/OI_Crawler/")


id = "TX"
os.chdir("//10.220.9.146/fd/SHARE/USER/心誠/Taifex_Crawler-master/Python_ver")
filename = "Temp_data/"+id+"_tmp.csv"


#### 取得一段時間內的data ####

## 下載檔案
  # datestart = "2018/01/22"
  # dateend = "2018/02/11"
  
download.file(paste0('http://www.taifex.com.tw/chinese/3/3_1_2dl.asp?datestart=',datestart,'&dateend=',dateend,'&COMMODITY_ID=',id),
                paste0("Temp_data/",id,"_tmp.csv"),mode="wb",quiet=T)
  
## 清理資料(轉為連續月)
data = read.csv(paste0("Temp_data/",id,"_tmp.csv"),stringsAsFactors=FALSE)[,c(1,2,3,12)] %>% 
         .[which(.[,4]!="-"),] %>% 
         `colnames<-`(c("Date","contract","expiration","OI"))
  
gb_data = group_by(.data=data,Date,len = nchar(expiration)) %>% mutate( FM = order(expiration) )
gb_data = cbind(gb_data, wm = gsub(8,"W",gb_data$len) %>% gsub(6,"",.))
fn_data = cbind.data.frame(date = gb_data$Date, contract = paste0(gb_data$contract,gb_data$wm,gb_data$FM),OI = as.numeric(gb_data$OI))
fn_data[1:10,]
  
  return(fn_data)





