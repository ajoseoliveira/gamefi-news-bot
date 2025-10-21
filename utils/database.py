"""
Sistema de banco de dados simples (JSON) para evitar duplicação de notícias
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict
import hashlib

from config.config import POSTED_NEWS_FILE
from utils.logger import logger


class NewsDatabase:
    """Gerencia histórico de notícias postadas"""
    
    def __init__(self, db_file: Path = POSTED_NEWS_FILE):
        self.db_file = db_file
        self.data = self._load_db()
    
    def _load_db(self) -> Dict:
        """Carrega banco de dados do arquivo JSON"""
        if self.db_file.exists():
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                logger.warning("Arquivo de banco corrompido. Criando novo.")
                return {"posted_news": []}
        return {"posted_news": []}
    
    def _save_db(self):
        """Salva banco de dados no arquivo JSON"""
        self.db_file.parent.mkdir(exist_ok=True)
        with open(self.db_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)
    
    def _generate_hash(self, content: str) -> str:
        """Gera hash único para o conteúdo"""
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def add_post(self, post_type: str, content: str, title: str = ""):
        """
        Adiciona uma postagem ao histórico
        
        Args:
            post_type: 'resumo_diario' ou 'noticia_relevante'
            content: Conteúdo completo da postagem
            title: Título da notícia (opcional)
        """
        post_data = {
            "type": post_type,
            "title": title,
            "content_hash": self._generate_hash(content),
            "timestamp": datetime.now().isoformat(),
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        
        self.data["posted_news"].append(post_data)
        self._save_db()
        
        logger.debug(f"Postagem adicionada ao histórico: {post_type}")
    
    def is_duplicate(self, content: str, days: int = 7) -> bool:
        """
        Verifica se o conteúdo já foi postado nos últimos N dias
        
        Args:
            content: Conteúdo a verificar
            days: Número de dias para verificar duplicação
        
        Returns:
            True se for duplicado, False caso contrário
        """
        content_hash = self._generate_hash(content)
        cutoff_date = datetime.now() - timedelta(days=days)
        
        for post in self.data["posted_news"]:
            post_date = datetime.fromisoformat(post["timestamp"])
            
            if post_date >= cutoff_date:
                if post["content_hash"] == content_hash:
                    logger.warning(f"Conteúdo duplicado detectado (postado em {post['date']})")
                    return True
        
        return False
    
    def get_recent_posts(self, days: int = 7) -> List[Dict]:
        """Retorna postagens dos últimos N dias"""
        cutoff_date = datetime.now() - timedelta(days=days)
        recent = []
        
        for post in self.data["posted_news"]:
            post_date = datetime.fromisoformat(post["timestamp"])
            if post_date >= cutoff_date:
                recent.append(post)
        
        return recent
    
    def clean_old_posts(self, days: int = 30):
        """Remove postagens mais antigas que N dias"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        before_count = len(self.data["posted_news"])
        
        self.data["posted_news"] = [
            post for post in self.data["posted_news"]
            if datetime.fromisoformat(post["timestamp"]) >= cutoff_date
        ]
        
        after_count = len(self.data["posted_news"])
        removed = before_count - after_count
        
        if removed > 0:
            self._save_db()
            logger.info(f"Limpeza: {removed} posts antigos removidos")
    
    def get_stats(self) -> Dict:
        """Retorna estatísticas do banco de dados"""
        total_posts = len(self.data["posted_news"])
        
        if total_posts == 0:
            return {
                "total_posts": 0,
                "resumos": 0,
                "noticias": 0,
                "first_post": None,
                "last_post": None
            }
        
        resumos = sum(1 for p in self.data["posted_news"] if p["type"] == "resumo_diario")
        noticias = sum(1 for p in self.data["posted_news"] if p["type"] == "noticia_relevante")
        
        timestamps = [datetime.fromisoformat(p["timestamp"]) for p in self.data["posted_news"]]
        
        return {
            "total_posts": total_posts,
            "resumos": resumos,
            "noticias": noticias,
            "first_post": min(timestamps).strftime("%Y-%m-%d %H:%M"),
            "last_post": max(timestamps).strftime("%Y-%m-%d %H:%M")
        }


# Instância global do banco de dados
db = NewsDatabase()


if __name__ == "__main__":
    # Teste do banco de dados
    logger.section("TESTE DO BANCO DE DADOS")
    
    # Adiciona postagens de teste
    db.add_post("resumo_diario", "Conteúdo de teste 1", "Teste 1")
    db.add_post("noticia_relevante", "Conteúdo de teste 2", "Teste 2")
    
    # Verifica duplicação
    is_dup = db.is_duplicate("Conteúdo de teste 1")
    print(f"É duplicado? {is_dup}")
    
    # Estatísticas
    stats = db.get_stats()
    print("\nEstatísticas:")
    print(f"  Total de posts: {stats['total_posts']}")
    print(f"  Resumos: {stats['resumos']}")
    print(f"  Notícias: {stats['noticias']}")
    print(f"  Primeiro post: {stats['first_post']}")
    print(f"  Último post: {stats['last_post']}")