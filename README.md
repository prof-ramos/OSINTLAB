# 🔍 OSINTLAB

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Um laboratório completo para ferramentas de Open Source Intelligence (OSINT), reunindo e aprimorando as melhores ferramentas disponíveis para investigações digitais.

## 📋 Sobre

O OSINTLAB é um repositório dedicado ao desenvolvimento e aprimoramento de ferramentas OSINT. Nosso objetivo é fornecer um ambiente unificado para pesquisadores de segurança, jornalistas investigativos e profissionais de OSINT, com ferramentas confiáveis e atualizadas.

### 🛠️ Ferramentas Incluídas

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
- pip ou poetry para gerenciamento de dependências

### Passos de Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/osintlab.git
   cd osintlab
   ```

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   # ou se usar poetry:
   poetry install
   ```

3. **Configure as variáveis de ambiente (opcional):**
   ```bash
   cp .env.example .env
   # Edite o .env com suas configurações
   ```

## 📖 Uso

### Uso Básico

```bash
# Ativar ambiente virtual (recomendado)
source venv/bin/activate  # ou poetry shell

# Executar uma ferramenta específica
python -m osintlab.sherlock username
python -m osintlab.maigret email@exemplo.com
```

### Exemplos Avançados

```bash
# Busca completa em todas as plataformas
python -m osintlab search --target username --platforms all

# Análise de domínio
python -m osintlab whois exemplo.com

# Rastreamento de IP
python -m osintlab spider --ip 192.168.1.1
```

## 📁 Estrutura do Projeto

```
osintlab/
├── tools/              # Ferramentas individuais
│   ├── sherlock/       # Localização de contas
│   ├── maigret/        # Busca de perfis
│   ├── holehe/         # Verificação de emails
│   └── ...
├── core/               # Núcleo do sistema
├── utils/              # Utilitários compartilhados
├── tests/              # Testes automatizados
└── docs/               # Documentação
```

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
