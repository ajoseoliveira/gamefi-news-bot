"""
Configurações centralizadas do GameFi RADAR BR Bot
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# Diretórios base
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"

# Cria diretórios se não existirem
DATA_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# ========== CLAUDE API ==========
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-20250514")
CLAUDE_MAX_TOKENS = 4096
CLAUDE_TEMPERATURE = 0.7

# ========== NEWSAPI ==========
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")

# ========== TELEGRAM ==========
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID", "@gamefiradarbr")
CHANNEL_NAME = os.getenv("CHANNEL_NAME", "GameFi RADAR BR👾🚀")

# Ajustes do cliente HTTP do Telegram (pool e timeouts)
def _to_int(value: str, default: int) -> int:
    try:
        return int(value)
    except Exception:
        return default

def _to_float(value: str, default: float) -> float:
    try:
        return float(value)
    except Exception:
        return default

TELEGRAM_POOL_SIZE = _to_int(os.getenv("TELEGRAM_POOL_SIZE", "20"), 20)
TELEGRAM_POOL_TIMEOUT = _to_float(os.getenv("TELEGRAM_POOL_TIMEOUT", "30"), 30.0)
TELEGRAM_READ_TIMEOUT = _to_float(os.getenv("TELEGRAM_READ_TIMEOUT", "30"), 30.0)
TELEGRAM_CONNECT_TIMEOUT = _to_float(os.getenv("TELEGRAM_CONNECT_TIMEOUT", "10"), 10.0)
TELEGRAM_RETRIES = _to_int(os.getenv("TELEGRAM_RETRIES", "3"), 3)
TELEGRAM_RETRY_BACKOFF = _to_float(os.getenv("TELEGRAM_RETRY_BACKOFF", "2"), 2.0)

# ========== AGENDAMENTO ==========
SCHEDULE_RESUMO_DIARIO = os.getenv("SCHEDULE_RESUMO_DIARIO", "09:00")
SCHEDULE_NOTICIA_RELEVANTE_1 = os.getenv("SCHEDULE_NOTICIA_RELEVANTE_1", "13:00")
SCHEDULE_NOTICIA_RELEVANTE_2 = os.getenv("SCHEDULE_NOTICIA_RELEVANTE_2", "18:00")
TIMEZONE = os.getenv("TIMEZONE", "America/Sao_Paulo")

# ========== MODO DE OPERAÇÃO ==========
MODE = os.getenv("MODE", "test")  # test ou production

# ========== LOGS ==========
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = LOGS_DIR / os.getenv("LOG_FILE", "bot.log").split("/")[-1]

# ========== ARQUIVOS DE DADOS ==========
POSTED_NEWS_FILE = DATA_DIR / "posted_news.json"
CACHE_FILE = DATA_DIR / "news_cache.json"

# ========== TEMAS PARA BUSCA ==========
TOPICS = [
    "GameFi",
    "Web3 Gaming",
    "Blockchain Games",
    "NFT Games",
    "Crypto Gaming",
    "Play to Earn",
    "P2E Games"
]

# ========== PALAVRAS-CHAVE PARA FILTRO ==========
KEYWORDS = [
    "gamefi", "web3 gaming", "blockchain game", "nft game",
    "crypto game", "play to earn", "p2e", "metaverse game",
    "gaming token", "gaming nft", "axie", "immutable",
    "gala games", "animoca", "sandbox", "decentraland"
]

# ========== VALIDAÇÃO ==========
def validate_config():
    """Valida se todas as configurações necessárias estão presentes"""
    errors = []
    
    if not CLAUDE_API_KEY:
        errors.append("❌ CLAUDE_API_KEY não encontrada no .env")
    
    if not TELEGRAM_BOT_TOKEN:
        errors.append("❌ TELEGRAM_BOT_TOKEN não encontrado no .env")
    
    if not TELEGRAM_CHANNEL_ID:
        errors.append("❌ TELEGRAM_CHANNEL_ID não encontrado no .env")
    
    if errors:
        print("\n🚨 ERROS DE CONFIGURAÇÃO:")
        for error in errors:
            print(error)
        print("\n👉 Verifique seu arquivo .env\n")
        return False
    
    return True


def print_config():
    """Imprime configurações atuais (sem mostrar chaves completas)"""
    print("\n" + "="*60)
    print(f"🤖 CONFIGURAÇÃO DO BOT: {CHANNEL_NAME}")
    print("="*60)
    print(f"🔑 Claude API: {'✅ Configurada' if CLAUDE_API_KEY else '❌ Não configurada'}")
    print(f"📱 Telegram Bot: {'✅ Configurado' if TELEGRAM_BOT_TOKEN else '❌ Não configurado'}")
    print(f"📢 Canal: {TELEGRAM_CHANNEL_ID}")
    print(f"🕐 Resumo Diário: {SCHEDULE_RESUMO_DIARIO}")
    print(f"🕐 Notícia Relevante 1: {SCHEDULE_NOTICIA_RELEVANTE_1}")
    print(f"🕐 Notícia Relevante 2: {SCHEDULE_NOTICIA_RELEVANTE_2}")
    print(f"🌍 Timezone: {TIMEZONE}")
    print(f"⚙️  Modo: {MODE.upper()}")
    print(f"📝 Log Level: {LOG_LEVEL}")
    print("="*60 + "\n")


if __name__ == "__main__":
    # Testa configurações
    print_config()
    if validate_config():
        print("✅ Todas as configurações estão OK!\n")
    else:
        print("❌ Existem problemas nas configurações!\n")
