@echo off
set py_script=%0
set py_script_name=Converter.py
call set py_script=%%py_script:ConvertOBJ.bat=%py_script_name%%%
set output_ext=.J3D
set output_file=%1
call set output_file=%%output_file:.obj=%output_ext%%%
echo Convert: %1 to %output_file%.
py %py_script% -h %1 %output_file%

pause