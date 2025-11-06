#!/bin/bash

###############################################################################
# OSINTLAB - Test Runner Script
# Script para executar testes com diferentes configurações
###############################################################################

set -e

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║              OSINTLAB - Test Automation Suite                   ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Função de ajuda
show_help() {
    echo "Uso: ./scripts/run_tests.sh [OPÇÃO]"
    echo ""
    echo "Opções:"
    echo "  all              Executa todos os testes (modo otimizado)"
    echo "  unit             Executa apenas testes unitários"
    echo "  integration      Executa apenas testes de integração"
    echo "  fast             Executa apenas testes rápidos"
    echo "  parallel         Executa testes em paralelo"
    echo "  coverage         Executa com relatório de cobertura"
    echo "  benchmark        Executa benchmarks de performance"
    echo "  ci               Simula pipeline de CI"
    echo "  watch            Executa testes em modo watch (auto-reload)"
    echo "  help             Mostra esta ajuda"
    echo ""
}

# Verifica se pytest está instalado
check_dependencies() {
    if ! command -v pytest &> /dev/null; then
        echo -e "${RED}❌ pytest não encontrado. Instale com: make install${NC}"
        exit 1
    fi
}

# Executa todos os testes (otimizado)
run_all() {
    echo -e "${BLUE}🧪 Executando todos os testes (modo otimizado)...${NC}"
    python tests/pytest_orchestration.py --mode optimized
}

# Executa testes unitários
run_unit() {
    echo -e "${BLUE}🧪 Executando testes unitários...${NC}"
    pytest tests/unit -v --cov=tools --cov=ui --cov-report=term-missing
}

# Executa testes de integração
run_integration() {
    echo -e "${BLUE}🧪 Executando testes de integração...${NC}"
    pytest tests/integration -v -m integration
}

# Executa apenas testes rápidos
run_fast() {
    echo -e "${BLUE}⚡ Executando testes rápidos...${NC}"
    pytest tests/unit -v -m "unit and fast"
}

# Executa testes em paralelo
run_parallel() {
    echo -e "${BLUE}🚀 Executando testes em paralelo...${NC}"
    pytest tests -n auto -v
}

# Executa com cobertura detalhada
run_coverage() {
    echo -e "${BLUE}📊 Executando testes com cobertura detalhada...${NC}"
    pytest tests -v \
        --cov=tools \
        --cov=ui \
        --cov-report=html \
        --cov-report=term-missing \
        --cov-report=json \
        --cov-report=xml

    echo ""
    echo -e "${GREEN}✅ Relatório de cobertura gerado em: htmlcov/index.html${NC}"

    # Abre o relatório no navegador (macOS)
    if [[ "$OSTYPE" == "darwin"* ]]; then
        open htmlcov/index.html
    fi
}

# Executa benchmarks
run_benchmark() {
    echo -e "${BLUE}⏱️  Executando benchmarks de performance...${NC}"
    pytest tests -v -m benchmark --benchmark-only
}

# Simula pipeline de CI
run_ci() {
    echo -e "${BLUE}🔄 Simulando pipeline de CI...${NC}"

    echo -e "${YELLOW}1. Linting...${NC}"
    ruff check . || true

    echo -e "${YELLOW}2. Formatação...${NC}"
    black --check . || true

    echo -e "${YELLOW}3. Testes unitários...${NC}"
    pytest tests/unit -v --cov=tools --cov=ui

    echo -e "${YELLOW}4. Testes de integração...${NC}"
    pytest tests/integration -v || true

    echo -e "${GREEN}✅ Pipeline de CI concluído!${NC}"
}

# Modo watch (auto-reload)
run_watch() {
    echo -e "${BLUE}👀 Modo watch ativado (Ctrl+C para sair)...${NC}"
    pytest-watch tests/ -- -v
}

# Main
main() {
    check_dependencies

    case "${1:-all}" in
        all)
            run_all
            ;;
        unit)
            run_unit
            ;;
        integration)
            run_integration
            ;;
        fast)
            run_fast
            ;;
        parallel)
            run_parallel
            ;;
        coverage)
            run_coverage
            ;;
        benchmark)
            run_benchmark
            ;;
        ci)
            run_ci
            ;;
        watch)
            run_watch
            ;;
        help|--help|-h)
            show_help
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Opção inválida: $1${NC}"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

main "$@"
