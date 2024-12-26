@echo off
set ENV_NAME=venv

echo Creando entorno virtual "%ENV_NAME%"...
python -m venv %ENV_NAME%
echo Entorno virtual creado.

echo Activando entorno virtual...
call %ENV_NAME%\Scripts\activate

echo Instalando dependencias...
pip install -r requirements.txt

echo El entorno virtual está activo. ¡Listo para usar!
cmd /K