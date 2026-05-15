@echo off
echo 🚀 更新股票數據...

C:\Users\chris\AppData\Local\Python\pythoncore-3.14-64\python.exe main.py

echo 🌐 開 Dashboard...

C:\Users\chris\AppData\Local\Python\pythoncore-3.14-64\python.exe -m streamlit run app.py

pause