set ORIG=%cd%

cd "C:\Program Files\mosquitto"
START "mosq" "mosquitto.exe" "-p 1883"

if not exist "C:\mongo" mkdir "C:\mongo"
if not exist "C:\mongo\netSens" mkdir "C:\mongo\netSens"

cd "C:\Program Files\MongoDB\Server\3.6\bin"
START "mongodb" "mongod.exe" --dbpath C:\mongo\netSens


cd %ORIG%
cd "..\app\web"
START "web" "python" "web.py"

cd %ORIG%
cd "..\app\playback"
START "playback" "python" "playback.py"

cd %ORIG%
cd "..\app\networker"
START "networker" "python" "networker.py"

cd %ORIG%
cd "..\app\monitor"
START "monitor" "python" "monitor.py"

