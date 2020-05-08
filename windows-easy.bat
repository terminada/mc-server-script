@echo off

echo NOTE: THIS BATCH SCRIPT CAN ONLY FUNCTION PROPERLY ON WINDOWS 10
echo CHU Y: FILE BAT CHI CHAY DUOC TREN WINDOWS 10

:DOES_PYTHON_EXIST
python -V | find "Python"    >NUL 2>NUL && (goto :PYTHON_DOES_EXIST)
python -V | find /v "Python" >NUL 2>NUL && (goto :PYTHON_DOES_NOT_EXIST)
goto :EOF

:PYTHON_DOES_NOT_EXIST
python\python.exe -V | find "Python"    >NUL 2>NUL && (goto :PYTHON_PORTABLE_EXIST)
echo May ban chua co Python / You don't have Python installed
echo Dang tai Python / Downloading Python...
curl https://www.python.org/ftp/python/3.7.7/python-3.7.7-embed-amd64.zip > python.zip
echo Da tai xong Python / Downloaded Python
echo Dang giai nen Python / Extracting Python...
mkdir python
tar -C python -xf python.zip
echo Da giai nen Python / Extracted Python
echo Dang cai dat / Installing...

:PYTHON_PORTABLE_EXIST
curl https://bootstrap.pypa.io/get-pip.py > get-pip.py
python\python.exe get-pip.py
python\python.exe -m pip install -r requirements.txt
python\python.exe makeserver.py
pause
goto :EOF

:PYTHON_DOES_EXIST
echo Dang cai dat / Installing...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python makeserver.py
pause
goto :EOF