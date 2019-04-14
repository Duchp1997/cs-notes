cd /d %userprofile%\AppData\Local\Microsoft\Windows\Explorer
taskkill /f /im explorer.exe
attrib -h thumbcache_*.db
del thumbcache_*.db /a
start explorer
pause