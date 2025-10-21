# 🎮 GameFi RADAR BR - Bot de Notícias Automatizado 🚀

Bot inteligente que usa **Claude API** para gerar e postar automaticamente:
- **Resumo Diário** de notícias GameFi/Web3 (09:00)
- **Notícias Relevantes** do setor (13:00 e 18:00)

Canal: **GameFi RADAR BR👾🚀** (@gamefiradarbr)

---

## 📋 Índice

- [Características](#-características)
- [Requisitos](#-requisitos)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Como Usar](#-como-usar)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Comandos Úteis](#-comandos-úteis)
- [Solução de Problemas](#-solução-de-problemas)
- [Deploy no Fly.io](#-deploy-no-flyio)

---

## ✨ Características

✅ **Postagens Automáticas Diárias**
- Resumo diário com 5 notícias (09:00)
- 2 análises detalhadas de notícias relevantes (13:00 e 18:00)

✅ **IA Inteligente (Claude Sonnet 4)**
- Busca notícias atualizadas
- Cria resumos personalizados
- Análise contextual e relevante

✅ **Anti-Duplicação**
- Histórico de postagens
- Evita repetir conteúdo

✅ **Modo de Teste**
- Teste antes de postar no canal
- Visualize conteúdo no terminal

✅ **Logs Detalhados**
- Acompanhe todas as operações
- Debug facilitado

✅ **Temas Específicos**
- GameFi
- Web3 Gaming
- Blockchain Games
- NFT Games
- Crypto Gaming

---

## 🔧 Requisitos

### Software Necessário

- **Python 3.8+** 
- **pip** (gerenciador de pacotes Python)

### Contas e Credenciais

1. **Claude API** (Anthropic)
   - Crie conta em: https://console.anthropic.com/
   - Gere uma API Key

2. **Telegram Bot**
   - Crie bot com @BotFather no Telegram
   - Obtenha o Token

3. **Canal do Telegram**
   - Crie um canal
   - Adicione o bot como administrador

---

## 📥 Instalação

### 1. Clone ou baixe o projeto

```bash
# Se tiver git instalado
git clone <seu-repositorio>
cd gamefi-news-bot

# Ou baixe o ZIP e extraia
```

### 2. Crie ambiente virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale dependências

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuração

### 1. Configure suas credenciais

Edite o arquivo `.env` com suas chaves:

```env
# Claude API
CLAUDE_API_KEY=sk-ant-api03-SEU_TOKEN_AQUI
CLAUDE_MODEL=claude-sonnet-4-20250514

# Telegram Bot
TELEGRAM_BOT_TOKEN=SEU_TOKEN_AQUI
TELEGRAM_CHANNEL_ID=@gamefiradarbr
CHANNEL_NAME=GameFi RADAR BR👾🚀

# Horários (formato 24h - Brasília GMT-3)
SCHEDULE_RESUMO_DIARIO=09:00
SCHEDULE_NOTICIA_RELEVANTE_1=13:00
SCHEDULE_NOTICIA_RELEVANTE_2=18:00

# Modo (test ou production)
MODE=test
```

### 2. Execute o assistente de configuração

```bash
python setup_helper.py
```

Este script vai:
- ✅ Verificar dependências
- ✅ Validar credenciais
- ✅ Testar conexões
- ✅ Configurar tudo automaticamente

---

## 🚀 Como Usar

### Modo Teste (Recomendado primeiro)

```bash
# 1. Configure MODE=test no .env
# 2. Execute o menu de testes
python test_bot.py
```

**Menu de Testes:**
- Validar todas as configurações
- Testar Claude API
- Testar Telegram Bot
- Gerar conteúdo de teste
- Executar postagens imediatamente (sem postar no canal)

### Modo Produção

```bash
# 1. Configure MODE=production no .env
# 2. Execute o bot
python main.py
```

O bot ficará rodando e postará automaticamente nos horários configurados.

**Para parar o bot:** Pressione `Ctrl+C`

---

## 📁 Estrutura do Projeto

```
gamefi-news-bot/
├── config/
│   ├── config.py           # Configurações centralizadas
│   └── prompts.py          # Templates de prompts personalizados
├── src/
│   ├── ai_processor.py     # Processamento com Claude API
│   ├── telegram_bot.py     # Gerenciamento do Telegram
│   └── scheduler.py        # Sistema de agendamento
├── utils/
│   ├── logger.py           # Sistema de logs
│   └── database.py         # Histórico de postagens
├── data/
│   └── posted_news.json    # Banco de dados local
├── logs/
│   └── bot.log             # Logs do bot
├── .env                    # Suas credenciais (NÃO compartilhar!)
├── .gitignore              # Proteção de arquivos sensíveis
├── requirements.txt        # Dependências Python
├── setup_helper.py         # Assistente de configuração
├── test_bot.py             # Script de testes
├── main.py                 # Executável principal
└── README.md               # Esta documentação
```

---

## 💻 Comandos Úteis

### Testes e Validação

```bash
# Assistente de configuração completo
python setup_helper.py

# Menu interativo de testes
python test_bot.py

# Validar apenas configurações
python config/config.py

# Testar apenas Claude API
python src/ai_processor.py

# Testar apenas Telegram Bot
python src/telegram_bot.py

# Ver logs em tempo real
tail -f logs/bot.log  # Linux/Mac
Get-Content logs/bot.log -Wait  # Windows PowerShell
```

### Execução

```bash
# Rodar bot em modo produção
python main.py

# Rodar em background (Linux/Mac)
nohup python main.py &

# Rodar como serviço (recomendado para produção)
# Ver seção "Deploy no Fly.io"
```

---

## 🔍 Solução de Problemas

### Erro: "CLAUDE_API_KEY não configurada"

**Solução:**
1. Verifique se o arquivo `.env` existe
2. Confirme que a chave está correta
3. Acesse: https://console.anthropic.com/ para gerar nova chave

### Erro: "Telegram Bot não tem permissão"

**Solução:**
1. Abra o canal no Telegram
2. Adicione o bot como **Administrador**
3. Dê permissão de "Postar mensagens"

### Erro: "ModuleNotFoundError"

**Solução:**
```bash
# Reinstale as dependências
pip install -r requirements.txt --force-reinstall
```

### Bot não posta no horário

**Soluções:**
1. Verifique se o MODE está em "production"
2. Confirme o timezone (GMT-3 para Brasília)
3. Veja os logs: `logs/bot.log`

### Postagens duplicadas

**Solução:**
- O sistema já evita duplicatas automaticamente
- Se persistir, delete: `data/posted_news.json`

---

## ☁️ Deploy no Fly.io

### Preparação

1. Instale Fly CLI:
```bash
# Linux/Mac
curl -L https://fly.io/install.sh | sh

# Windows
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"
```

2. Faça login:
```bash
fly auth login
```

### Deploy

1. Crie o Dockerfile na raiz do projeto:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

2. Crie `fly.toml`:

```toml
app = "gamefi-radar-br"
primary_region = "gru"  # São Paulo

[build]
  dockerfile = "Dockerfile"

[[services]]
  internal_port = 8080
  protocol = "tcp"

  [[services.ports]]
    port = 80
    handlers = ["http"]

[env]
  TIMEZONE = "America/Sao_Paulo"
```

3. Configure secrets:

```bash
fly secrets set CLAUDE_API_KEY=sk-ant-api03-...
fly secrets set TELEGRAM_BOT_TOKEN=...
fly secrets set MODE=production
```

4. Deploy:

```bash
fly deploy
```

### Monitoramento

```bash
# Ver logs
fly logs

# Status
fly status

# SSH para debug
fly ssh console
```

---

## 📊 Personalização

### Alterar Horários

Edite no `.env`:
```env
SCHEDULE_RESUMO_DIARIO=10:00
SCHEDULE_NOTICIA_RELEVANTE_1=14:00
SCHEDULE_NOTICIA_RELEVANTE_2=20:00
```

### Modificar Prompts

Edite `config/prompts.py`:
- `PROMPT_RESUMO_DIARIO` - Template do resumo
- `PROMPT_NOTICIA_RELEVANTE` - Template da notícia

### Adicionar Mais Postagens

Edite `src/scheduler.py`, adicione novos horários:
```python
schedule.every().day.at("21:00").do(self.job_noticia_relevante)
```

---

## 📝 Logs e Monitoramento

### Localização dos Logs

- **Arquivo:** `logs/bot.log`
- **Console:** Saída colorida em tempo real

### Níveis de Log

- 🟢 **INFO:** Operações normais
- 🟡 **WARNING:** Avisos não críticos
- 🔴 **ERROR:** Erros recuperáveis
- ⚫ **CRITICAL:** Erros fatais

### Ver Estatísticas

```python
python test_bot.py
# Escolha opção 7 - Ver estatísticas
```

---

## 🤝 Contribuindo

Melhorias são bem-vindas! Sinta-se livre para:
- Reportar bugs
- Sugerir novas features
- Melhorar documentação
- Enviar pull requests

---

## 📄 Licença

Este projeto é de código aberto para uso pessoal e educacional.

---

## 💬 Suporte

**Problemas?**
- Verifique a seção "Solução de Problemas"
- Execute `python setup_helper.py`
- Execute `python test_bot.py`
- Consulte os logs em `logs/bot.log`

---

## 🎯 Roadmap Futuro

- [ ] Interface web para gerenciamento
- [ ] Suporte a múltiplos canais
- [ ] Análise de sentimento nas notícias
- [ ] Integração com mais fontes de notícias
- [ ] Dashboard de estatísticas
- [ ] Notificações por email

---

**Feito com ❤️ para a comunidade GameFi Brasil**

🎮 **GameFi RADAR BR** 🚀