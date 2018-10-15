@ECHO OFF

ECHO Start

::取得批次檔所在的路徑上一層
SET BatchPATH=%~DP0
SET CompilerPath="C:\ProgramData\Anaconda3\python"

ECHO #######  載入當天資料 #######

::PC_ratio
ECHO Put-Call ratio...
%CompilerPath% %BatchPATH%\scripts\py_version\PC_ratio_Crawler.py recent %BatchPATH% 
REM %CompilerPath% %BatchPATH%\scripts\py_version\PC_ratio_Crawler.py all %BatchPATH% 

::三大法人
REM ECHO 大小台(三大法人)...
REM %CompilerPath% %BatchPATH%\scripts\py_version\Big3_Crawler.py TXF %BatchPATH%
REM %CompilerPath% %BatchPATH%\scripts\py_version\Big3_Crawler.py MXF %BatchPATH%

::完整契約資訊(依到期月分開)
REM ECHO 大小台(總OI)
REM %CompilerPath% %BatchPATH%\scripts\py_version\Single_Contract_Crawler.py TX %BatchPATH%
REM %CompilerPath% %BatchPATH%\scripts\py_version\Single_Contract_Crawler.py MTX %BatchPATH%

REM ::全部更新時要開下方
REM %CompilerPath% %BatchPATH%\scripts\py_version\Single_Contract_Crawler.py TX %BatchPATH% all
REM %CompilerPath% %BatchPATH%\scripts\py_version\Single_Contract_Crawler.py MTX %BatchPATH% all

REM ECHO #######  合併歷史資料與新資料 #######

::合併三大法人...
::for /f %%i in ('%CompilerPath% %BatchPATH%mergeBig3.r %BatchPATH%') do set Big3=%%i
::if %Big3% == success_yesToday(Big3) ECHO ^  Merge Big3 Completed @@@~~~
::if %Big3% == success_noToday(Big3) ECHO ^  No today @@@~~~

::合併全部新舊資料
REM for /f %%i in ('%CompilerPath% %BatchPATH%\scripts\py_version\mergeAll.py %BatchPATH%') do set All=%%i
REM if %All% == success_yesToday(All) ECHO ^  Merge All Completed @@@~~~
REM if %All% == success_noToday(All) ECHO ^  No today @@@~~~

REM ECHO #######  檢查資料是否正確 + 輸出log #######

::設定當天日期
REM SET DT=%DATE% %TIME% 

REM ECHO %DT%  %Big3% >> log\log.txt
REM ECHO %DT%  %All% >> log\log.txt

	
ECHO Finish

pause