#!/usr/bin/env python3
"""
Script de teste rápido para o verificador de domínios
Verifica apenas alguns domínios de teste para validar a instalação
"""

import asyncio
import aiohttp
import sys

API_URL = "https://registro.br/v2/ajax/avail/raw/"

# Domínios de teste (alguns provavelmente disponíveis, outros ocupados)
TEST_DOMAINS = [
    "google.com.br",  # Ocupado
    "facebook.com.br",  # Ocupado
    "xyz123test456.com.br",  # Provavelmente disponível
    "qwerty9876test.com.br",  # Provavelmente disponível
]

async def check_domain(session, domain):
    """Verifica um domínio"""
    try:
        async with session.get(API_URL + domain, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            if resp.status == 200:
                data = await resp.text()
                if "disponível" in data.lower():
                    return domain, "disponível"
                else:
                    return domain, "ocupado"
            else:
                return domain, f"erro: status {resp.status}"
    except Exception as e:
        return domain, f"erro: {str(e)[:50]}"

async def main():
    """Função principal de teste"""
    print("=" * 60)
    print("🧪 Teste Rápido - Verificador de Domínios .com.br")
    print("=" * 60)
    print(f"\n📋 Testando {len(TEST_DOMAINS)} domínios...\n")

    async with aiohttp.ClientSession() as session:
        tasks = [check_domain(session, domain) for domain in TEST_DOMAINS]
        results = await asyncio.gather(*tasks)

    # Exibir resultados
    disponiveis = 0
    ocupados = 0
    erros = 0

    for domain, status in results:
        if status == "disponível":
            print(f"✅ {domain:<30} DISPONÍVEL")
            disponiveis += 1
        elif status == "ocupado":
            print(f"❌ {domain:<30} OCUPADO")
            ocupados += 1
        else:
            print(f"⚠️ {domain:<30} {status}")
            erros += 1

    # Resumo
    print("\n" + "=" * 60)
    print(f"📊 Resumo:")
    print(f"   ✅ Disponíveis: {disponiveis}")
    print(f"   ❌ Ocupados: {ocupados}")
    print(f"   ⚠️ Erros: {erros}")
    print("=" * 60)

    if erros == 0:
        print("\n✨ Teste concluído com sucesso!")
        print("🚀 A ferramenta está funcionando corretamente!\n")
        return 0
    else:
        print("\n⚠️ Alguns erros ocorreram. Verifique sua conexão com a internet.\n")
        return 1

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠️ Teste interrompido pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")
        sys.exit(1)
