# 🚀 OSINTLAB - Setup e Instalação

## Requisitos

- **Python**: 3.8 ou superior
- **UV**: Gerenciador de pacotes moderno (recomendado)
- **Sistema Operacional**: macOS, Linux ou Windows
- **Memória**: Mínimo 4GB RAM (8GB recomendado para testes paralelos)

## 🔧 Instalação Rápida

### 1. Clonar o Repositório

```bash
git clone https://github.com/prof-ramos/OSINTLAB.git
cd OSINTLAB
```

### 2. Instalar UV (se ainda não tiver)

#### macOS e Linux
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Windows (PowerShell)
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 3. Instalar Dependências

#### Dependências Básicas
```bash
uv pip install -e .
```

#### Dependências de Desenvolvimento
```bash
uv pip install -e ".[dev]"
```

#### Dependências de Teste
```bash
uv pip install -e ".[test]"
```

#### Todas as Dependências
```bash
uv pip install -e ".[all]"
```

### 4. Verificar Instalação

```bash
# Verificar informações do ambiente
make info

# Executar teste rápido
python tools/domain-checker/test_quick.py
```

## 📦 Instalação com Make

O projeto inclui um Makefile completo para facilitar a instalação:

```bash
# Instalar dependências de desenvolvimento
make install

# Instalar todas as dependências
make install-all

# Configurar ambiente completo
make dev
```

## 🧪 Executar Testes

Após a instalação, você pode executar os testes:

```bash
# Testes básicos
make test-unit-fast

# Todos os testes
make test

# Testes com cobertura
make test-coverage
```

## 🎨 Configuração do Ambiente

### Ambiente Virtual (Opcional)

Embora `uv` gerencie dependências de forma eficiente, você pode usar um ambiente virtual:

```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
# macOS/Linux:
source .venv/bin/activate
# Windows:
.venv\Scripts\activate

# Instalar com uv
uv pip install -e ".[all]"
```

### Configuração do Pre-commit (Opcional)

Para garantir qualidade de código antes de cada commit:

```bash
# Instalar hooks de pre-commit
pre-commit install

# Executar manualmente
make pre-commit
```

## 🔍 Estrutura do Projeto

```
OSINTLAB/
├── .github/
│   └── workflows/        # CI/CD com GitHub Actions
├── scripts/
│   └── run_tests.sh      # Script de execução de testes
├── tests/
│   ├── unit/             # Testes unitários
│   ├── integration/      # Testes de integração
│   ├── e2e/              # Testes end-to-end
│   ├── conftest.py       # Fixtures compartilhadas
│   └── pytest_orchestration.py  # Orquestração inteligente
├── tools/
│   └── domain-checker/   # Ferramenta de verificação de domínios
├── ui/
│   └── pages/            # Páginas da interface Streamlit
├── app.py                # Aplicação principal
├── pyproject.toml        # Configuração do projeto
├── Makefile              # Comandos make
├── TESTING.md            # Guia de testes
└── SETUP.md              # Este arquivo
```

## 🚀 Executar a Aplicação

### Modo Desenvolvimento

```bash
# Usando Make
make run

# Ou diretamente
streamlit run app.py
```

### Modo Produção

```bash
streamlit run app.py --server.port 8501 --server.headless true
```

## 🔧 Comandos Úteis

### Testes

```bash
make test              # Executar todos os testes (otimizado)
make test-unit         # Testes unitários
make test-integration  # Testes de integração
make test-parallel     # Testes em paralelo
make test-coverage     # Testes com cobertura
make test-benchmark    # Benchmarks de performance
```

### Qualidade de Código

```bash
make lint              # Verificar linting
make lint-fix          # Corrigir problemas de linting
make format            # Formatar código
make format-check      # Verificar formatação
make typecheck         # Verificar tipos
make quality           # Todas as verificações
```

### Limpeza

```bash
make clean             # Limpar arquivos temporários
make clean-all         # Limpeza completa (incluindo venv)
```

### CI/CD

```bash
make ci                # Simular pipeline de CI
make pre-commit        # Verificações antes de commit
```

### Relatórios

```bash
make report            # Abrir relatório de cobertura
make report-pytest     # Abrir relatório do pytest
```

## 🐛 Troubleshooting

### Erro: "uv: command not found"

Instale o UV seguindo as instruções acima ou use pip tradicional:

```bash
pip install -e ".[all]"
```

### Erro: "pytest: command not found"

Instale as dependências de teste:

```bash
uv pip install -e ".[test]"
```

### Testes Falhando

1. Limpe o cache:
   ```bash
   make clean
   ```

2. Reinstale as dependências:
   ```bash
   make install
   ```

3. Execute testes específicos:
   ```bash
   pytest tests/unit -v
   ```

### Performance Lenta no MacBook Air M3

O projeto está otimizado para Apple Silicon, mas com 8GB RAM:

1. Use testes paralelos com menos workers:
   ```bash
   pytest tests -n 4 -v
   ```

2. Execute apenas testes rápidos durante desenvolvimento:
   ```bash
   make test-unit-fast
   ```

3. Use modo otimizado da orquestração:
   ```bash
   python tests/pytest_orchestration.py --mode optimized
   ```

## 📊 Monitoramento de Recursos

### Verificar Uso de Memória

```bash
# Durante execução de testes paralelos
# macOS:
top -pid $(pgrep -f pytest)

# Linux:
htop -p $(pgrep -f pytest)
```

### Ajustar Execução Paralela

Edite `pyproject.toml` para ajustar workers:

```toml
[tool.pytest.ini_options]
addopts = ["-n", "4"]  # Usar 4 workers em vez de "auto"
```

## 🔐 Variáveis de Ambiente (Opcional)

Crie um arquivo `.env` para configurações:

```bash
# .env
PYTEST_TIMEOUT=300
PYTEST_WORKERS=4
UV_CACHE_DIR=.uv_cache
```

## 📚 Próximos Passos

1. ✅ Instalação completa
2. 📖 Ler [TESTING.md](TESTING.md) para guia de testes
3. 🧪 Executar `make test-unit-fast` para validar setup
4. 🚀 Executar `make run` para iniciar a aplicação
5. 🔍 Explorar o código em `tools/` e `ui/`

## 🤝 Contribuindo

Para contribuir com o projeto:

1. Fork o repositório
2. Crie uma branch para sua feature
3. Faça suas alterações
4. Execute `make pre-commit`
5. Commit e push
6. Abra um Pull Request

## 📞 Suporte

- **GitHub Issues**: [Reportar bug](https://github.com/prof-ramos/OSINTLAB/issues)
- **Documentação**: [Wiki do projeto](https://github.com/prof-ramos/OSINTLAB/wiki)
- **Autor**: [@prof-ramos](https://github.com/prof-ramos)

## 📄 Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

---

**Versão:** 1.0.0
**Última atualização:** 2025-11-06
