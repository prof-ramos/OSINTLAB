# 🧪 OSINTLAB - Guia de Testes

## Visão Geral

Este guia descreve o sistema completo de testes do OSINTLAB, incluindo estrutura, orquestração e execução.

## 📁 Estrutura de Testes

```
tests/
├── __init__.py                 # Inicialização do pacote de testes
├── conftest.py                 # Configurações globais e fixtures
├── pytest_orchestration.py     # Sistema de orquestração inteligente
├── unit/                       # Testes unitários (rápidos, isolados)
│   ├── __init__.py
│   └── test_domain_checker.py
├── integration/                # Testes de integração (APIs, banco, etc)
│   ├── __init__.py
│   └── test_domain_checker_integration.py
└── e2e/                        # Testes end-to-end (fluxo completo)
    └── __init__.py
```

## 🏷️ Marcadores de Testes

Os testes são organizados usando marcadores (markers) do pytest:

- **`@pytest.mark.unit`**: Testes unitários rápidos e isolados
- **`@pytest.mark.integration`**: Testes de integração entre componentes
- **`@pytest.mark.e2e`**: Testes end-to-end completos
- **`@pytest.mark.fast`**: Testes que executam em < 1 segundo
- **`@pytest.mark.slow`**: Testes que demoram > 5 segundos
- **`@pytest.mark.network`**: Testes que requerem conectividade de rede
- **`@pytest.mark.asyncio`**: Testes assíncronos
- **`@pytest.mark.benchmark`**: Testes de performance

## 🚀 Como Executar os Testes

### Usando Make (Recomendado)

```bash
# Executar todos os testes (modo otimizado)
make test

# Testes unitários apenas
make test-unit

# Testes unitários rápidos
make test-unit-fast

# Testes de integração
make test-integration

# Testes em paralelo
make test-parallel

# Testes com cobertura detalhada
make test-coverage

# Testes de benchmark
make test-benchmark
```

### Usando Script Shell

```bash
# Executar todos os testes
./scripts/run_tests.sh all

# Testes unitários
./scripts/run_tests.sh unit

# Testes rápidos
./scripts/run_tests.sh fast

# Testes com cobertura
./scripts/run_tests.sh coverage

# Pipeline de CI
./scripts/run_tests.sh ci
```

### Usando Pytest Diretamente

```bash
# Todos os testes
pytest tests/ -v

# Testes unitários
pytest tests/unit -v

# Testes de integração
pytest tests/integration -v

# Testes por marcador
pytest tests/ -v -m "unit and fast"
pytest tests/ -v -m "not slow"

# Testes paralelos
pytest tests/ -n auto -v

# Com cobertura
pytest tests/ -v --cov=tools --cov=ui --cov-report=html
```

## 🎯 Sistema de Orquestração

O sistema de orquestração inteligente (`pytest_orchestration.py`) oferece:

### Modos de Execução

#### 1. Modo Sequencial
Executa testes um após o outro.

```bash
python tests/pytest_orchestration.py --mode sequential
```

#### 2. Modo Paralelo
Executa todos os testes em paralelo com workers automáticos.

```bash
python tests/pytest_orchestration.py --mode parallel
```

#### 3. Modo Condicional
Executa testes rápidos primeiro; se passarem, executa os lentos.

```bash
python tests/pytest_orchestration.py --mode conditional
```

#### 4. Modo Otimizado (Padrão)
Execução inteligente com balanceamento de recursos.

```bash
python tests/pytest_orchestration.py --mode optimized
# ou simplesmente
python tests/pytest_orchestration.py
```

### Categorias Específicas

```bash
# Apenas testes unitários
python tests/pytest_orchestration.py --category unit

# Apenas integração
python tests/pytest_orchestration.py --category integration

# Todos os testes
python tests/pytest_orchestration.py --category all
```

## 📊 Relatórios

### Relatório de Cobertura HTML

```bash
make test-coverage
make report  # Abre o relatório no navegador
```

### Relatório JSON

Após execução, os relatórios JSON são gerados em:
- `coverage.json` - Cobertura de código
- `htmlcov/pytest_report.json` - Resultados dos testes
- `htmlcov/orchestration_report.json` - Relatório de orquestração

### Visualizar Relatórios

```bash
# Relatório de cobertura
make report

# Relatório do pytest
make report-pytest
```

## 🔧 Configuração

### pyproject.toml

Toda a configuração de testes está em `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
markers = [
    "unit: Testes unitários",
    "integration: Testes de integração",
    # ... outros marcadores
]
```

### Fixtures Globais

As fixtures compartilhadas estão em `tests/conftest.py`:

- `project_root`: Diretório raiz do projeto
- `aio_session`: Sessão aiohttp para testes
- `mock_aio_session`: Mock de sessão aiohttp
- `test_domains`: Lista de domínios para testes
- `performance_tracker`: Rastreador de performance

## 🎨 Boas Práticas

### 1. Nomenclatura

```python
# Arquivos de teste
test_*.py ou *_test.py

# Classes de teste
class TestNomeDaFuncionalidade:
    pass

# Funções de teste
def test_comportamento_esperado():
    pass
```

### 2. Organização

```python
# Arrange (Preparar)
dados = preparar_dados()

# Act (Agir)
resultado = funcao_a_testar(dados)

# Assert (Verificar)
assert resultado == esperado
```

### 3. Marcadores

```python
@pytest.mark.unit
@pytest.mark.fast
def test_funcao_rapida():
    assert True

@pytest.mark.integration
@pytest.mark.network
@pytest.mark.slow
async def test_api_externa():
    # Teste que faz chamada de rede
    pass
```

### 4. Fixtures

```python
@pytest.fixture
def dados_de_teste():
    return {"key": "value"}

def test_com_fixture(dados_de_teste):
    assert dados_de_teste["key"] == "value"
```

## 🔄 CI/CD

### GitHub Actions

O workflow `.github/workflows/tests.yml` executa:

1. ✅ Testes unitários (todas as plataformas e versões Python)
2. ✅ Testes de integração
3. 🚀 Testes paralelos otimizados
4. 🔍 Verificações de qualidade (linting, formatação)
5. ⏱️ Benchmarks de performance
6. 📊 Upload de cobertura para Codecov

### Executar Localmente

```bash
# Simular pipeline de CI
make ci

# Ou usando script
./scripts/run_tests.sh ci
```

## 📈 Monitoramento de Performance

### Benchmarks

```bash
# Executar benchmarks
make test-benchmark

# Ou
pytest tests/ -v -m benchmark --benchmark-only
```

### Profiling

```python
# Usar fixture de performance
def test_com_profiling(performance_tracker):
    with performance_tracker:
        # Código a medir
        funcao_lenta()

    print(f"Duração: {performance_tracker.duration}s")
```

## 🐛 Debugging

### Modo Verbose

```bash
pytest tests/ -vv  # Muito verbose
```

### Parar no Primeiro Erro

```bash
pytest tests/ -x  # Fail fast
```

### Executar Teste Específico

```bash
pytest tests/unit/test_domain_checker.py::TestGenerateDomains::test_generate_2letters -v
```

### PDB (Python Debugger)

```bash
pytest tests/ --pdb  # Para no erro
pytest tests/ -s     # Mostra prints
```

## 📦 Dependências de Teste

Instaladas via `uv`:

```bash
# Apenas dependências de teste
uv pip install -e ".[test]"

# Todas as dependências de desenvolvimento
uv pip install -e ".[dev]"

# Tudo
uv pip install -e ".[all]"
```

## 🔍 Troubleshooting

### Testes Falhando

1. Verifique dependências:
   ```bash
   make install
   ```

2. Limpe cache:
   ```bash
   make clean
   ```

3. Execute testes específicos:
   ```bash
   pytest tests/unit -v
   ```

### Performance Lenta

1. Use testes paralelos:
   ```bash
   make test-parallel
   ```

2. Execute apenas testes rápidos:
   ```bash
   make test-unit-fast
   ```

3. Use modo otimizado:
   ```bash
   python tests/pytest_orchestration.py --mode optimized
   ```

## 📚 Recursos Adicionais

- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-xdist](https://pytest-xdist.readthedocs.io/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)

## 🤝 Contribuindo

Ao adicionar novos testes:

1. Siga a estrutura de diretórios
2. Use marcadores apropriados
3. Adicione fixtures em `conftest.py` se reutilizáveis
4. Documente testes complexos
5. Execute `make pre-commit` antes de commitar

---

**Criado por:** Gabriel Ramos
**Versão:** 1.0.0
**Última atualização:** 2025-11-06
