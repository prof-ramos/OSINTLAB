"""
Domain Checker - Interface UI
Verificador assíncrono de domínios .com.br
"""

import streamlit as st
import asyncio
import aiohttp
import itertools
import pandas as pd
from datetime import datetime
import io
import sys
from pathlib import Path

# Adiciona o diretório tools ao path
ROOT_DIR = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT_DIR / "tools" / "domain-checker"))

def show_domain_checker():
    """Página principal do Domain Checker"""

    st.markdown("# 🌐 Domain Checker")
    st.markdown("Verificador assíncrono de domínios .com.br usando a API oficial do Registro.br")

    st.markdown("---")

    # Tabs para organizar a interface
    tab1, tab2, tab3 = st.tabs(["🔍 Verificar Domínios", "📚 Documentação", "⚙️ Configurações"])

    with tab1:
        show_checker_tab()

    with tab2:
        show_documentation_tab()

    with tab3:
        show_settings_tab()

def show_checker_tab():
    """Tab de verificação de domínios"""

    st.markdown("## 🔍 Verificação de Domínios")

    # Modo de verificação
    mode = st.radio(
        "Modo de Verificação",
        ["🎯 Domínios Específicos", "🔢 Geração Automática"],
        horizontal=True
    )

    if mode == "🎯 Domínios Específicos":
        show_specific_domains_mode()
    else:
        show_auto_generation_mode()

def show_specific_domains_mode():
    """Modo de verificação de domínios específicos"""

    st.markdown("### Digite os domínios que deseja verificar")

    # Input de domínios
    domains_input = st.text_area(
        "Domínios (um por linha)",
        placeholder="exemplo1.com.br\nexemplo2.com.br\nexemplo3.com.br",
        height=150,
        help="Digite um domínio por linha. A extensão .com.br será adicionada automaticamente se não informada."
    )

    col1, col2 = st.columns([3, 1])

    with col2:
        check_button = st.button("🚀 Verificar Domínios", type="primary", use_container_width=True)

    if check_button:
        if not domains_input.strip():
            st.error("❌ Por favor, digite pelo menos um domínio!")
            return

        # Processa a lista de domínios
        domains = []
        for line in domains_input.strip().split('\n'):
            line = line.strip()
            if line:
                # Adiciona .com.br se não tiver
                if not line.endswith('.com.br'):
                    line = f"{line}.com.br"
                domains.append(line)

        if domains:
            st.info(f"🔍 Verificando {len(domains)} domínios...")
            run_domain_check(domains)

def show_auto_generation_mode():
    """Modo de geração automática de domínios"""

    st.markdown("### Configuração de Geração Automática")

    col1, col2 = st.columns(2)

    with col1:
        pattern_type = st.selectbox(
            "Padrão de Geração",
            ["Letras Customizadas", "2 Letras", "3 Letras", "4 Letras"],
            help="Escolha o padrão para gerar os domínios"
        )

    with col2:
        if pattern_type == "Letras Customizadas":
            custom_letters = st.text_input(
                "Letras a usar",
                value="abc",
                max_chars=26,
                help="Digite as letras que deseja usar na geração (ex: abc)"
            ).lower()

    # Calcula quantidade de domínios
    if pattern_type == "Letras Customizadas":
        if custom_letters:
            total_domains = len(custom_letters) ** 3
            st.info(f"📊 Serão gerados **{total_domains:,}** domínios com o padrão '{custom_letters}'")
    elif pattern_type == "2 Letras":
        total_domains = 26 ** 2
        st.info(f"📊 Serão gerados **{total_domains:,}** domínios (aa.com.br até zz.com.br)")
    elif pattern_type == "3 Letras":
        total_domains = 26 ** 3
        st.warning(f"⚠️ Serão gerados **{total_domains:,}** domínios! Isso pode levar várias horas.")
    else:  # 4 Letras
        total_domains = 26 ** 4
        st.error(f"🚨 Serão gerados **{total_domains:,}** domínios! Isso pode levar dias!")

    # Configurações avançadas
    with st.expander("⚙️ Configurações Avançadas"):
        col1, col2 = st.columns(2)

        with col1:
            batch_size = st.slider(
                "Requisições Simultâneas",
                min_value=10,
                max_value=200,
                value=50,
                step=10,
                help="Quantidade de requisições simultâneas. Valores maiores = mais rápido, mas maior risco de bloqueio."
            )

        with col2:
            batch_delay = st.slider(
                "Delay Entre Lotes (segundos)",
                min_value=0.1,
                max_value=5.0,
                value=1.0,
                step=0.1,
                help="Pausa entre lotes de requisições. Valores menores = mais rápido, mas maior risco de bloqueio."
            )

        timeout = st.slider(
            "Timeout (segundos)",
            min_value=5,
            max_value=30,
            value=10,
            help="Tempo máximo de espera por cada requisição"
        )

    # Botão de verificação
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        check_button = st.button("🚀 Iniciar Verificação", type="primary", use_container_width=True)

    if check_button:
        # Gera lista de domínios
        if pattern_type == "Letras Customizadas":
            if not custom_letters:
                st.error("❌ Digite as letras para geração customizada!")
                return
            domains = generate_domains(custom_letters, 3)
        elif pattern_type == "2 Letras":
            domains = generate_domains('abcdefghijklmnopqrstuvwxyz', 2)
        elif pattern_type == "3 Letras":
            if not st.session_state.get('confirmed_3_letters', False):
                st.warning("⚠️ Esta verificação pode levar várias horas!")
                if st.button("✅ Confirmar e Continuar"):
                    st.session_state['confirmed_3_letters'] = True
                    st.rerun()
                return
            domains = generate_domains('abcdefghijklmnopqrstuvwxyz', 3)
        else:  # 4 Letras
            if not st.session_state.get('confirmed_4_letters', False):
                st.error("🚨 Esta verificação pode levar dias!")
                if st.button("✅ Confirmar e Continuar (Não Recomendado)"):
                    st.session_state['confirmed_4_letters'] = True
                    st.rerun()
                return
            domains = generate_domains('abcdefghijklmnopqrstuvwxyz', 4)

        if domains:
            st.info(f"🔍 Verificando {len(domains):,} domínios...")
            run_domain_check(domains, batch_size=batch_size, batch_delay=batch_delay, timeout=timeout)

def generate_domains(letters: str, length: int) -> list:
    """
    Gera lista de domínios baseada em letras e comprimento

    Args:
        letters: Letras a usar
        length: Comprimento das combinações

    Returns:
        Lista de domínios
    """
    combos = itertools.product(letters, length=length)
    return [f"{''.join(combo)}.com.br" for combo in combos]

def run_domain_check(domains: list, batch_size: int = 50, batch_delay: float = 1.0, timeout: int = 10):
    """
    Executa a verificação de domínios

    Args:
        domains: Lista de domínios a verificar
        batch_size: Tamanho do lote
        batch_delay: Delay entre lotes
        timeout: Timeout das requisições
    """

    API_URL = "https://registro.br/v2/ajax/avail/raw/"

    # Containers para UI
    progress_container = st.container()
    results_container = st.container()

    with progress_container:
        progress_bar = st.progress(0)
        status_text = st.empty()
        metrics_cols = st.columns(4)

        with metrics_cols[0]:
            total_metric = st.empty()
        with metrics_cols[1]:
            checked_metric = st.empty()
        with metrics_cols[2]:
            available_metric = st.empty()
        with metrics_cols[3]:
            errors_metric = st.empty()

    # Estado inicial
    total = len(domains)
    checked = 0
    available_domains = []
    errors = 0

    # Atualiza métricas iniciais
    total_metric.metric("Total", f"{total:,}")
    checked_metric.metric("Verificados", "0")
    available_metric.metric("Disponíveis", "0", delta="0")
    errors_metric.metric("Erros", "0")

    async def check_domain(session, domain, semaphore):
        """Verifica um domínio"""
        nonlocal checked, errors

        async with semaphore:
            try:
                async with session.get(
                    API_URL + domain,
                    timeout=aiohttp.ClientTimeout(total=timeout)
                ) as resp:
                    if resp.status == 200:
                        data = await resp.text()
                        checked += 1

                        if "disponível" in data.lower():
                            return domain, True
                        else:
                            return domain, False
                    else:
                        errors += 1
                        return None, None

            except Exception:
                errors += 1
                return None, None

    async def verify_all():
        """Verifica todos os domínios"""
        nonlocal checked, available_domains

        semaphore = asyncio.Semaphore(batch_size)

        async with aiohttp.ClientSession() as session:
            tasks = []

            for i, domain in enumerate(domains, 1):
                task = check_domain(session, domain, semaphore)
                tasks.append(task)

                # Processa em lotes
                if len(tasks) >= batch_size or i == total:
                    results = await asyncio.gather(*tasks, return_exceptions=True)

                    for result in results:
                        if isinstance(result, tuple) and result[0]:
                            domain, is_available = result
                            if is_available:
                                available_domains.append(domain)

                    # Atualiza UI
                    progress = checked / total
                    progress_bar.progress(progress)
                    status_text.text(f"Verificando... {checked:,}/{total:,} ({progress*100:.1f}%)")

                    checked_metric.metric("Verificados", f"{checked:,}")
                    available_metric.metric(
                        "Disponíveis",
                        f"{len(available_domains):,}",
                        delta=f"+{len(available_domains)}"
                    )
                    errors_metric.metric("Erros", f"{errors:,}")

                    tasks = []

                    # Delay entre lotes
                    if i < total:
                        await asyncio.sleep(batch_delay)

    # Executa verificação
    try:
        asyncio.run(verify_all())

        # Mostra resultados
        with results_container:
            st.markdown("---")
            st.markdown("## ✅ Verificação Concluída!")

            if available_domains:
                st.success(f"🎉 **{len(available_domains)}** domínios disponíveis encontrados!")

                # Mostra domínios disponíveis
                df = pd.DataFrame({
                    'Domínio': sorted(available_domains),
                    'Status': ['✅ Disponível'] * len(available_domains),
                    'Verificado em': [datetime.now().strftime('%Y-%m-%d %H:%M:%S')] * len(available_domains)
                })

                st.dataframe(df, use_container_width=True, hide_index=True)

                # Botão de download
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Baixar Resultados (CSV)",
                    data=csv,
                    file_name=f"dominios_disponiveis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    type="primary"
                )
            else:
                st.warning("😕 Nenhum domínio disponível foi encontrado.")

            # Resumo
            st.markdown("### 📊 Resumo")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total Verificado", f"{checked:,}")
            with col2:
                st.metric("Disponíveis", f"{len(available_domains):,}")
            with col3:
                st.metric("Ocupados", f"{checked - len(available_domains):,}")
            with col4:
                st.metric("Erros", f"{errors:,}")

    except Exception as e:
        st.error(f"❌ Erro durante a verificação: {str(e)}")

def show_documentation_tab():
    """Tab de documentação"""

    st.markdown("## 📚 Documentação")

    st.markdown("""
    ### 🌐 Sobre o Domain Checker

    O **Domain Checker** é uma ferramenta OSINT poderosa para verificar a disponibilidade de domínios .com.br
    usando a API oficial do Registro.br.

    ### 🔥 Características

    - ⚡ **Verificação Assíncrona** - Verifica múltiplos domínios simultaneamente
    - 🎯 **Dois Modos de Operação**:
      - Domínios específicos (verificação manual)
      - Geração automática (busca em massa)
    - 📊 **Progresso em Tempo Real** - Acompanhe a verificação ao vivo
    - 💾 **Export CSV** - Baixe os resultados facilmente
    - ⚙️ **Configurável** - Ajuste velocidade e performance

    ### 🚀 Como Usar

    #### Modo 1: Domínios Específicos

    1. Selecione "🎯 Domínios Específicos"
    2. Digite os domínios que deseja verificar (um por linha)
    3. Clique em "Verificar Domínios"
    4. Aguarde os resultados
    5. Baixe o CSV se desejar

    #### Modo 2: Geração Automática

    1. Selecione "🔢 Geração Automática"
    2. Escolha o padrão:
       - **Letras Customizadas**: Use apenas letras específicas (ex: abc)
       - **2 Letras**: Gera 676 domínios (aa a zz)
       - **3 Letras**: Gera 17.576 domínios (aaa a zzz) ⚠️
       - **4 Letras**: Gera 456.976 domínios (aaaa a zzzz) 🚨
    3. Configure parâmetros avançados se necessário
    4. Clique em "Iniciar Verificação"
    5. Aguarde e baixe os resultados

    ### ⚙️ Parâmetros Avançados

    - **Requisições Simultâneas**: Quantidade de domínios verificados ao mesmo tempo
      - Valores baixos (10-30): Mais lento, mais estável
      - Valores médios (50-100): Balanceado (recomendado)
      - Valores altos (100-200): Mais rápido, risco de bloqueio

    - **Delay Entre Lotes**: Pausa entre grupos de requisições
      - 2-5s: Muito seguro, mais lento
      - 1-2s: Balanceado (recomendado)
      - 0.1-1s: Rápido, risco de bloqueio

    - **Timeout**: Tempo máximo de espera por resposta
      - Recomendado: 10 segundos

    ### ⏱️ Tempo Estimado

    | Quantidade | Configuração | Tempo Estimado |
    |------------|-------------|----------------|
    | 10-50 domínios | Qualquer | < 1 minuto |
    | 676 (2 letras) | Padrão | ~15 minutos |
    | 17.576 (3 letras) | Padrão | ~2-3 horas |
    | 17.576 (3 letras) | Agressiva | ~30-60 min |

    ### ⚠️ Boas Práticas

    1. **Teste primeiro**: Use "Letras Customizadas" com poucas letras (ex: abc = 27 domínios)
    2. **Respeite limites**: O Registro.br pode bloquear IPs com requisições excessivas
    3. **Use delays adequados**: Não reduza muito os delays sem necessidade
    4. **Horários**: Evite horários de pico para verificações grandes

    ### 🔒 API do Registro.br

    Esta ferramenta usa o endpoint oficial:
    ```
    https://registro.br/v2/ajax/avail/raw/[dominio]
    ```

    O mesmo usado pelo site oficial do Registro.br.

    ### 📄 Formato do CSV

    O arquivo exportado contém:
    - **Domínio**: Nome do domínio disponível
    - **Status**: Status da verificação
    - **Verificado em**: Data e hora da verificação

    ### 🐛 Problemas Comuns

    **Muitos erros durante a verificação:**
    - Reduza "Requisições Simultâneas"
    - Aumente "Delay Entre Lotes"
    - Verifique sua conexão de internet

    **Verificação muito lenta:**
    - Aumente "Requisições Simultâneas"
    - Reduza "Delay Entre Lotes"
    - Use padrões menores para testes

    **Nenhum domínio disponível:**
    - Normal para padrões comuns (ex: 2 letras)
    - Tente padrões mais específicos
    - Use "Letras Customizadas" com combinações únicas
    """)

def show_settings_tab():
    """Tab de configurações"""

    st.markdown("## ⚙️ Configurações")

    st.info("🚧 Em desenvolvimento. Em breve você poderá configurar proxies e outras opções avançadas.")

    with st.expander("🔄 Configuração de Proxies (Em Breve)"):
        st.markdown("""
        Suporte a proxies será adicionado em breve para:
        - Evitar bloqueios em verificações massivas
        - Distribuir requisições
        - Aumentar velocidade

        Por enquanto, use a versão CLI para suporte a proxies:
        ```bash
        cd tools/domain-checker
        python domain_checker_advanced.py --proxy-file proxies.txt
        ```
        """)

    with st.expander("📊 Histórico de Verificações (Em Breve)"):
        st.markdown("""
        Em breve você poderá visualizar:
        - Histórico de verificações anteriores
        - Estatísticas de uso
        - Domínios salvos
        """)

    with st.expander("🔔 Notificações (Em Breve)"):
        st.markdown("""
        Configuração de notificações quando:
        - Verificação for concluída
        - Domínios específicos ficarem disponíveis
        - Erros ocorrerem
        """)

    st.markdown("---")
    st.markdown("### 🔧 Informações do Sistema")

    col1, col2 = st.columns(2)

    with col1:
        st.code(f"""
Versão: 1.0.0
API: registro.br/v2/ajax/avail
Status: ✅ Online
        """)

    with col2:
        st.code(f"""
Modo: Interface Web
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """)
