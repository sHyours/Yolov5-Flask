@echo off
cd  %~dp0
python app.py --device cpu --save 0 --port 5004 --model checker --thres 0.7 --log 1