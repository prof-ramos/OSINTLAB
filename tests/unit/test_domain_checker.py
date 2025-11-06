"""
Testes Unitários - Domain Checker
==================================

Testes isolados para funcionalidades do verificador de domínios.
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch, MagicMock
import aiohttp
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Importa as funções a serem testadas
from tools.domain_checker.domain_checker_advanced import (
    DomainChecker,
    generate_domains,
    load_proxies,
    setup_logging
)


# ============================================================================
# Testes de Geração de Domínios
# ============================================================================

@pytest.mark.unit
@pytest.mark.fast
class TestGenerateDomains:
    """Testes para função generate_domains"""

    def test_generate_2letters(self):
        """Testa geração de domínios de 2 letras"""
        domains = generate_domains("2letters")
        assert len(domains) == 26 * 26  # 676 combinações
        assert "aa.com.br" in domains
        assert "zz.com.br" in domains
        assert all(d.endswith(".com.br") for d in domains)

    def test_generate_3letters(self):
        """Testa geração de domínios de 3 letras"""
        domains = generate_domains("3letters")
        assert len(domains) == 26 * 26 * 26  # 17576 combinações
        assert "aaa.com.br" in domains
        assert "zzz.com.br" in domains

    def test_generate_4letters(self):
        """Testa geração de domínios de 4 letras"""
        domains = generate_domains("4letters")
        assert len(domains) == 26 ** 4  # 456976 combinações
        assert "aaaa.com.br" in domains
        assert "zzzz.com.br" in domains

    def test_generate_custom_pattern(self):
        """Testa geração com padrão customizado"""
        domains = generate_domains("custom:abc")
        assert len(domains) == 3 ** 3  # 27 combinações
        assert "aaa.com.br" in domains
        assert "ccc.com.br" in domains
        # Não deve conter letras fora do padrão
        assert not any("d" in d for d in domains)

    def test_generate_invalid_pattern(self):
        """Testa que padrão inválido levanta erro"""
        with pytest.raises(ValueError, match="Padrão desconhecido"):
            generate_domains("invalid_pattern")


# ============================================================================
# Testes de Carregamento de Proxies
# ============================================================================

@pytest.mark.unit
@pytest.mark.fast
class TestLoadProxies:
    """Testes para função load_proxies"""

    def test_load_proxies_from_file(self, tmp_path):
        """Testa carregamento de proxies de arquivo"""
        proxy_file = tmp_path / "proxies.txt"
        proxy_file.write_text(
            "http://proxy1.com:8080\n"
            "http://proxy2.com:8080\n"
            "# Comment line\n"
            "http://proxy3.com:8080\n"
        )

        proxies = load_proxies(str(proxy_file))
        assert len(proxies) == 3
        assert "http://proxy1.com:8080" in proxies
        assert "http://proxy2.com:8080" in proxies
        assert "http://proxy3.com:8080" in proxies

    def test_load_proxies_empty_file(self, tmp_path):
        """Testa carregamento de arquivo vazio"""
        proxy_file = tmp_path / "empty.txt"
        proxy_file.write_text("")

        proxies = load_proxies(str(proxy_file))
        assert proxies == []

    def test_load_proxies_nonexistent_file(self):
        """Testa carregamento de arquivo inexistente"""
        proxies = load_proxies("nonexistent.txt")
        assert proxies == []


# ============================================================================
# Testes de Logging
# ============================================================================

@pytest.mark.unit
@pytest.mark.fast
class TestLogging:
    """Testes para configuração de logging"""

    def test_setup_logging_console_only(self):
        """Testa configuração de logging apenas para console"""
        logger = setup_logging()
        assert logger.name == 'domain_checker'
        assert logger.level == 20  # INFO
        assert len(logger.handlers) >= 1

    def test_setup_logging_with_file(self, tmp_path):
        """Testa configuração de logging com arquivo"""
        log_file = tmp_path / "test.log"
        logger = setup_logging(str(log_file))

        assert logger.name == 'domain_checker'
        assert len(logger.handlers) >= 2
        assert log_file.exists()


# ============================================================================
# Testes da Classe DomainChecker
# ============================================================================

@pytest.mark.unit
class TestDomainCheckerInit:
    """Testes de inicialização do DomainChecker"""

    def test_init_default_values(self):
        """Testa inicialização com valores padrão"""
        logger = Mock()
        checker = DomainChecker(logger)

        assert checker.logger == logger
        assert checker.proxies == []
        assert checker.batch_size == 50
        assert checker.batch_delay == 1.0
        assert checker.timeout == 10
        assert checker.max_retries == 3
        assert checker.verificados == 0
        assert checker.erros == 0
        assert len(checker.disponiveis) == 0

    def test_init_custom_values(self):
        """Testa inicialização com valores customizados"""
        logger = Mock()
        proxies = ["http://proxy1.com:8080", "http://proxy2.com:8080"]

        checker = DomainChecker(
            logger=logger,
            proxies=proxies,
            batch_size=100,
            batch_delay=0.5,
            timeout=15,
            max_retries=5
        )

        assert checker.proxies == proxies
        assert checker.batch_size == 100
        assert checker.batch_delay == 0.5
        assert checker.timeout == 15
        assert checker.max_retries == 5

    def test_get_proxy_with_proxies(self):
        """Testa obtenção de proxy quando existem proxies"""
        logger = Mock()
        proxies = ["http://proxy1.com:8080", "http://proxy2.com:8080"]
        checker = DomainChecker(logger, proxies=proxies)

        proxy = checker.get_proxy()
        assert proxy in proxies

    def test_get_proxy_without_proxies(self):
        """Testa obtenção de proxy quando não há proxies"""
        logger = Mock()
        checker = DomainChecker(logger)

        proxy = checker.get_proxy()
        assert proxy is None


# ============================================================================
# Testes Assíncronos de check_domain
# ============================================================================

@pytest.mark.unit
@pytest.mark.asyncio
class TestCheckDomain:
    """Testes para método check_domain"""

    async def test_check_domain_available(self, mock_aio_session):
        """Testa verificação de domínio disponível"""
        logger = Mock()
        checker = DomainChecker(logger)

        # Mock da resposta
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(return_value="Domínio disponível")
        mock_aio_session.get = AsyncMock(return_value=mock_response)
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock()

        semaphore = asyncio.Semaphore(1)
        result = await checker.check_domain(mock_aio_session, "test.com.br", semaphore)

        assert result == "test.com.br"
        assert checker.verificados == 1

    async def test_check_domain_unavailable(self, mock_aio_session):
        """Testa verificação de domínio ocupado"""
        logger = Mock()
        checker = DomainChecker(logger)

        # Mock da resposta
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.text = AsyncMock(return_value="Domínio não disponível")
        mock_aio_session.get = AsyncMock(return_value=mock_response)
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock()

        semaphore = asyncio.Semaphore(1)
        result = await checker.check_domain(mock_aio_session, "google.com.br", semaphore)

        assert result is None
        assert checker.verificados == 1

    async def test_check_domain_http_error(self, mock_aio_session):
        """Testa tratamento de erro HTTP"""
        logger = Mock()
        checker = DomainChecker(logger, max_retries=2)

        # Mock de resposta com erro
        mock_response = AsyncMock()
        mock_response.status = 500
        mock_aio_session.get = AsyncMock(return_value=mock_response)
        mock_response.__aenter__ = AsyncMock(return_value=mock_response)
        mock_response.__aexit__ = AsyncMock()

        semaphore = asyncio.Semaphore(1)
        result = await checker.check_domain(mock_aio_session, "test.com.br", semaphore)

        assert result is None
        assert checker.erros == 1

    async def test_check_domain_timeout(self, mock_aio_session):
        """Testa tratamento de timeout"""
        logger = Mock()
        checker = DomainChecker(logger, max_retries=2)

        # Mock de timeout
        mock_aio_session.get = AsyncMock(side_effect=asyncio.TimeoutError)

        semaphore = asyncio.Semaphore(1)
        result = await checker.check_domain(mock_aio_session, "test.com.br", semaphore)

        assert result is None
        assert checker.erros == 1


# ============================================================================
# Testes de Salvamento de Resultados
# ============================================================================

@pytest.mark.unit
@pytest.mark.fast
class TestSaveResults:
    """Testes para método save_results"""

    def test_save_results_to_csv(self, tmp_path):
        """Testa salvamento de resultados em CSV"""
        logger = Mock()
        checker = DomainChecker(logger)
        checker.disponiveis = {"test1.com.br", "test2.com.br", "test3.com.br"}

        output_file = tmp_path / "results.csv"
        checker.save_results(str(output_file))

        assert output_file.exists()

        # Verifica conteúdo do arquivo
        content = output_file.read_text()
        assert "dominio,verificado_em" in content
        assert "test1.com.br" in content
        assert "test2.com.br" in content
        assert "test3.com.br" in content

    def test_save_results_empty(self, tmp_path):
        """Testa salvamento quando não há resultados"""
        logger = Mock()
        checker = DomainChecker(logger)

        output_file = tmp_path / "empty_results.csv"
        checker.save_results(str(output_file))

        assert output_file.exists()
        content = output_file.read_text()
        assert "dominio,verificado_em" in content
        # Apenas o header deve estar presente
        assert len(content.strip().split('\n')) == 1


# ============================================================================
# Testes de Performance e Benchmark
# ============================================================================

@pytest.mark.benchmark
@pytest.mark.slow
class TestPerformance:
    """Testes de performance"""

    def test_generate_domains_performance(self, benchmark):
        """Benchmark de geração de domínios"""
        result = benchmark(generate_domains, "2letters")
        assert len(result) == 676

    def test_load_proxies_performance(self, benchmark, tmp_path):
        """Benchmark de carregamento de proxies"""
        proxy_file = tmp_path / "proxies.txt"
        proxies_list = [f"http://proxy{i}.com:8080\n" for i in range(100)]
        proxy_file.write_text("".join(proxies_list))

        result = benchmark(load_proxies, str(proxy_file))
        assert len(result) == 100
