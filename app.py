#!/usr/bin/env python3
"""
OSINTLAB - Open Source Intelligence Laboratory
Interface UI principal com Streamlit
"""

import streamlit as st
from pathlib import Path
import sys

# Adiciona o diretório raiz ao path
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

# Configuração da página
st.set_page_config(
    page_title="OSINTLAB",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/prof-ramos/OSINTLAB',
        'Report a bug': 'https://github.com/prof-ramos/OSINTLAB/issues',
        'About': """
        # OSINTLAB
        ### Open Source Intelligence Laboratory

        Um laboratório completo para ferramentas de OSINT.

        **Desenvolvido por:** Gabriel Ramos
        **Licença:** MIT
        """
    }
)

# CSS customizado
st.markdown("""
<style>
    /* Estilo principal */
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(120deg, #2196F3 0%, #21CBF3 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    .sub-header {
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }

    /* Cards de ferramentas */
    .tool-card {
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        background: white;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
        cursor: pointer;
    }

    .tool-card:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }

    .tool-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }

    .tool-title {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .tool-description {
        color: #666;
        font-size: 0.9rem;
    }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }

    .badge-new {
        background: #4CAF50;
        color: white;
    }

    .badge-beta {
        background: #FF9800;
        color: white;
    }

    .badge-soon {
        background: #9E9E9E;
        color: white;
    }

    /* Sidebar */
    .sidebar-info {
        padding: 1rem;
        background: #f5f5f5;
        border-radius: 8px;
        margin-top: 1rem;
    }

    /* Botões */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Função principal da aplicação"""

    # Sidebar com navegação
    with st.sidebar:
        st.markdown("# 🔍 OSINTLAB")
        st.markdown("---")

        # Menu de navegação
        page = st.radio(
            "Navegação",
            ["🏠 Home", "🌐 Domain Checker", "📊 Sobre"],
            label_visibility="collapsed"
        )

        st.markdown("---")

        # Informações da sidebar
        st.markdown("""
        <div class="sidebar-info">
            <h4>ℹ️ Sobre o OSINTLAB</h4>
            <p style="font-size: 0.9rem;">
                Laboratório completo de ferramentas OSINT para investigações digitais.
            </p>
        </div>
        """, unsafe_allow_html=True)

        # Estatísticas
        st.markdown("### 📈 Estatísticas")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Ferramentas", "1", delta="Ativa")
        with col2:
            st.metric("Em Breve", "6+", delta="Desenvolvimento")

        # Links úteis
        st.markdown("---")
        st.markdown("### 🔗 Links Úteis")
        st.markdown("""
        - [📖 Documentação](https://github.com/prof-ramos/OSINTLAB)
        - [🐛 Reportar Bug](https://github.com/prof-ramos/OSINTLAB/issues)
        - [⭐ GitHub](https://github.com/prof-ramos/OSINTLAB)
        """)

    # Conteúdo principal baseado na navegação
    if page == "🏠 Home":
        show_home()
    elif page == "🌐 Domain Checker":
        from ui.pages.domain_checker import show_domain_checker
        show_domain_checker()
    elif page == "📊 Sobre":
        show_about()

def show_home():
    """Página inicial com lista de ferramentas"""

    st.markdown('<h1 class="main-header">🔍 OSINTLAB</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Open Source Intelligence Laboratory</p>', unsafe_allow_html=True)

    st.markdown("""
    Bem-vindo ao **OSINTLAB**, seu laboratório completo de ferramentas OSINT para investigações digitais.
    Selecione uma ferramenta no menu lateral para começar.
    """)

    st.markdown("---")
    st.markdown("## 🛠️ Ferramentas Disponíveis")

    # Grid de ferramentas
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="tool-card">
            <div class="tool-icon">🌐</div>
            <div class="tool-title">Domain Checker</div>
            <div style="margin-bottom: 0.5rem;">
                <span class="badge badge-new">NOVO</span>
            </div>
            <div class="tool-description">
                Verificador assíncrono de domínios .com.br usando a API oficial do Registro.br.
                Suporta proxy rotativo e logging em tempo real.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="tool-card">
            <div class="tool-icon">🔎</div>
            <div class="tool-title">Sherlock</div>
            <div style="margin-bottom: 0.5rem;">
                <span class="badge badge-soon">EM BREVE</span>
            </div>
            <div class="tool-description">
                Localização de contas em redes sociais.
                Busca usernames em centenas de plataformas.
            </div>
        </div>
        """, unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown("""
        <div class="tool-card">
            <div class="tool-icon">🕷️</div>
            <div class="tool-title">Spider</div>
            <div style="margin-bottom: 0.5rem;">
                <span class="badge badge-soon">EM BREVE</span>
            </div>
            <div class="tool-description">
                Rastreamento e coleta de dados web.
                Crawling inteligente de websites.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown("""
        <div class="tool-card">
            <div class="tool-icon">📧</div>
            <div class="tool-title">Holehe</div>
            <div style="margin-bottom: 0.5rem;">
                <span class="badge badge-soon">EM BREVE</span>
            </div>
            <div class="tool-description">
                Verificação de contas de email.
                Descubra onde um email está cadastrado.
            </div>
        </div>
        """, unsafe_allow_html=True)

    col5, col6 = st.columns(2)

    with col5:
        st.markdown("""
        <div class="tool-card">
            <div class="tool-icon">👤</div>
            <div class="tool-title">Maigret</div>
            <div style="margin-bottom: 0.5rem;">
                <span class="badge badge-soon">EM BREVE</span>
            </div>
            <div class="tool-description">
                Busca avançada de perfis em plataformas.
                Coleta informações detalhadas.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col6:
        st.markdown("""
        <div class="tool-card">
            <div class="tool-icon">🌍</div>
            <div class="tool-title">Whois</div>
            <div style="margin-bottom: 0.5rem;">
                <span class="badge badge-soon">EM BREVE</span>
            </div>
            <div class="tool-description">
                Consultas de domínio e IP.
                Informações de registro e histórico.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Quick Start
    st.markdown("## 🚀 Quick Start")

    st.info("""
    **Para começar:**
    1. Selecione uma ferramenta no menu lateral
    2. Configure os parâmetros necessários
    3. Execute a análise
    4. Exporte os resultados
    """)

    # Estatísticas gerais
    st.markdown("---")
    st.markdown("## 📊 Visão Geral")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Ferramentas Ativas",
            value="1",
            delta="Domain Checker",
            delta_color="normal"
        )

    with col2:
        st.metric(
            label="Em Desenvolvimento",
            value="5",
            delta="Em breve",
            delta_color="normal"
        )

    with col3:
        st.metric(
            label="Contribuidores",
            value="1+",
            delta="Open Source"
        )

    with col4:
        st.metric(
            label="Licença",
            value="MIT",
            delta="Código Aberto"
        )

def show_about():
    """Página sobre o projeto"""

    st.markdown("# 📊 Sobre o OSINTLAB")

    st.markdown("""
    ## 🎯 Missão

    O **OSINTLAB** é um laboratório completo para ferramentas de Open Source Intelligence (OSINT),
    reunindo e aprimorando as melhores ferramentas disponíveis para investigações digitais.

    ## 🌟 Objetivos

    - **Centralizar** ferramentas OSINT em um único ambiente
    - **Facilitar** o acesso através de interface intuitiva
    - **Automatizar** processos de investigação digital
    - **Educar** sobre técnicas e ferramentas OSINT
    - **Promover** uso ético e responsável

    ## 🛠️ Tecnologias

    - **Python 3.8+** - Linguagem principal
    - **Streamlit** - Interface web interativa
    - **aiohttp** - Requisições assíncronas
    - **asyncio** - Processamento paralelo

    ## 👨‍💻 Desenvolvimento

    Este projeto é desenvolvido e mantido por **Gabriel Ramos** e a comunidade open source.

    ### Contribua

    Contribuições são bem-vindas! Visite nosso [GitHub](https://github.com/prof-ramos/OSINTLAB)
    para reportar bugs, sugerir features ou contribuir com código.

    ## ⚠️ Aviso Legal

    Este projeto é destinado **exclusivamente** para fins educacionais e de pesquisa ética.

    Os usuários são responsáveis por:
    - ✅ Usar as ferramentas de forma ética e legal
    - ✅ Respeitar a privacidade e os termos de serviço
    - ✅ Obter autorização quando necessário
    - ❌ NÃO usar para fins maliciosos ou ilegais

    ## 📄 Licença

    **MIT License** - Código aberto e gratuito para uso pessoal e comercial.

    ## 📞 Contato

    - **GitHub:** [@prof-ramos](https://github.com/prof-ramos)
    - **Projeto:** [OSINTLAB](https://github.com/prof-ramos/OSINTLAB)

    ---

    ### ⭐ Se este projeto foi útil, considere dar uma estrela no GitHub!
    """)

    # Versão e informações do sistema
    st.markdown("---")
    st.markdown("### 🔧 Informações do Sistema")

    col1, col2 = st.columns(2)

    with col1:
        st.code(f"""
Versão: 1.0.0
Python: {sys.version.split()[0]}
Streamlit: {st.__version__}
        """)

    with col2:
        st.code(f"""
Ambiente: Production
Status: ✅ Online
Última atualização: 2025-11-06
        """)

if __name__ == "__main__":
    main()
