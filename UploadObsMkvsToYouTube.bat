::
:: UploadObsMkvsToYouTube.bat
:: 
:: Author: Vincent Kocks (engineering@vingenuity.net)
:: v1.0.0 - 2020-08-10
::
:: Converts and uploads MKV video recordings to YouTube.
:: Currently, only the conversion stage of the pipeline is implemented.
::
@echo off

:: Static Environment Variables
set CONVERTED_DIRECTORY=C:\MP4
set FFMPEG_EXE_PATH=%~dp0\ffmpeg\bin\ffmpeg.exe
set INPUT_DIRECTORY=C:\MKV
set INPUT_SUFFIX=.mkv
set VIDEO_SERVICE=youtube


:: Main Execution
py -3 .\upload_obs_recording_to_service.py --video-service "%VIDEO_SERVICE%" --input-directory "%INPUT_DIRECTORY%" --input-suffix "%INPUT_SUFFIX%" --converted-directory "%CONVERTED_DIRECTORY%" --ffmpeg-exe "%FFMPEG_EXE_PATH%"

pause
