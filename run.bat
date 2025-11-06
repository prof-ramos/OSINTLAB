@echo off
REM OSINTLAB - Script de Inicialização (Windows)

echo =========================================
echo 🔍 OSINTLAB - Iniciando Interface...
echo =========================================
echo.

REM Verifica se o Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado!
    echo Por favor, instale Python 3.8 ou superior.
    pause
    exit /b 1
)

REM Verifica se as dependências estão instaladas
python -c "import streamlit" >nul 2>&1
if errorlevel 1 (
    echo 📦 Instalando dependências...
    pip install -r requirements.txt
    echo.
)

REM Inicia o Streamlit
echo 🚀 Iniciando OSINTLAB...
echo.
echo 📍 A interface estará disponível em:
echo    http://localhost:8501
echo.
echo ⚠️  Para parar o servidor, pressione Ctrl+C
echo.
echo =========================================
echo.

streamlit run app.py
