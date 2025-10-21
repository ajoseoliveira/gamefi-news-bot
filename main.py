#!/usr/bin/env python3
"""
GameFi RADAR BR - Bot de Notícias Automatizado
Bot inteligente que posta resumos diários e notícias relevantes sobre GameFi/Web3
+ Painel Administrativo integrado
"""

import sys
import asyncio
import threading
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from config.config import validate_config, print_config, MODE
from src.scheduler import scheduler
from utils.logger import logger

# Só importa admin_bot se for modo test
if MODE == "test":
    from src.admin_bot import AdminBot


def run_scheduler():
    """Roda o scheduler em uma thread separada"""
    try:
        scheduler.start()
    except KeyboardInterrupt:
        pass


def run_admin_bot():
    """Roda o admin bot"""
    try:
        admin_bot = AdminBot()
        admin_bot.run()
    except KeyboardInterrupt:
        pass


def main():
    """Função principal do bot"""
    
    # Banner
    print("\n" + "="*60)
    print("🎮 GameFi RADAR BR - Bot de Notícias Automatizado 🚀")
    print("="*60 + "\n")
    
    # Valida configurações
    if not validate_config():
        logger.critical("❌ Configurações inválidas! Verifique o arquivo .env")
        sys.exit(1)
    
    # Mostra configurações
    print_config()
    
    # Inicia os bots
    try:
        if MODE == "production":
            # Modo produção: apenas scheduler (sem admin bot)
            logger.info("🚀 Iniciando bot em modo PRODUÇÃO...")
            logger.info("📊 Apenas scheduler de notícias ativo")

            scheduler.start()  # Roda direto na thread principal

        else:
            # Modo test: scheduler + admin bot
            logger.info("🚀 Iniciando sistema completo em modo TESTE...")
            logger.info("📊 Bot de notícias + Painel administrativo")

            # Cria thread para o scheduler (bot de notícias)
            scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
            scheduler_thread.start()

            logger.info("✅ Bot de notícias iniciado")
            logger.info("🤖 Iniciando painel administrativo...")

            # Roda o admin bot na thread principal
            run_admin_bot()

    except KeyboardInterrupt:
        logger.warning("\n⚠️  Sistema interrompido pelo usuário")

    except Exception as e:
        logger.critical(f"❌ Erro fatal: {str(e)}")
        sys.exit(1)

    finally:
        scheduler.stop()
        logger.info("👋 Sistema finalizado\n")


if __name__ == "__main__":
    main()