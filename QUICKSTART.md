# 🚀 Guia Rápido de Início - GameFi RADAR BR Bot

## ⚡ Começar em 5 minutos!

### 1️⃣ Instale Python 3.8+

**Windows:**
- Baixe em: https://www.python.org/downloads/
- ✅ Marque "Add Python to PATH"

**Linux/Mac:**
```bash
python3 --version  # Verifica se já tem
```

### 2️⃣ Instale as dependências

```bash
# Entre na pasta do projeto
cd gamefi-news-bot

# Instale
pip install -r requirements.txt
```

### 3️⃣ Configure suas chaves

Edite o arquivo `.env`:

```env
# Sua chave do Claude (obtenha em: https://console.anthropic.com/)
CLAUDE_API_KEY=sua_chave_aqui

# Seu token do bot (obtenha com @BotFather no Telegram)
TELEGRAM_BOT_TOKEN=seu_token_aqui

# ID do seu canal
TELEGRAM_CHANNEL_ID=@seu_canal_aqui
```

### 4️⃣ Teste tudo

```bash
python setup_helper.py
```

Se tudo estiver ✅ verde, está pronto!

### 5️⃣ Rode o bot

**Modo Teste (não posta no canal):**
```bash
python test_bot.py
```

**Modo Produção (posta automaticamente):**
```bash
# 1. Mude no .env: MODE=production
# 2. Execute:
python main.py
```

---

## 📱 Como criar o Bot no Telegram

1. Abra o Telegram
2. Procure por: **@BotFather**
3. Envie: `/newbot`
4. Escolha um nome: `GameFi News`
5. Escolha um username: `gamefi_news_bot`
6. Copie o **token** que ele der

---

## 📢 Como configurar o Canal

1. Crie um canal no Telegram
2. Adicione o bot como **Administrador**
3. Dê permissão de "Postar mensagens"
4. Use o username do canal no `.env`:
   ```
   TELEGRAM_CHANNEL_ID=@seu_canal
   ```

---

## ⏰ Horários das Postagens

Por padrão:
- **09:00** - Resumo Diário (5 notícias)
- **13:00** - Notícia Relevante
- **18:00** - Notícia Relevante

Para alterar, edite no `.env`:
```env
SCHEDULE_RESUMO_DIARIO=10:00
SCHEDULE_NOTICIA_RELEVANTE_1=15:00
SCHEDULE_NOTICIA_RELEVANTE_2=20:00
```

---

## 🧪 Comandos de Teste

```bash
# Ver todas as opções
python test_bot.py

# Testar só o Claude
python src/ai_processor.py

# Testar só o Telegram
python src/telegram_bot.py

# Executar resumo AGORA (em teste)
python test_bot.py
# Escolha opção 8
```

---

## 🐛 Problemas Comuns

### "CLAUDE_API_KEY não configurada"
➡️ Verifique o arquivo `.env` e copie sua chave corretamente

### "Telegram Bot sem permissão"
➡️ Adicione o bot como **Administrador** do canal

### "ModuleNotFoundError"
➡️ Execute: `pip install -r requirements.txt`

### Bot não está postando
➡️ Verifique se `MODE=production` no `.env`

---

## 📊 Ver o que está acontecendo

**Logs em tempo real:**
```bash
# Windows PowerShell
Get-Content logs/bot.log -Wait

# Linux/Mac
tail -f logs/bot.log
```

**Estatísticas:**
```bash
python test_bot.py
# Escolha opção 7
```

---

## 🎯 Próximos Passos

Depois que o bot estiver funcionando:

1. **Personalize os prompts** em `config/prompts.py`
2. **Ajuste os horários** no `.env`
3. **Monitore os logs** em `logs/bot.log`
4. **Faça backup** do `data/posted_news.json`

---

## 💡 Dicas Pro

**Rodar 24/7 no seu computador:**
```bash
# Linux/Mac
nohup python main.py &

# Windows
# Use Task Scheduler ou rode em uma VPS
```

**Deploy na nuvem (gratuito):**
- Ver seção completa no `README.md`
- Fly.io, Railway, ou Render.com

**Mudar o tom das postagens:**
- Edite `config/prompts.py`
- Modifique as instruções de estilo

---

## 📞 Precisa de Ajuda?

1. ✅ Leia o `README.md` completo
2. ✅ Execute `python setup_helper.py`
3. ✅ Execute `python test_bot.py`
4. ✅ Verifique `logs/bot.log`

---

## ✨ Está Funcionando?

**Parabéns!** 🎉

Agora seu bot está:
- 🤖 Buscando notícias automaticamente
- 📝 Criando resumos inteligentes
- 📢 Postando no seu canal do Telegram

**Aproveite e acompanhe seu canal: @gamefiradarbr**

---

**Boas postagens!** 🚀🎮