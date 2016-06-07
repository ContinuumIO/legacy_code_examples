@echo off
SET BLD_DIR=%CD%
SET LIB=C:\Program Files (x86)\Intel\Composer XE 2013 SP1.239\compiler\lib\intel64
cd /D "%RECIPE_DIR%\.."
"%PYTHON%" setup.py install
