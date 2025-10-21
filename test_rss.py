#!/usr/bin/env python3
"""
Teste do RSS Fetcher
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from src.rss_fetcher import rss_fetcher
from utils.logger import logger

if __name__ == "__main__":
    logger.section("TESTE DO RSS FETCHER")
    
    news = rss_fetcher.fetch_all(hours=168)
    
    print(f"\nEncontradas {len(news)} notícias:\n")
    for i, item in enumerate(news[:10], 1):
        print(f"{i}. {item['title']}")
        print(f"   {item['source']} - {item['published_at']}")
        print(f"   {item['url']}\n")