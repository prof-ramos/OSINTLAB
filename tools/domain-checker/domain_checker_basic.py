#!/usr/bin/env python3
"""
Verificador Assíncrono de Domínios .com.br - Versão Básica
Verifica simultaneamente a disponibilidade de domínios usando a API do Registro.br
"""

import asyncio
import aiohttp
import itertools
import csv

API_URL = "https://registro.br/v2/ajax/avail/raw/"  # endpoint interno usado pelo site do registro.br

async def check_domain(session, domain):
    """
    Verifica se um domínio está disponível

    Args:
        session: Sessão aiohttp
        domain: Nome do domínio a verificar

    Returns:
        str: Nome do domínio se disponível, None caso contrário
    """
    try:
        async with session.get(API_URL + domain) as resp:
            data = await resp.text()
            if "disponível" in data.lower():
                print(f"✅ {domain} disponível")
                return domain
            else:
                print(f"❌ {domain} ocupado")
                return None
    except Exception as e:
        print(f"⚠️ Erro ao verificar {domain}: {e}")
        return None

async def main():
    """
    Função principal que coordena a verificação de domínios
    """
    letras = 'abcdefghijklmnopqrstuvwxyz'
    tasks = []
    disponiveis = []

    async with aiohttp.ClientSession() as session:
        for combo in itertools.product(letras, repeat=3):
            dominio = f"{''.join(combo)}.com.br"
            tasks.append(check_domain(session, dominio))

            # Limita a quantidade de requisições simultâneas para não ser bloqueado
            if len(tasks) >= 50:
                results = await asyncio.gather(*tasks)
                disponiveis.extend([r for r in results if r])
                tasks = []
                await asyncio.sleep(1)  # pausa curta entre os blocos

        # Processa as tarefas restantes
        if tasks:
            results = await asyncio.gather(*tasks)
            disponiveis.extend([r for r in results if r])

    # Salva resultados
    with open("disponiveis_async.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["dominio"])
        for d in disponiveis:
            writer.writerow([d])

    print(f"\n✨ Verificação concluída! {len(disponiveis)} domínios disponíveis salvos em disponiveis_async.csv")

if __name__ == "__main__":
    asyncio.run(main())
