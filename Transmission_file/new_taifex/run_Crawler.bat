@ECHO OFF

ECHO Start

::���o�妸�ɩҦb�����|�W�@�h
SET BatchPATH=%~DP0
SET CompilerPath="C:\ProgramData\Anaconda3\python"

ECHO #######  ���J���Ѹ�� #######

::���㫴����T(�̨������})
ECHO �j�p�x(�`OI)
%CompilerPath% %BatchPATH%\scripts\py_version\Single_Contract_Crawler.py TX %BatchPATH%
%CompilerPath% %BatchPATH%\scripts\py_version\Single_Contract_Crawler.py MTX %BatchPATH%

::������s�ɭn�}�U��
REM %CompilerPath% %BatchPATH%\scripts\py_version\Single_Contract_Crawler.py TX %BatchPATH% all
REM %CompilerPath% %BatchPATH%\scripts\py_version\Single_Contract_Crawler.py MTX %BatchPATH% all

::�T�j�k�H
ECHO �j�p�x(�T�j�k�H)...
%CompilerPath% %BatchPATH%\scripts\py_version\Big3_Crawler.py TXF %BatchPATH%
%CompilerPath% %BatchPATH%\scripts\py_version\Big3_Crawler.py MXF %BatchPATH% 

ECHO #######  �X�־��v��ƻP�s��� #######

::�X�֤T�j�k�H...
::for /f %%i in ('%CompilerPath% %BatchPATH%mergeBig3.r %BatchPATH%') do set Big3=%%i
::if %Big3% == success_yesToday(Big3) ECHO ^  Merge Big3 Completed @@@~~~
::if %Big3% == success_noToday(Big3) ECHO ^  No today @@@~~~

::�X�֥����s�¸��
for /f %%i in ('%CompilerPath% %BatchPATH%\scripts\py_version\mergeAll.py %BatchPATH%') do set All=%%i
if %All% == success_yesToday(All) ECHO ^  Merge All Completed @@@~~~
if %All% == success_noToday(All) ECHO ^  No today @@@~~~

ECHO #######  �ˬd��ƬO�_���T + ��Xlog #######

REM ::�]�w���Ѥ��
SET DT=%DATE% %TIME% 

ECHO %DT%  %Big3% >> log\log.txt
ECHO %DT%  %All% >> log\log.txt

	
ECHO Finish

::pause