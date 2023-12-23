@echo off

G:
cd "G:\Fleet Command\Graphics"

for %%a in (%*) do (
  copy "%%a" "G:\Fleet Command\Graphics"
  "cmpUtil.exe" 3d "%%~nxa"
)

pause