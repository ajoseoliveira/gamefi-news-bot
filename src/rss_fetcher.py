"""
Busca notícias via RSS feeds (Google News, CoinDesk, CoinTelegraph, DappRadar, etc)
"""

import feedparser
from datetime import datetime, timedelta, timezone
from typing import List, Dict
from urllib.parse import quote

from utils.logger import logger


class RSSFetcher:
    """Busca notícias de múltiplos RSS feeds"""

    def __init__(self):
        # RSS feeds focados em GAMEFI/Web3 Gaming
        self.gamefi_feeds = {
            'dappradar': 'https://dappradar.com/blog/feed',
            'nftplazas': 'https://nftplazas.com/feed/',
            'beincrypto_gaming': 'https://beincrypto.com/gaming/feed/',
        }

        # RSS feeds de CRYPTO GERAL
        self.crypto_feeds = {
            'coindesk': 'https://www.coindesk.com/arc/outboundfeeds/rss/',
            'cointelegraph': 'https://cointelegraph.com/rss',
            'decrypt': 'https://decrypt.co/feed',
            'theblock': 'https://www.theblock.co/rss.xml',
            'cryptoslate': 'https://cryptoslate.com/feed/'
        }

        # Keywords para busca no Google News (GameFi)
        self.gamefi_keywords = [
            "GameFi", "Web3 gaming", "blockchain games",
            "crypto gaming", "NFT games", "play-to-earn"
        ]

        # Keywords para busca no Google News (Crypto geral)
        self.crypto_keywords = [
            "Bitcoin", "Ethereum", "crypto market",
            "cryptocurrency", "DeFi", "altcoin"
        ]

        logger.info("RSS Fetcher inicializado (GameFi + Crypto geral)")

    def _parse_date(self, date_str: str) -> datetime:
        """Converte data do RSS para datetime"""
        try:
            from dateutil import parser
            return parser.parse(date_str)
        except:
            return datetime.now(timezone.utc)
    
    def fetch_google_news(self, hours: int = 72) -> List[Dict]:
        """
        Busca notícias do Google News RSS
        
        Args:
            hours: Período em horas
        
        Returns:
            Lista de notícias
        """
        news_list = []
        cutoff_date = datetime.now(timezone.utc) - timedelta(hours=hours)
        
        for keyword in self.gamefi_keywords:
            try:
                # URL do Google News RSS
                encoded_keyword = quote(keyword)
                url = f"https://news.google.com/rss/search?q={encoded_keyword}&hl=en-US&gl=US&ceid=US:en"
                
                logger.debug(f"Buscando Google News: {keyword}")
                
                feed = feedparser.parse(url)
                
                for entry in feed.entries[:5]:  # Limita 5 por keyword
                    pub_date = self._parse_date(entry.get('published', ''))

                    if pub_date >= cutoff_date:
                        news_item = {
                            'title': entry.get('title', ''),
                            'description': entry.get('summary', ''),
                            'url': entry.get('link', ''),
                            'published_at': pub_date.isoformat(),
                            'source': 'Google News'
                        }
                        news_list.append(news_item)
                        
            except Exception as e:
                logger.debug(f"Erro ao buscar Google News ({keyword}): {str(e)}")
                continue
        
        return news_list
    
    def fetch_gamefi_rss(self, max_results: int = 10) -> List[Dict]:
        """
        Busca notícias GAMEFI de RSS feeds específicos

        Args:
            max_results: Número máximo de notícias

        Returns:
            Lista de notícias GameFi
        """
        news_list = []
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=7)

        for feed_name, feed_url in self.gamefi_feeds.items():
            try:
                logger.debug(f"Buscando {feed_name} GameFi RSS...")

                feed = feedparser.parse(feed_url)
                logger.info(f"{feed_name}: {len(feed.entries)} entries no feed")

                for entry in feed.entries[:50]:
                    if len(news_list) >= max_results:
                        break

                    pub_date = self._parse_date(entry.get('published', ''))
                    if pub_date < cutoff_date:
                        continue

                    news_item = {
                        'title': entry.get('title', ''),
                        'description': entry.get('summary', '')[:200] if entry.get('summary') else '',
                        'url': entry.get('link', ''),
                        'published_at': entry.get('published', ''),
                        'source': feed_name.title(),
                        'category': 'gamefi'
                    }
                    news_list.append(news_item)

            except Exception as e:
                logger.debug(f"Erro ao buscar {feed_name}: {str(e)}")
                continue

        logger.info(f"GameFi RSS: {len(news_list)} notícias encontradas")
        return news_list

    def fetch_crypto_general_rss(self, max_results: int = 10) -> List[Dict]:
        """
        Busca notícias de CRYPTO GERAL de RSS feeds

        Args:
            max_results: Número máximo de notícias

        Returns:
            Lista de notícias crypto geral
        """
        news_list = []
        cutoff_date = datetime.now(timezone.utc) - timedelta(days=7)

        # Termos crypto geral (não GameFi)
        crypto_terms = [
            'bitcoin', 'btc', 'ethereum', 'eth', 'price', 'market',
            'trading', 'defi', 'altcoin', 'regulation', 'sec',
            'etf', 'investment', 'blockchain', 'crypto', 'cryptocurrency'
        ]

        for feed_name, feed_url in self.crypto_feeds.items():
            try:
                logger.debug(f"Buscando {feed_name} Crypto RSS...")

                feed = feedparser.parse(feed_url)
                logger.info(f"{feed_name}: {len(feed.entries)} entries no feed")

                for entry in feed.entries[:100]:
                    if len(news_list) >= max_results:
                        break

                    pub_date = self._parse_date(entry.get('published', ''))
                    if pub_date < cutoff_date:
                        continue

                    title = entry.get('title', '').lower()
                    description = (entry.get('summary', '') or '').lower()

                    # Verifica se é crypto geral (não GameFi)
                    if any(term in title or term in description for term in crypto_terms):
                        news_item = {
                            'title': entry.get('title', ''),
                            'description': entry.get('summary', '')[:200] if entry.get('summary') else '',
                            'url': entry.get('link', ''),
                            'published_at': entry.get('published', ''),
                            'source': feed_name.title(),
                            'category': 'crypto'
                        }
                        news_list.append(news_item)

            except Exception as e:
                logger.debug(f"Erro ao buscar {feed_name}: {str(e)}")
                continue

        logger.info(f"Crypto Geral RSS: {len(news_list)} notícias encontradas")
        return news_list
    
    def fetch_all(self, hours: int = 72) -> List[Dict]:
        """
        Busca notícias GameFi de todas as fontes RSS (para notícias relevantes)

        Args:
            hours: Período em horas (usado apenas para Google News)

        Returns:
            Lista combinada de notícias GameFi
        """
        logger.processing(f"Buscando notícias GameFi RSS...")

        all_news = []

        # Busca Google News GameFi
        google_news = self.fetch_google_news(hours)
        all_news.extend(google_news)
        logger.debug(f"Google News: {len(google_news)} notícias")

        # Busca RSS feeds GameFi
        gamefi_news = self.fetch_gamefi_rss(max_results=10)
        all_news.extend(gamefi_news)

        # Remove duplicatas (mesmo URL)
        seen_urls = set()
        unique_news = []
        for news in all_news:
            url = news['url']
            if url not in seen_urls:
                seen_urls.add(url)
                unique_news.append(news)

        logger.success(f"RSS GameFi: {len(unique_news)} notícias únicas encontradas")
        return unique_news

    def fetch_for_daily_summary(self, gamefi_count: int = 5, crypto_count: int = 5) -> List[Dict]:
        """
        Busca notícias separadas para o resumo diário: GameFi + Crypto Geral

        Args:
            gamefi_count: Quantidade de notícias GameFi
            crypto_count: Quantidade de notícias crypto geral

        Returns:
            Lista combinada (GameFi + Crypto)
        """
        logger.processing(f"Buscando {gamefi_count} GameFi + {crypto_count} Crypto Geral...")

        all_news = []

        # Busca notícias GameFi
        gamefi_news = self.fetch_gamefi_rss(max_results=gamefi_count)
        all_news.extend(gamefi_news)
        logger.debug(f"GameFi: {len(gamefi_news)} notícias")

        # Busca notícias Crypto Geral
        crypto_news = self.fetch_crypto_general_rss(max_results=crypto_count)
        all_news.extend(crypto_news)
        logger.debug(f"Crypto Geral: {len(crypto_news)} notícias")

        # Remove duplicatas (mesmo URL)
        seen_urls = set()
        unique_news = []
        for news in all_news:
            url = news['url']
            if url not in seen_urls:
                seen_urls.add(url)
                unique_news.append(news)

        logger.success(f"RSS Total: {len(unique_news)} notícias ({len(gamefi_news)} GameFi + {len(crypto_news)} Crypto)")
        return unique_news


# Instância global
rss_fetcher = RSSFetcher()


if __name__ == "__main__":
    # Teste
    logger.section("TESTE DO RSS FETCHER")
    
    news = rss_fetcher.fetch_all(hours=48)
    
    print(f"\nEncontradas {len(news)} notícias:\n")
    for i, item in enumerate(news[:10], 1):
        print(f"{i}. {item['title']}")
        print(f"   {item['source']} - {item['published_at']}")
        print(f"   {item['url']}\n")