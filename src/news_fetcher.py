"""
Busca notícias reais via NewsAPI com sistema anti-duplicação
"""

import requests
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path
import os

from utils.logger import logger


class NewsFetcher:
    """Busca notícias atuais sobre GameFi/Web3 Gaming"""
    
    def __init__(self):
        self.api_key = os.getenv('NEWSAPI_KEY')
        if not self.api_key:
            raise ValueError("NEWSAPI_KEY não configurada no .env")
        
        self.base_url = "https://newsapi.org/v2/everything"
        
        # Arquivo de cache
        self.cache_file = Path("data/used_news_cache.json")
        self.cache_file.parent.mkdir(exist_ok=True)
        
        # Carrega cache
        self.used_news = self._load_cache()
        
        # Keywords GameFi específicas
        self.keywords = [
            "GameFi", 
            "Web3 gaming", 
            "blockchain games",
            "crypto gaming",
            "play-to-earn",
            "NFT gaming",
            "gaming NFT",
            "Axie Infinity",
            "Immutable X",
            "Gala Games",
            "The Sandbox",
            "Decentraland",
            "Ronin network",
            "gaming token",
            "metaverse game",
            "blockchain game launch",
            "crypto game funding",
            "Web3 game",
            "on-chain gaming"
        ]
        
        logger.info("NewsAPI inicializado com cache anti-duplicação")
    
    def _load_cache(self) -> Dict:
        """Carrega cache de notícias já usadas"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {"used_urls": [], "last_cleanup": None}
        return {"used_urls": [], "last_cleanup": None}
    
    def _save_cache(self):
        """Salva cache de notícias usadas"""
        with open(self.cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.used_news, f, indent=2)
    
    def _clean_old_cache(self):
        """Remove URLs com mais de 30 dias do cache"""
        # Implementação simplificada - limpa tudo a cada 30 dias
        last_cleanup = self.used_news.get('last_cleanup')

        if last_cleanup:
            last_date = datetime.fromisoformat(last_cleanup)
            days_since = (datetime.now() - last_date).days

            if days_since >= 30:
                self.used_news['used_urls'] = []
                self.used_news['last_cleanup'] = datetime.now().isoformat()
                self._save_cache()
                logger.info("Cache de notícias limpado (30 dias)")
        else:
            self.used_news['last_cleanup'] = datetime.now().isoformat()
            self._save_cache()
    
    def mark_as_used(self, url: str):
        """
        Marca uma notícia como já usada
        
        Args:
            url: URL da notícia
        """
        if url not in self.used_news['used_urls']:
            self.used_news['used_urls'].append(url)
            self._save_cache()
            logger.debug(f"Notícia marcada como usada: {url[:50]}...")
    
    def _is_used(self, url: str) -> bool:
        """Verifica se notícia já foi usada"""
        return url in self.used_news['used_urls']
    
    def _build_query(self) -> str:
        """Constrói query de busca otimizada"""
        # Query focada em GameFi específico
        query = '("GameFi" OR "Web3 gaming" OR "blockchain games" OR "crypto gaming" OR "play-to-earn" OR "NFT games" OR "gaming token")'
        return query
    
    def fetch_recent_news(self, hours: int = 48, max_results: int = 30, filter_used: bool = True) -> List[Dict]:
        """
        Busca notícias recentes
        
        Args:
            hours: Buscar notícias das últimas N horas
            max_results: Número máximo de resultados (aumentado para 30)
            filter_used: Se True, remove notícias já usadas
        
        Returns:
            Lista de notícias com título, descrição, URL, data e fonte
        """
        logger.processing(f"Buscando notícias das últimas {hours}h...")
        
        # Limpa cache antigo
        self._clean_old_cache()
        
        # Calcula data inicial
        from_date = datetime.now() - timedelta(hours=hours)
        from_date_str = from_date.strftime('%Y-%m-%dT%H:%M:%S')
        
        # Parâmetros da API
        params = {
            'q': self._build_query(),
            'from': from_date_str,
            'sortBy': 'publishedAt',
            'language': 'en',
            'pageSize': max_results,
            'apiKey': self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('status') != 'ok':
                logger.error(f"NewsAPI retornou erro: {data.get('message')}")
                return []
            
            articles = data.get('articles', [])
            
            # Processa artigos
            news_list = []
            for article in articles:
                # Filtra artigos sem conteúdo útil
                if not article.get('title') or not article.get('url'):
                    continue

                url = article.get('url', '')

                # Filtra URLs inválidas (redirects, consent pages, etc)
                invalid_patterns = [
                    'consent.yahoo.com',
                    'consent.google.com',
                    'removed.com',
                    '[Removed]',
                    'login?',
                    'signin?'
                ]
                if any(pattern in url for pattern in invalid_patterns):
                    logger.debug(f"URL inválida/redirect detectada, pulando: {url[:50]}...")
                    continue

                # Filtra notícias já usadas
                if filter_used and self._is_used(url):
                    logger.debug(f"Notícia já usada, pulando: {article.get('title', '')[:50]}...")
                    continue
                
                news_item = {
                    'title': article.get('title', ''),
                    'description': article.get('description', ''),
                    'url': url,
                    'published_at': article.get('publishedAt', ''),
                    'source': article.get('source', {}).get('name', 'Unknown')
                }
                
                news_list.append(news_item)
            
            logger.success(f"Encontradas {len(news_list)} notícias novas e relevantes")
            
            if filter_used and len(news_list) < 5:
                logger.warning(f"Poucas notícias novas ({len(news_list)}). Considere aumentar período de busca.")
            
            return news_list
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao buscar notícias: {str(e)}")
            return []
    
    def format_news_for_ai(self, news_list: List[Dict], include_usage_info: bool = False) -> str:
        """
        Formata notícias para enviar ao Claude
        
        Args:
            news_list: Lista de notícias
            include_usage_info: Se True, adiciona informação sobre notícias já usadas
        
        Returns:
            String formatada com todas as notícias
        """
        if not news_list:
            return "Nenhuma notícia encontrada."
        
        formatted = "NOTÍCIAS DISPONÍVEIS (TODAS SÃO NOVAS - NUNCA FORAM USADAS):\n\n"
        
        if include_usage_info:
            formatted += f"ℹ️ IMPORTANTE: Você já usou {len(self.used_news['used_urls'])} notícias recentemente.\n"
            formatted += "As notícias abaixo são TODAS NOVAS - escolha livremente.\n\n"
        
        for i, news in enumerate(news_list, 1):
            category = news.get('category', 'gamefi')  # Default gamefi se não tiver
            formatted += f"{i}. **{news['title']}**\n"
            formatted += f"   Categoria: {category.upper()}\n"
            formatted += f"   Fonte: {news['source']}\n"
            formatted += f"   Data: {news['published_at']}\n"
            formatted += f"   Descrição: {news['description']}\n"
            formatted += f"   URL: {news['url']}\n\n"
        
        return formatted
    
    def get_cache_stats(self) -> Dict:
        """Retorna estatísticas do cache"""
        return {
            'total_used': len(self.used_news['used_urls']),
            'last_cleanup': self.used_news.get('last_cleanup', 'Nunca')
        }


# Instância global
news_fetcher = NewsFetcher()


if __name__ == "__main__":
    # Teste do fetcher
    logger.section("TESTE DO NEWS FETCHER COM CACHE")
    
    print("\nEstatísticas do cache:")
    stats = news_fetcher.get_cache_stats()
    print(f"  Notícias usadas: {stats['total_used']}")
    print(f"  Última limpeza: {stats['last_cleanup']}")
    
    print("\nBuscando notícias de teste...\n")
    news = news_fetcher.fetch_recent_news(hours=48, max_results=10)
    
    if news:
        print(f"Encontradas {len(news)} notícias novas:\n")
        for i, item in enumerate(news, 1):
            print(f"{i}. {item['title']}")
            print(f"   {item['source']} - {item['published_at']}")
            print(f"   {item['url']}\n")
    else:
        print("Nenhuma notícia nova encontrada.")