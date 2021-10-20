call nssm.exe install wr_rtm_dem_dash "%cd%\run_server.bat"
rem call nssm.exe edit wr_rtm_dem_dash
call nssm.exe set wr_rtm_dem_dash AppStdout "%cd%\logs\wr_rtm_dem_dash.log"
call nssm.exe set wr_rtm_dem_dash AppStderr "%cd%\logs\wr_rtm_dem_dash.log"
nssm set wr_rtm_dem_dash AppRotateFiles 1
nssm set wr_rtm_dem_dash AppRotateOnline 1
nssm set wr_rtm_dem_dash AppRotateSeconds 86400
nssm set wr_rtm_dem_dash AppRotateBytes 104857600
call sc start wr_rtm_dem_dash