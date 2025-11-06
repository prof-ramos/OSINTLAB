"""
Pytest Conftest - Configurações Globais de Testes
==================================================

Este arquivo contém fixtures compartilhadas e configurações para todos os testes.
"""

import asyncio
import pytest
from pathlib import Path
from typing import AsyncGenerator, Generator
import aiohttp
from unittest.mock import Mock, AsyncMock

# ============================================================================
# Configurações de Fixtures
# ============================================================================

@pytest.fixture(scope="session")
def project_root() -> Path:
    """Retorna o diretório raiz do projeto."""
    return Path(__file__).parent.parent


@pytest.fixture(scope="session")
def tools_dir(project_root: Path) -> Path:
    """Retorna o diretório de ferramentas."""
    return project_root / "tools"


@pytest.fixture(scope="session")
def ui_dir(project_root: Path) -> Path:
    """Retorna o diretório de UI."""
    return project_root / "ui"


# ============================================================================
# Fixtures de Event Loop (para testes assíncronos)
# ============================================================================

@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """
    Cria um event loop para toda a sessão de testes.
    Necessário para testes assíncronos.
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# ============================================================================
# Fixtures de HTTP Cliente (aiohttp)
# ============================================================================

@pytest.fixture
async def aio_session() -> AsyncGenerator[aiohttp.ClientSession, None]:
    """
    Fornece uma sessão aiohttp para testes.
    Automaticamente fecha a sessão após o teste.
    """
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def mock_aio_session() -> Mock:
    """
    Fornece uma sessão aiohttp mockada para testes sem rede.
    """
    session = AsyncMock(spec=aiohttp.ClientSession)
    return session


# ============================================================================
# Fixtures de Configuração de Testes
# ============================================================================

@pytest.fixture
def test_domains() -> list[str]:
    """Retorna lista de domínios para testes."""
    return [
        "google.com.br",
        "facebook.com.br",
        "test123xyz.com.br",
        "qwerty9876.com.br",
    ]


@pytest.fixture
def available_domain() -> str:
    """Retorna um domínio provavelmente disponível."""
    return "xyz123test456unavailable.com.br"


@pytest.fixture
def unavailable_domain() -> str:
    """Retorna um domínio certamente ocupado."""
    return "google.com.br"


# ============================================================================
# Fixtures de Mock de APIs
# ============================================================================

@pytest.fixture
def mock_registro_br_response_available() -> dict:
    """Mock de resposta da API Registro.br para domínio disponível."""
    return {
        "status": "available",
        "domain": "test123xyz.com.br",
        "message": "Domínio disponível para registro"
    }


@pytest.fixture
def mock_registro_br_response_unavailable() -> dict:
    """Mock de resposta da API Registro.br para domínio ocupado."""
    return {
        "status": "unavailable",
        "domain": "google.com.br",
        "message": "Domínio não disponível"
    }


# ============================================================================
# Hooks do Pytest
# ============================================================================

def pytest_configure(config):
    """
    Configuração executada antes de todos os testes.
    """
    # Registrar marcadores customizados
    config.addinivalue_line(
        "markers", "unit: Testes unitários rápidos isolados"
    )
    config.addinivalue_line(
        "markers", "integration: Testes de integração entre componentes"
    )
    config.addinivalue_line(
        "markers", "e2e: Testes end-to-end completos"
    )
    config.addinivalue_line(
        "markers", "slow: Testes que demoram mais de 5 segundos"
    )
    config.addinivalue_line(
        "markers", "fast: Testes rápidos (< 1 segundo)"
    )


def pytest_collection_modifyitems(config, items):
    """
    Modificar itens coletados antes da execução.
    Útil para classificação automática de testes.
    """
    for item in items:
        # Auto-marcar testes assíncronos
        if asyncio.iscoroutinefunction(item.function):
            item.add_marker(pytest.mark.asyncio)

        # Auto-marcar testes de rede
        if "aio_session" in item.fixturenames or "requests" in item.name.lower():
            item.add_marker(pytest.mark.network)

        # Auto-marcar testes por localização
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        elif "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        elif "e2e" in str(item.fspath):
            item.add_marker(pytest.mark.e2e)


# ============================================================================
# Fixtures de Performance e Benchmark
# ============================================================================

@pytest.fixture
def performance_tracker():
    """
    Rastreia métricas de performance durante os testes.
    """
    import time

    class PerformanceTracker:
        def __init__(self):
            self.start_time = None
            self.end_time = None
            self.duration = None

        def start(self):
            self.start_time = time.perf_counter()

        def stop(self):
            self.end_time = time.perf_counter()
            self.duration = self.end_time - self.start_time
            return self.duration

        def __enter__(self):
            self.start()
            return self

        def __exit__(self, *args):
            self.stop()

    return PerformanceTracker()


# ============================================================================
# Fixtures de Limpeza
# ============================================================================

@pytest.fixture(autouse=True)
def cleanup_test_files(tmp_path):
    """
    Limpa arquivos de teste após cada execução.
    """
    yield
    # Cleanup após o teste
    for file in tmp_path.glob("*"):
        if file.is_file():
            file.unlink()
