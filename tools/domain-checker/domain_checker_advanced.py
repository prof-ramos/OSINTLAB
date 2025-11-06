#!/usr/bin/env python3
"""
Verificador Assíncrono de Domínios .com.br - Versão Avançada
Versão otimizada com proxy rotativo, logging em tempo real e retry logic
"""

import asyncio
import aiohttp
import itertools
import csv
import logging
import argparse
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Set
import random

# Configuração de logging
def setup_logging(log_file: str = None) -> logging.Logger:
    """
    Configura logging para arquivo e console

    Args:
        log_file: Caminho do arquivo de log (opcional)

    Returns:
        Logger configurado
    """
    logger = logging.getLogger('domain_checker')
    logger.setLevel(logging.INFO)

    # Formato do log
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Handler para console
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Handler para arquivo
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


class DomainChecker:
    """
    Classe para verificação assíncrona de domínios .com.br
    """

    API_URL = "https://registro.br/v2/ajax/avail/raw/"

    def __init__(
        self,
        logger: logging.Logger,
        proxies: List[str] = None,
        batch_size: int = 50,
        batch_delay: float = 1.0,
        timeout: int = 10,
        max_retries: int = 3
    ):
        """
        Inicializa o verificador de domínios

        Args:
            logger: Logger para registrar eventos
            proxies: Lista de proxies para rotação (opcional)
            batch_size: Quantidade de requisições simultâneas
            batch_delay: Delay entre lotes (segundos)
            timeout: Timeout para requisições (segundos)
            max_retries: Número máximo de tentativas em caso de erro
        """
        self.logger = logger
        self.proxies = proxies or []
        self.batch_size = batch_size
        self.batch_delay = batch_delay
        self.timeout = timeout
        self.max_retries = max_retries
        self.disponiveis: Set[str] = set()
        self.verificados = 0
        self.erros = 0

    def get_proxy(self) -> Optional[str]:
        """
        Retorna um proxy aleatório da lista

        Returns:
            URL do proxy ou None se não houver proxies
        """
        if self.proxies:
            return random.choice(self.proxies)
        return None

    async def check_domain(
        self,
        session: aiohttp.ClientSession,
        domain: str,
        semaphore: asyncio.Semaphore
    ) -> Optional[str]:
        """
        Verifica se um domínio está disponível com retry logic

        Args:
            session: Sessão aiohttp
            domain: Nome do domínio a verificar
            semaphore: Semáforo para controle de concorrência

        Returns:
            str: Nome do domínio se disponível, None caso contrário
        """
        async with semaphore:
            for attempt in range(self.max_retries):
                try:
                    proxy = self.get_proxy()
                    timeout = aiohttp.ClientTimeout(total=self.timeout)

                    async with session.get(
                        self.API_URL + domain,
                        proxy=proxy,
                        timeout=timeout
                    ) as resp:
                        if resp.status == 200:
                            data = await resp.text()
                            self.verificados += 1

                            if "disponível" in data.lower():
                                self.logger.info(f"✅ {domain} DISPONÍVEL")
                                return domain
                            else:
                                self.logger.debug(f"❌ {domain} ocupado")
                                return None
                        else:
                            self.logger.warning(
                                f"⚠️ {domain} - Status {resp.status} (tentativa {attempt + 1}/{self.max_retries})"
                            )

                except asyncio.TimeoutError:
                    self.logger.warning(
                        f"⏱️ {domain} - Timeout (tentativa {attempt + 1}/{self.max_retries})"
                    )
                except Exception as e:
                    self.logger.warning(
                        f"⚠️ {domain} - Erro: {str(e)[:50]} (tentativa {attempt + 1}/{self.max_retries})"
                    )

                # Espera exponencial entre tentativas
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(2 ** attempt)

            # Falha após todas as tentativas
            self.erros += 1
            self.logger.error(f"❌ {domain} - Falha após {self.max_retries} tentativas")
            return None

    async def verify_domains(
        self,
        domains: List[str],
        output_file: str = "disponiveis.csv"
    ):
        """
        Verifica uma lista de domínios de forma assíncrona

        Args:
            domains: Lista de domínios a verificar
            output_file: Arquivo para salvar resultados
        """
        total = len(domains)
        self.logger.info(f"🚀 Iniciando verificação de {total} domínios")
        self.logger.info(f"⚙️ Configuração: batch_size={self.batch_size}, delay={self.batch_delay}s")

        if self.proxies:
            self.logger.info(f"🔄 Usando {len(self.proxies)} proxies para rotação")

        semaphore = asyncio.Semaphore(self.batch_size)

        async with aiohttp.ClientSession() as session:
            tasks = []

            for i, domain in enumerate(domains, 1):
                task = self.check_domain(session, domain, semaphore)
                tasks.append(task)

                # Processa em lotes
                if len(tasks) >= self.batch_size or i == total:
                    results = await asyncio.gather(*tasks, return_exceptions=True)

                    for result in results:
                        if isinstance(result, str):
                            self.disponiveis.add(result)

                    # Log de progresso
                    progress = (self.verificados / total) * 100
                    self.logger.info(
                        f"📊 Progresso: {self.verificados}/{total} ({progress:.1f}%) | "
                        f"Disponíveis: {len(self.disponiveis)} | Erros: {self.erros}"
                    )

                    tasks = []

                    # Pausa entre lotes (exceto no último)
                    if i < total:
                        await asyncio.sleep(self.batch_delay)

        # Salva resultados
        self.save_results(output_file)

        self.logger.info("=" * 60)
        self.logger.info(f"✨ Verificação concluída!")
        self.logger.info(f"📊 Total verificado: {self.verificados}/{total}")
        self.logger.info(f"✅ Domínios disponíveis: {len(self.disponiveis)}")
        self.logger.info(f"❌ Erros: {self.erros}")
        self.logger.info(f"💾 Resultados salvos em: {output_file}")
        self.logger.info("=" * 60)

    def save_results(self, output_file: str):
        """
        Salva os domínios disponíveis em um arquivo CSV

        Args:
            output_file: Caminho do arquivo de saída
        """
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['dominio', 'verificado_em'])

            timestamp = datetime.now().isoformat()
            for domain in sorted(self.disponiveis):
                writer.writerow([domain, timestamp])

        self.logger.info(f"💾 {len(self.disponiveis)} domínios salvos em {output_file}")


def generate_domains(pattern: str = "3letters") -> List[str]:
    """
    Gera lista de domínios baseada no padrão

    Args:
        pattern: Padrão de geração ('3letters', '2letters', '4letters', ou 'custom:abc')

    Returns:
        Lista de domínios gerados
    """
    if pattern == "3letters":
        letras = 'abcdefghijklmnopqrstuvwxyz'
        combos = itertools.product(letras, repeat=3)
    elif pattern == "2letters":
        letras = 'abcdefghijklmnopqrstuvwxyz'
        combos = itertools.product(letras, repeat=2)
    elif pattern == "4letters":
        letras = 'abcdefghijklmnopqrstuvwxyz'
        combos = itertools.product(letras, repeat=4)
    elif pattern.startswith("custom:"):
        letras = pattern.split(":", 1)[1]
        combos = itertools.product(letras, repeat=3)
    else:
        raise ValueError(f"Padrão desconhecido: {pattern}")

    return [f"{''.join(combo)}.com.br" for combo in combos]


def load_proxies(proxy_file: str) -> List[str]:
    """
    Carrega proxies de um arquivo

    Args:
        proxy_file: Caminho do arquivo com proxies (um por linha)

    Returns:
        Lista de proxies
    """
    proxies = []
    try:
        with open(proxy_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    proxies.append(line)
    except FileNotFoundError:
        pass

    return proxies


def main():
    """
    Função principal com argumentos de linha de comando
    """
    parser = argparse.ArgumentParser(
        description='Verificador Assíncrono de Domínios .com.br - Versão Avançada',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:

  # Verificar domínios de 3 letras (padrão)
  python domain_checker_advanced.py

  # Verificar com 100 requisições simultâneas
  python domain_checker_advanced.py --batch-size 100 --batch-delay 0.5

  # Usar proxies
  python domain_checker_advanced.py --proxy-file proxies.txt

  # Testar apenas algumas letras
  python domain_checker_advanced.py --pattern custom:abc

  # Domínios de 2 letras
  python domain_checker_advanced.py --pattern 2letters

  # Especificar arquivo de saída
  python domain_checker_advanced.py --output dominios_disponiveis.csv
        """
    )

    parser.add_argument(
        '--pattern',
        default='3letters',
        help='Padrão de geração: 3letters, 2letters, 4letters, ou custom:abc (padrão: 3letters)'
    )
    parser.add_argument(
        '--batch-size',
        type=int,
        default=50,
        help='Quantidade de requisições simultâneas (padrão: 50)'
    )
    parser.add_argument(
        '--batch-delay',
        type=float,
        default=1.0,
        help='Delay entre lotes em segundos (padrão: 1.0)'
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=10,
        help='Timeout para requisições em segundos (padrão: 10)'
    )
    parser.add_argument(
        '--max-retries',
        type=int,
        default=3,
        help='Número máximo de tentativas por domínio (padrão: 3)'
    )
    parser.add_argument(
        '--proxy-file',
        help='Arquivo com lista de proxies (um por linha)'
    )
    parser.add_argument(
        '--output',
        default='disponiveis.csv',
        help='Arquivo de saída para domínios disponíveis (padrão: disponiveis.csv)'
    )
    parser.add_argument(
        '--log-file',
        help='Arquivo para salvar logs (padrão: domain_checker_YYYYMMDD_HHMMSS.log)'
    )

    args = parser.parse_args()

    # Configurar arquivo de log padrão
    if not args.log_file:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        args.log_file = f'domain_checker_{timestamp}.log'

    # Configurar logging
    logger = setup_logging(args.log_file)

    logger.info("=" * 60)
    logger.info("🔍 Verificador Assíncrono de Domínios .com.br - Versão Avançada")
    logger.info("=" * 60)

    # Carregar proxies se especificado
    proxies = []
    if args.proxy_file:
        proxies = load_proxies(args.proxy_file)
        if proxies:
            logger.info(f"✅ {len(proxies)} proxies carregados de {args.proxy_file}")
        else:
            logger.warning(f"⚠️ Nenhum proxy encontrado em {args.proxy_file}")

    # Gerar lista de domínios
    try:
        domains = generate_domains(args.pattern)
        logger.info(f"📝 {len(domains)} domínios gerados com padrão '{args.pattern}'")
    except ValueError as e:
        logger.error(f"❌ Erro ao gerar domínios: {e}")
        sys.exit(1)

    # Criar verificador
    checker = DomainChecker(
        logger=logger,
        proxies=proxies,
        batch_size=args.batch_size,
        batch_delay=args.batch_delay,
        timeout=args.timeout,
        max_retries=args.max_retries
    )

    # Executar verificação
    try:
        asyncio.run(checker.verify_domains(domains, args.output))
    except KeyboardInterrupt:
        logger.info("\n⚠️ Verificação interrompida pelo usuário")
        if checker.disponiveis:
            checker.save_results(args.output)
        sys.exit(0)
    except Exception as e:
        logger.error(f"❌ Erro fatal: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
