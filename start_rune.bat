@echo off
cd  %~dp0
python app.py --device cpu --save 0  --port 5003 --model final