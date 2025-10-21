#!/usr/bin/env python3
"""
Script para limpar o cache de notícias usadas
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from src.news_fetcher import news_fetcher
from utils.logger import logger

if __name__ == "__main__":
    logger.section("LIMPEZA DE CACHE")

    # Mostra estatísticas antes
    stats = news_fetcher.get_cache_stats()
    print(f"\nCache atual:")
    print(f"  Notícias usadas: {stats['total_used']}")
    print(f"  Última limpeza: {stats['last_cleanup']}")

    # Confirmação
    print("\n⚠️  Esta ação irá limpar TODAS as notícias marcadas como usadas.")
    confirm = input("Deseja continuar? (s/N): ").strip().lower()

    if confirm == 's':
        # Limpa o cache
        news_fetcher.used_news['used_urls'] = []
        news_fetcher._save_cache()

        logger.success("Cache limpo com sucesso!")
        print("\n✅ Todas as notícias foram desmarcadas.")
        print("Você pode usar qualquer notícia novamente agora.\n")
    else:
        logger.info("Operação cancelada.")
        print("\nCache não foi alterado.\n")
