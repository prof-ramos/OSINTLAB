#!/bin/bash
# OSINTLAB - Script de Inicialização

echo "========================================="
echo "🔍 OSINTLAB - Iniciando Interface..."
echo "========================================="
echo ""

# Verifica se o Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado!"
    echo "Por favor, instale Python 3.8 ou superior."
    exit 1
fi

# Verifica se as dependências estão instaladas
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "📦 Instalando dependências..."
    pip install -r requirements.txt
    echo ""
fi

# Inicia o Streamlit
echo "🚀 Iniciando OSINTLAB..."
echo ""
echo "📍 A interface estará disponível em:"
echo "   http://localhost:8501"
echo ""
echo "⚠️  Para parar o servidor, pressione Ctrl+C"
echo ""
echo "========================================="
echo ""

streamlit run app.py
