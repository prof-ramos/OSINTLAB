# 🌐 Verificador Assíncrono de Domínios .com.br

Uma ferramenta OSINT poderosa e rápida para verificar a disponibilidade de domínios .com.br usando a API oficial do Registro.br.

## 📋 Características

### Versão Básica (`domain_checker_basic.py`)
- ✅ Verificação assíncrona de domínios
- ✅ API oficial do Registro.br
- ✅ Saída em CSV
- ✅ Simples e direto

### Versão Avançada (`domain_checker_advanced.py`)
- ⚡ Verificação assíncrona ultra-rápida
- 🔄 Suporte a proxy rotativo
- 📝 Logging em tempo real (arquivo + terminal)
- 🔁 Retry logic com backoff exponencial
- 📊 Relatório de progresso em tempo real
- ⚙️ Altamente configurável via CLI
- 🎯 Múltiplos padrões de geração de domínios
- 💪 Tratamento robusto de erros
- 🛑 Interrupção segura (Ctrl+C)

## 🚀 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação das dependências

```bash
# Clone o repositório OSINTLAB (se ainda não fez)
git clone https://github.com/seu-usuario/OSINTLAB.git
cd OSINTLAB/tools/domain-checker

# Crie um ambiente virtual (recomendado)
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
```

## 📖 Uso

### Versão Básica

Verificação simples de domínios de 3 letras:

```bash
python domain_checker_basic.py
```

**Saída:**
- `disponiveis_async.csv` - Lista de domínios disponíveis

### Versão Avançada

#### Uso Básico

```bash
# Verificar domínios de 3 letras (padrão)
python domain_checker_advanced.py
```

#### Exemplos Avançados

```bash
# Verificar domínios de 2 letras
python domain_checker_advanced.py --pattern 2letters

# Verificar domínios de 4 letras
python domain_checker_advanced.py --pattern 4letters

# Testar apenas algumas letras (ideal para testes)
python domain_checker_advanced.py --pattern custom:abc

# Aumentar velocidade (100 requisições simultâneas)
python domain_checker_advanced.py --batch-size 100 --batch-delay 0.5

# Usar proxies para evitar bloqueios
python domain_checker_advanced.py --proxy-file proxies.txt

# Especificar arquivo de saída customizado
python domain_checker_advanced.py --output meus_dominios.csv

# Configuração completa para máxima velocidade
python domain_checker_advanced.py \
  --pattern 3letters \
  --batch-size 100 \
  --batch-delay 0.3 \
  --timeout 15 \
  --max-retries 5 \
  --proxy-file proxies.txt \
  --output resultado.csv
```

#### Opções da Linha de Comando

```
Opções disponíveis:

  --pattern PATTERN         Padrão de geração de domínios:
                           - 3letters: domínios de 3 letras (aaa a zzz) - 17.576 domínios
                           - 2letters: domínios de 2 letras (aa a zz) - 676 domínios
                           - 4letters: domínios de 4 letras (aaaa a zzzz) - 456.976 domínios
                           - custom:abc: apenas letras especificadas (ex: abc)
                           Padrão: 3letters

  --batch-size N           Quantidade de requisições simultâneas (padrão: 50)
                           Valores maiores = mais rápido, mas maior chance de bloqueio
                           Recomendado: 50-100

  --batch-delay SEGUNDOS   Delay entre lotes em segundos (padrão: 1.0)
                           Valores menores = mais rápido, mas maior chance de bloqueio
                           Recomendado: 0.5-2.0

  --timeout SEGUNDOS       Timeout para cada requisição (padrão: 10)

  --max-retries N          Número máximo de tentativas por domínio (padrão: 3)

  --proxy-file ARQUIVO     Arquivo com lista de proxies (um por linha)
                           Formato: protocolo://host:porta
                           Exemplo: http://proxy.exemplo.com:8080

  --output ARQUIVO         Arquivo de saída CSV (padrão: disponiveis.csv)

  --log-file ARQUIVO       Arquivo para salvar logs detalhados
                           Padrão: domain_checker_YYYYMMDD_HHMMSS.log

  -h, --help              Mostra esta mensagem de ajuda
```

## 🔄 Configuração de Proxies

Para usar proxies (recomendado para verificações em massa):

1. Copie o arquivo de exemplo:
```bash
cp proxies.txt.example proxies.txt
```

2. Edite `proxies.txt` e adicione seus proxies (um por linha):
```
http://proxy1.exemplo.com:8080
http://proxy2.exemplo.com:3128
http://usuario:senha@proxy3.exemplo.com:8080
```

3. Execute com o parâmetro `--proxy-file`:
```bash
python domain_checker_advanced.py --proxy-file proxies.txt
```

## 📊 Formato de Saída

O arquivo CSV gerado contém:

```csv
dominio,verificado_em
abc.com.br,2025-11-06T15:30:45.123456
xyz.com.br,2025-11-06T15:30:45.123456
```

## 🎯 Estratégias de Uso

### Para Testes
```bash
# Testar apenas 27 domínios (aaa a azz)
python domain_checker_advanced.py --pattern custom:abc
```

### Para Velocidade Máxima
```bash
# Configuração agressiva com proxies
python domain_checker_advanced.py \
  --batch-size 150 \
  --batch-delay 0.3 \
  --proxy-file proxies.txt
```

### Para Estabilidade Máxima
```bash
# Configuração conservadora sem bloqueios
python domain_checker_advanced.py \
  --batch-size 30 \
  --batch-delay 2.0 \
  --max-retries 5
```

## ⚡ Performance

### Domínios de 3 Letras (17.576 domínios)

| Configuração | Tempo Estimado | Requisições/s |
|--------------|----------------|---------------|
| Conservadora | ~6-8 horas     | ~0.6 req/s    |
| Padrão       | ~2-3 horas     | ~1.6 req/s    |
| Agressiva    | ~30-60 min     | ~5-10 req/s   |

**Nota:** Tempos reais variam com conexão de internet, proxies e taxa de resposta do Registro.br.

## 📝 Logs

A versão avançada gera logs detalhados:

```
2025-11-06 15:30:45 - INFO - 🚀 Iniciando verificação de 17576 domínios
2025-11-06 15:30:45 - INFO - ⚙️ Configuração: batch_size=50, delay=1.0s
2025-11-06 15:30:50 - INFO - ✅ abc.com.br DISPONÍVEL
2025-11-06 15:30:51 - INFO - 📊 Progresso: 50/17576 (0.3%) | Disponíveis: 3 | Erros: 0
...
2025-11-06 17:45:30 - INFO - ✨ Verificação concluída!
2025-11-06 17:45:30 - INFO - 📊 Total verificado: 17576/17576
2025-11-06 17:45:30 - INFO - ✅ Domínios disponíveis: 127
2025-11-06 17:45:30 - INFO - 💾 Resultados salvos em: disponiveis.csv
```

## 🛡️ Boas Práticas

### Evitando Bloqueios
1. **Use delays adequados:** Não reduza `--batch-delay` abaixo de 0.5s sem proxies
2. **Use proxies:** Para verificações em massa, proxies são essenciais
3. **Respeite rate limits:** O Registro.br pode bloquear IPs com requisições excessivas
4. **Teste primeiro:** Use `--pattern custom:abc` para testar sua configuração

### Responsabilidade
- ⚠️ Use esta ferramenta de forma ética e responsável
- 📜 Respeite os Termos de Uso do Registro.br
- 🤝 Não sobrecarregue a infraestrutura do Registro.br
- 🎯 Use apenas para fins legítimos (pesquisa, análise, registro legal)

## 🐛 Troubleshooting

### Erro: "Timeout"
- Aumente `--timeout` (ex: `--timeout 20`)
- Reduza `--batch-size` (ex: `--batch-size 30`)
- Aumente `--batch-delay` (ex: `--batch-delay 2.0`)

### Erro: "Muitos erros"
- Você pode estar sendo bloqueado
- Use proxies: `--proxy-file proxies.txt`
- Reduza a velocidade: `--batch-size 30 --batch-delay 2.0`

### Verificação Muito Lenta
- Aumente `--batch-size` (ex: `--batch-size 100`)
- Reduza `--batch-delay` (ex: `--batch-delay 0.5`)
- Use proxies para distribuir requisições

### Interromper Verificação
- Pressione `Ctrl+C` - os resultados parciais serão salvos automaticamente

## 🔧 Desenvolvimento

### Estrutura do Código

```
domain-checker/
├── domain_checker_basic.py      # Versão simples
├── domain_checker_advanced.py   # Versão completa
├── requirements.txt             # Dependências
├── proxies.txt.example          # Exemplo de proxies
├── .gitignore                   # Arquivos ignorados
└── README.md                    # Esta documentação
```

### Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o repositório OSINTLAB
2. Crie uma branch para sua feature
3. Faça suas alterações
4. Envie um Pull Request

## 📄 Licença

Este projeto faz parte do OSINTLAB e está licenciado sob a Licença MIT.

## ⚠️ Aviso Legal

Esta ferramenta é destinada exclusivamente para fins educacionais, de pesquisa e uso legítimo. Os usuários são responsáveis por:
- Respeitar os Termos de Uso do Registro.br
- Não usar para fins maliciosos ou ilegais
- Não sobrecarregar a infraestrutura do Registro.br
- Usar de forma ética e responsável

Os desenvolvedores não se responsabilizam por uso indevido desta ferramenta.

## 📞 Suporte

Para problemas, sugestões ou dúvidas:
- Abra uma issue no repositório OSINTLAB
- Entre em contato com a equipe de desenvolvimento

---

⭐ Se esta ferramenta foi útil, considere dar uma estrela no repositório!

**Desenvolvido com ❤️ para a comunidade OSINT**
