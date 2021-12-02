@ECHO off

REM check for python installation
python --version

REM update python
python -m pip install --upgrade pip

REM install dependencies
pip install tqdm

REM start python script
python ./extract_swf_all.py

pause