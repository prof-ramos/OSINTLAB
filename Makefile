.PHONY: help install test test-unit test-integration test-all test-fast test-coverage lint format clean

# Cores para output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Exibe ajuda
	@echo "$(BLUE)OSINTLAB - Comandos Disponíveis$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

install: ## Instala dependências com uv
	@echo "$(BLUE)📦 Instalando dependências...$(NC)"
	uv pip install -e ".[dev,test]"

install-all: ## Instala todas as dependências
	@echo "$(BLUE)📦 Instalando todas as dependências...$(NC)"
	uv pip install -e ".[all]"

# ============================================================================
# Testes
# ============================================================================

test: ## Executa todos os testes (modo otimizado)
	@echo "$(BLUE)🧪 Executando todos os testes (otimizado)...$(NC)"
	python tests/pytest_orchestration.py --mode optimized

test-unit: ## Executa apenas testes unitários
	@echo "$(BLUE)🧪 Executando testes unitários...$(NC)"
	pytest tests/unit -v --cov=tools --cov=ui --cov-report=term-missing

test-unit-fast: ## Executa apenas testes unitários rápidos
	@echo "$(BLUE)⚡ Executando testes unitários rápidos...$(NC)"
	pytest tests/unit -v -m "unit and fast"

test-integration: ## Executa testes de integração
	@echo "$(BLUE)🧪 Executando testes de integração...$(NC)"
	pytest tests/integration -v -m integration

test-parallel: ## Executa testes em paralelo
	@echo "$(BLUE)🚀 Executando testes em paralelo...$(NC)"
	pytest tests -n auto -v

test-sequential: ## Executa testes sequencialmente
	@echo "$(BLUE)📝 Executando testes sequencialmente...$(NC)"
	python tests/pytest_orchestration.py --mode sequential

test-conditional: ## Executa testes com lógica condicional
	@echo "$(BLUE)🔀 Executando testes com lógica condicional...$(NC)"
	python tests/pytest_orchestration.py --mode conditional

test-coverage: ## Executa testes com relatório de cobertura detalhado
	@echo "$(BLUE)📊 Executando testes com cobertura...$(NC)"
	pytest tests -v --cov=tools --cov=ui \
		--cov-report=html \
		--cov-report=term-missing \
		--cov-report=json \
		--cov-report=xml

test-benchmark: ## Executa testes de benchmark
	@echo "$(BLUE)⏱️  Executando benchmarks...$(NC)"
	pytest tests -v -m benchmark --benchmark-only

test-network: ## Executa apenas testes que requerem rede
	@echo "$(BLUE)🌐 Executando testes de rede...$(NC)"
	pytest tests -v -m network

test-no-network: ## Executa testes sem requisitos de rede
	@echo "$(BLUE)🚫 Executando testes sem rede...$(NC)"
	pytest tests -v -m "not network"

# ============================================================================
# Code Quality
# ============================================================================

lint: ## Executa linting com ruff
	@echo "$(BLUE)🔍 Executando linting...$(NC)"
	ruff check .

lint-fix: ## Corrige problemas de linting automaticamente
	@echo "$(BLUE)🔧 Corrigindo problemas de linting...$(NC)"
	ruff check --fix .

format: ## Formata código com black
	@echo "$(BLUE)✨ Formatando código...$(NC)"
	black .

format-check: ## Verifica formatação sem modificar
	@echo "$(BLUE)🔍 Verificando formatação...$(NC)"
	black --check .

typecheck: ## Verifica tipos com mypy
	@echo "$(BLUE)🔍 Verificando tipos...$(NC)"
	mypy tools ui

quality: lint format typecheck ## Executa todas as verificações de qualidade

# ============================================================================
# Limpeza
# ============================================================================

clean: ## Remove arquivos temporários e cache
	@echo "$(YELLOW)🧹 Limpando arquivos temporários...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf coverage.xml coverage.json
	@echo "$(GREEN)✅ Limpeza concluída!$(NC)"

clean-all: clean ## Remove todos os arquivos gerados incluindo venv
	@echo "$(YELLOW)🧹 Limpeza completa...$(NC)"
	rm -rf .venv/
	rm -rf dist/
	rm -rf build/
	@echo "$(GREEN)✅ Limpeza completa concluída!$(NC)"

# ============================================================================
# Desenvolvimento
# ============================================================================

dev: install ## Configura ambiente de desenvolvimento
	@echo "$(GREEN)✅ Ambiente de desenvolvimento configurado!$(NC)"

run: ## Executa aplicação Streamlit
	@echo "$(BLUE)🚀 Iniciando OSINTLAB...$(NC)"
	streamlit run app.py

run-test-quick: ## Executa teste rápido do domain checker
	@echo "$(BLUE)🧪 Executando teste rápido...$(NC)"
	python tools/domain-checker/test_quick.py

# ============================================================================
# CI/CD
# ============================================================================

ci: clean install test-coverage lint ## Executa pipeline de CI
	@echo "$(GREEN)✅ Pipeline de CI concluído!$(NC)"

pre-commit: format lint test-unit-fast ## Executa verificações antes de commit
	@echo "$(GREEN)✅ Pré-commit verificações concluídas!$(NC)"

# ============================================================================
# Relatórios
# ============================================================================

report: ## Abre relatório HTML de cobertura
	@echo "$(BLUE)📊 Abrindo relatório de cobertura...$(NC)"
	@if [ -f htmlcov/index.html ]; then \
		open htmlcov/index.html || xdg-open htmlcov/index.html; \
	else \
		echo "$(RED)❌ Relatório não encontrado. Execute 'make test-coverage' primeiro.$(NC)"; \
	fi

report-pytest: ## Abre relatório HTML do pytest
	@echo "$(BLUE)📊 Abrindo relatório do pytest...$(NC)"
	@if [ -f htmlcov/pytest_report.html ]; then \
		open htmlcov/pytest_report.html || xdg-open htmlcov/pytest_report.html; \
	else \
		echo "$(RED)❌ Relatório não encontrado. Execute 'make test' primeiro.$(NC)"; \
	fi

# ============================================================================
# Informações
# ============================================================================

info: ## Exibe informações do ambiente
	@echo "$(BLUE)ℹ️  Informações do Ambiente$(NC)"
	@echo ""
	@echo "Python: $$(python --version)"
	@echo "UV: $$(uv --version 2>/dev/null || echo 'não instalado')"
	@echo "Pytest: $$(pytest --version 2>/dev/null || echo 'não instalado')"
	@echo "Black: $$(black --version 2>/dev/null || echo 'não instalado')"
	@echo "Ruff: $$(ruff --version 2>/dev/null || echo 'não instalado')"
