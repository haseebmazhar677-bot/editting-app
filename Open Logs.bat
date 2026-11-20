@echo off
rem Opens the folder with Video Transformer's log files (app.log) in File Explorer.
if not exist "%LOCALAPPDATA%\VideoTransformer\logs" mkdir "%LOCALAPPDATA%\VideoTransformer\logs"
explorer "%LOCALAPPDATA%\VideoTransformer\logs"
