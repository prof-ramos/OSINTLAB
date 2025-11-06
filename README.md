# 🔍 OSINTLAB

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Um laboratório completo para ferramentas de Open Source Intelligence (OSINT), reunindo e aprimorando as melhores ferramentas disponíveis para investigações digitais.

## 📋 Sobre

O OSINTLAB é um repositório dedicado ao desenvolvimento e aprimoramento de ferramentas OSINT. Nosso objetivo é fornecer um ambiente unificado para pesquisadores de segurança, jornalistas investigativos e profissionais de OSINT, com ferramentas confiáveis e atualizadas.

### 🛠️ Ferramentas Incluídas

- **Domain Checker** ⚡ - Verificador assíncrono de domínios .com.br com API do Registro.br
- **Sherlock** - Localização de contas em redes sociais (forks aprimorados)
- **Spider** - Rastreamento e coleta de dados web
- **Archive** - Análise de dados arquivados e históricos
- **Maigret** - Busca avançada de perfis em plataformas
- **Holehe** - Verificação de contas de email
- **Whois** - Consultas de domínio e IP
- *E muitas outras ferramentas em desenvolvimento*

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- Git
- pip para gerenciamento de dependências

### Instalação Rápida

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/prof-ramos/OSINTLAB.git
   cd OSINTLAB
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Inicie a interface web:**
   ```bash
   # Linux/macOS
   ./run.sh

   # Windows
   run.bat

   # Ou diretamente com Streamlit
   streamlit run app.py
   ```

4. **Acesse a interface:**

   Abra seu navegador em: **http://localhost:8501**

   🎉 Pronto! Agora você pode usar todas as ferramentas através da interface web intuitiva.

## 📖 Uso

### 🖥️ Interface Web (Recomendado)

A forma mais fácil de usar o OSINTLAB é através da **interface web com Streamlit**:

```bash
# Inicie a interface
./run.sh  # Linux/macOS
run.bat   # Windows

# Ou diretamente
streamlit run app.py
```

Acesse: **http://localhost:8501**

**Recursos da Interface:**
- ✅ Navegação intuitiva entre ferramentas
- ✅ Formulários interativos
- ✅ Visualização de resultados em tempo real
- ✅ Export de dados (CSV, JSON, etc.)
- ✅ Dashboards e gráficos
- ✅ Documentação integrada

### 💻 Linha de Comando (Avançado)

Para usuários avançados, todas as ferramentas também podem ser usadas via CLI:

```bash
# Verificar domínios .com.br (CLI)
cd tools/domain-checker
python domain_checker_advanced.py --pattern custom:abc

# Com configurações avançadas
python domain_checker_advanced.py \
  --pattern 3letters \
  --batch-size 100 \
  --batch-delay 0.5 \
  --proxy-file proxies.txt

# Teste rápido
python test_quick.py
```

## 📁 Estrutura do Projeto

```
OSINTLAB/
├── app.py              # Aplicação principal Streamlit
├── run.sh              # Script de inicialização (Linux/macOS)
├── run.bat             # Script de inicialização (Windows)
├── requirements.txt    # Dependências do projeto
├── .streamlit/         # Configurações do Streamlit
│   └── config.toml
├── ui/                 # Interface do usuário
│   ├── pages/          # Páginas individuais
│   │   └── domain_checker.py
│   ├── components/     # Componentes reutilizáveis
│   └── utils/          # Utilitários da UI
├── tools/              # Ferramentas OSINT
│   ├── domain-checker/ # Verificação de domínios .com.br
│   │   ├── domain_checker_basic.py
│   │   ├── domain_checker_advanced.py
│   │   ├── test_quick.py
│   │   ├── requirements.txt
│   │   └── README.md
│   ├── sherlock/       # Localização de contas (Em breve)
│   ├── maigret/        # Busca de perfis (Em breve)
│   └── holehe/         # Verificação de emails (Em breve)
└── README.md           # Este arquivo
```

## 🎨 Interface Web

O OSINTLAB possui uma interface web moderna e intuitiva construída com **Streamlit**.

### Características da UI

- 🎯 **Navegação Simples** - Menu lateral com acesso rápido a todas as ferramentas
- 📊 **Visualização em Tempo Real** - Acompanhe o progresso das análises
- 💾 **Export de Dados** - Baixe resultados em CSV, JSON e outros formatos
- 📈 **Dashboards Interativos** - Gráficos e visualizações dinâmicas
- 📚 **Documentação Integrada** - Tutoriais e exemplos dentro da interface
- ⚙️ **Configurações Avançadas** - Controle total sobre os parâmetros

### Adicionando Novas Ferramentas à UI

Para adicionar uma nova ferramenta à interface:

1. Crie um arquivo em `ui/pages/` com o nome da ferramenta:
   ```python
   # ui/pages/minha_ferramenta.py
   import streamlit as st

   def show_minha_ferramenta():
       st.markdown("# 🔧 Minha Ferramenta")
       # Sua implementação aqui
   ```

2. Adicione a ferramenta ao menu em `app.py`:
   ```python
   # No menu de navegação
   page = st.radio(
       "Navegação",
       ["🏠 Home", "🌐 Domain Checker", "🔧 Minha Ferramenta", "📊 Sobre"]
   )

   # No conteúdo principal
   elif page == "🔧 Minha Ferramenta":
       from ui.pages.minha_ferramenta import show_minha_ferramenta
       show_minha_ferramenta()
   ```

3. Atualize o card da ferramenta na home page em `app.py`

4. Pronto! A ferramenta estará disponível na interface.

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

### Diretrizes de Contribuição

- Siga o estilo de código PEP 8
- Adicione testes para novas funcionalidades
- Atualize a documentação conforme necessário
- Mantenha compatibilidade com Python 3.8+
- Ao adicionar ferramentas, integre-as à interface web

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## ⚠️ Aviso Legal

Este projeto é destinado exclusivamente para fins educacionais e de pesquisa ética. Os usuários são responsáveis pelo uso adequado das ferramentas. Não nos responsabilizamos por uso indevido ou ilegal das ferramentas fornecidas.

## 📞 Contato

- **Autor:** Gabriel Ramos
- **Email:** seu-email@exemplo.com
- **GitHub:** [@seu-usuario](https://github.com/seu-usuario)

---

⭐ Se este projeto foi útil para você, considere dar uma estrela!
