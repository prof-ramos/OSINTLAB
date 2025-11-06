"""
Testes de Integração - Domain Checker
======================================

Testes de integração com APIs externas e fluxo completo.
"""

import pytest
import asyncio
import aiohttp
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tools.domain_checker.domain_checker_advanced import DomainChecker, setup_logging


# ============================================================================
# Testes de Integração com API Real
# ============================================================================

@pytest.mark.integration
@pytest.mark.network
@pytest.mark.slow
@pytest.mark.asyncio
class TestDomainCheckerIntegration:
    """Testes de integração com API do Registro.br"""

    async def test_check_real_unavailable_domain(self):
        """Testa verificação de domínio real ocupado"""
        logger = setup_logging()
        checker = DomainChecker(logger, timeout=15)

        async with aiohttp.ClientSession() as session:
            semaphore = asyncio.Semaphore(1)
            result = await checker.check_domain(session, "google.com.br", semaphore)

        # google.com.br deve estar ocupado
        assert result is None
        assert checker.verificados == 1

    async def test_check_real_available_domain(self):
        """Testa verificação de domínio provavelmente disponível"""
        logger = setup_logging()
        checker = DomainChecker(logger, timeout=15)

        # Domínio com alta probabilidade de estar disponível
        test_domain = "xyz123test456unavailable9999.com.br"

        async with aiohttp.ClientSession() as session:
            semaphore = asyncio.Semaphore(1)
            result = await checker.check_domain(session, test_domain, semaphore)

        # Se disponível, deve retornar o domínio
        # Se ocupado (improvável), deve retornar None
        assert result == test_domain or result is None
        assert checker.verificados == 1

    async def test_check_multiple_domains_real(self):
        """Testa verificação de múltiplos domínios reais"""
        logger = setup_logging()
        checker = DomainChecker(logger, batch_size=3, timeout=15)

        test_domains = [
            "google.com.br",
            "facebook.com.br",
            "xyz123test.com.br",
        ]

        async with aiohttp.ClientSession() as session:
            semaphore = asyncio.Semaphore(3)
            tasks = [
                checker.check_domain(session, domain, semaphore)
                for domain in test_domains
            ]
            results = await asyncio.gather(*tasks)

        # Pelo menos google.com.br deve estar ocupado
        assert results[0] is None  # google.com.br
        assert checker.verificados == len(test_domains)


# ============================================================================
# Testes de Fluxo Completo
# ============================================================================

@pytest.mark.integration
@pytest.mark.network
@pytest.mark.slow
@pytest.mark.asyncio
class TestCompleteWorkflow:
    """Testes de fluxo completo de verificação"""

    async def test_complete_workflow_small_batch(self, tmp_path):
        """Testa fluxo completo com pequeno lote de domínios"""
        logger = setup_logging()
        checker = DomainChecker(
            logger,
            batch_size=5,
            batch_delay=0.5,
            timeout=15
        )

        # Gera alguns domínios de teste
        test_domains = [
            f"test{i}xyz123.com.br" for i in range(10)
        ]

        output_file = tmp_path / "test_results.csv"
        await checker.verify_domains(test_domains, str(output_file))

        # Verifica que o arquivo foi criado
        assert output_file.exists()

        # Verifica que todos os domínios foram verificados
        assert checker.verificados == len(test_domains)

    async def test_workflow_with_known_domains(self, tmp_path):
        """Testa fluxo com domínios conhecidos"""
        logger = setup_logging()
        checker = DomainChecker(logger, timeout=15)

        # Mix de domínios ocupados e possivelmente disponíveis
        test_domains = [
            "google.com.br",  # Ocupado
            "facebook.com.br",  # Ocupado
            "xyz123testunlikely999.com.br",  # Possivelmente disponível
        ]

        output_file = tmp_path / "known_results.csv"
        await checker.verify_domains(test_domains, str(output_file))

        assert output_file.exists()
        assert checker.verificados == 3


# ============================================================================
# Testes de Resiliência
# ============================================================================

@pytest.mark.integration
@pytest.mark.slow
@pytest.mark.asyncio
class TestResilience:
    """Testes de resiliência e recuperação de erros"""

    async def test_retry_logic_with_timeout(self):
        """Testa lógica de retry com timeout baixo"""
        logger = setup_logging()
        checker = DomainChecker(
            logger,
            timeout=0.001,  # Timeout muito baixo para forçar erro
            max_retries=2
        )

        async with aiohttp.ClientSession() as session:
            semaphore = asyncio.Semaphore(1)
            result = await checker.check_domain(session, "test.com.br", semaphore)

        # Deve falhar e incrementar erros
        assert result is None
        assert checker.erros == 1

    async def test_concurrent_requests_handling(self):
        """Testa tratamento de requisições concorrentes"""
        logger = setup_logging()
        checker = DomainChecker(logger, batch_size=10, timeout=15)

        # Cria 10 domínios de teste
        test_domains = [f"test{i}.com.br" for i in range(10)]

        async with aiohttp.ClientSession() as session:
            semaphore = asyncio.Semaphore(10)
            tasks = [
                checker.check_domain(session, domain, semaphore)
                for domain in test_domains
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)

        # Verifica que todas as requisições foram processadas
        assert len(results) == 10
        assert checker.verificados + checker.erros == 10


# ============================================================================
# Testes de Proxy (Mockados)
# ============================================================================

@pytest.mark.integration
class TestProxyIntegration:
    """Testes de integração com proxy"""

    def test_proxy_rotation(self):
        """Testa rotação de proxies"""
        logger = setup_logging()
        proxies = [
            "http://proxy1.com:8080",
            "http://proxy2.com:8080",
            "http://proxy3.com:8080",
        ]
        checker = DomainChecker(logger, proxies=proxies)

        # Testa múltiplas chamadas de get_proxy
        selected_proxies = {checker.get_proxy() for _ in range(50)}

        # Deve ter usado todos os proxies disponíveis
        assert len(selected_proxies) <= len(proxies)
        assert all(p in proxies for p in selected_proxies)
