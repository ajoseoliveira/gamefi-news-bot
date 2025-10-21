"""
Processador de IA usando Claude API para gerar conteúdo
"""

import anthropic
import re
from typing import Optional

from config.config import (
    CLAUDE_API_KEY,
    CLAUDE_MODEL,
    CLAUDE_MAX_TOKENS,
    CLAUDE_TEMPERATURE
)
from config.prompts import get_prompt_resumo_diario, get_prompt_noticia_relevante
from src.news_fetcher import news_fetcher
from utils.logger import logger


class AIProcessor:
    """Processa notícias usando Claude API"""
    
    def __init__(self):
        if not CLAUDE_API_KEY:
            raise ValueError("CLAUDE_API_KEY não configurada!")
        
        self.client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)
        self.model = CLAUDE_MODEL
        logger.info(f"Claude API inicializada (modelo: {self.model})")
    
    def _clean_response(self, response: str) -> str:
        """
        Remove tags de busca e outras tags internas do Claude
        
        Args:
            response: Resposta bruta do Claude
        
        Returns:
            Resposta limpa sem tags
        """
        # Remove tags de busca
        response = re.sub(r'<search>.*?</search>', '', response, flags=re.DOTALL)
        response = re.sub(r'<searchqualitycheck>.*?</searchqualitycheck>', '', response, flags=re.DOTALL)
        response = re.sub(r'<searchqualityscore>.*?</searchqualityscore>', '', response, flags=re.DOTALL)
        
        # Remove outras tags comuns
        response = re.sub(r'<thinking>.*?</thinking>', '', response, flags=re.DOTALL)
        response = re.sub(r'<analysis>.*?</analysis>', '', response, flags=re.DOTALL)
        
        # Remove múltiplas quebras de linha
        response = re.sub(r'\n{3,}', '\n\n', response)
        
        # Remove espaços extras
        response = response.strip()
        
        return response
    
    def _call_claude(self, prompt: str, system_prompt: str = "") -> Optional[str]:
        """
        Chama a API do Claude
        
        Args:
            prompt: Prompt principal
            system_prompt: Prompt de sistema (opcional)
        
        Returns:
            Resposta do Claude ou None em caso de erro
        """
        try:
            logger.processing(f"Chamando Claude API ({self.model})...")
            
            message = self.client.messages.create(
                model=self.model,
                max_tokens=CLAUDE_MAX_TOKENS,
                temperature=CLAUDE_TEMPERATURE,
                system=system_prompt if system_prompt else "Você é um especialista em GameFi e Web3 Gaming.",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )
            
            response = message.content[0].text
            
            # Limpa a resposta removendo tags internas
            response = self._clean_response(response)
            
            logger.success(f"Claude respondeu ({len(response)} caracteres)")
            return response
            
        except anthropic.APIError as e:
            logger.error(f"Erro na API do Claude: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado ao chamar Claude: {str(e)}")
            return None
    
    def generate_resumo_diario(self) -> Optional[str]:
        """
        Gera o resumo diário de notícias GameFi

        Returns:
            Texto formatado do resumo ou None em caso de erro
        """
        logger.section("GERANDO RESUMO DIÁRIO")

        # Busca notícias reais via NewsAPI (filtra já usadas)
        logger.info("Buscando notícias atuais via NewsAPI...")
        news_list = news_fetcher.fetch_recent_news(hours=72, max_results=10, filter_used=True)

        # Se NewsAPI retornar poucas notícias, complementa com RSS GameFi + Crypto
        if len(news_list) < 8:
            logger.warning(f"NewsAPI retornou apenas {len(news_list)} notícias. Complementando com RSS feeds...")
            from src.rss_fetcher import rss_fetcher

            # Calcula quanto precisa de cada tipo
            total_needed = 10 - len(news_list)
            gamefi_needed = max(3, total_needed // 2)  # Mínimo 3 GameFi
            crypto_needed = total_needed - gamefi_needed  # Resto é crypto geral

            rss_news = rss_fetcher.fetch_for_daily_summary(
                gamefi_count=gamefi_needed,
                crypto_count=crypto_needed
            )

            # Combina e remove duplicatas E já usadas (limita a 10 total)
            all_urls = {n['url'] for n in news_list}
            max_to_add = 10 - len(news_list)
            added = 0

            for rss_item in rss_news:
                if added >= max_to_add:
                    break
                # Verifica se não é duplicada E se não foi usada
                if (rss_item['url'] not in all_urls and
                    not news_fetcher._is_used(rss_item['url'])):
                    news_list.append(rss_item)
                    all_urls.add(rss_item['url'])
                    added += 1

            # Conta por categoria
            gamefi_count = sum(1 for n in news_list if n.get('category') == 'gamefi')
            crypto_count = sum(1 for n in news_list if n.get('category') == 'crypto')

            logger.info(f"Total após RSS: {len(news_list)} notícias ({gamefi_count} GameFi + {crypto_count} Crypto)")

        if not news_list:
            logger.error("Não foi possível buscar notícias novas. Todas já foram usadas.")
            return None

        if len(news_list) < 5:
            logger.warning(f"⚠️ ATENÇÃO: Apenas {len(news_list)} notícia(s) nova(s) disponível(is) para o resumo!")

        # ✅ MARCA TODAS AS NOTÍCIAS COMO USADAS ANTES DE ENVIAR AO CLAUDE
        # Isso garante que mesmo se Claude não retornar URLs, elas não se repitam
        logger.info(f"Marcando {len(news_list)} notícias como usadas ANTES de enviar ao Claude...")
        for news_item in news_list:
            news_fetcher.mark_as_used(news_item['url'])
        logger.info(f"✓ {len(news_list)} notícias marcadas no cache")

        # Formata notícias para o Claude
        news_context = news_fetcher.format_news_for_ai(news_list)

        # Monta o prompt com notícias reais
        base_prompt = get_prompt_resumo_diario()
        full_prompt = f"{base_prompt}\n\n{news_context}\n\nAgora crie o resumo diário com as 5 notícias MAIS RELEVANTES da lista acima, seguindo EXATAMENTE o formato especificado.\n\n⚠️ IMPORTANTE SOBRE SELEÇÃO:\n- Escolha 3 notícias sobre GAMEFI/Web3 Gaming (marcadas com category: gamefi)\n- Escolha 2 notícias sobre MERCADO CRYPTO GERAL (marcadas com category: crypto)\n- Todas as notícias listadas são NOVAS (nunca foram usadas antes)\n- Priorize as mais impactantes de cada categoria"

        system_prompt = """Você é um curador especializado em GameFi, Web3 Gaming e Crypto Gaming.
Você receberá uma lista de notícias reais e atuais.
Sua tarefa é selecionar as 5 MAIS RELEVANTES e criar um resumo formatado.
SEMPRE use as notícias fornecidas - não invente informações.
Siga EXATAMENTE o formato solicitado.
IMPORTANTE: Retorne APENAS o resumo final formatado, sem tags ou análise."""

        response = self._call_claude(full_prompt, system_prompt)

        if response:
            logger.success("Resumo diário gerado com sucesso!")
            logger.debug(f"Preview: {response[:200]}...")

        return response
    
    def generate_noticia_relevante(self) -> Optional[str]:
        """
        Gera uma postagem sobre uma notícia relevante

        Returns:
            Texto formatado da notícia ou None em caso de erro
        """
        logger.section("GERANDO NOTÍCIA RELEVANTE")

        # Busca notícias do NewsAPI primeiro (filtra já usadas automaticamente)
        logger.info("Buscando notícias via NewsAPI...")
        news_list = news_fetcher.fetch_recent_news(hours=72, max_results=10, filter_used=True)

        # Se NewsAPI retornar poucas notícias, complementa com RSS (máximo 10 no total)
        if len(news_list) < 5:
            logger.warning(f"NewsAPI retornou apenas {len(news_list)} notícias. Complementando com RSS feeds...")
            from src.rss_fetcher import rss_fetcher
            rss_news = rss_fetcher.fetch_all(hours=72)

            # Combina e remove duplicatas E já usadas (limita a 10 total)
            all_urls = {n['url'] for n in news_list}
            max_to_add = 10 - len(news_list)  # Limita total em 10
            added = 0

            for rss_item in rss_news:
                if added >= max_to_add:
                    break
                # Verifica se não é duplicada E se não foi usada
                if (rss_item['url'] not in all_urls and
                    not news_fetcher._is_used(rss_item['url'])):
                    news_list.append(rss_item)
                    all_urls.add(rss_item['url'])
                    added += 1

            logger.info(f"Total após RSS (filtrando já usadas): {len(news_list)} notícias (máx 10)")

        if not news_list:
            logger.error("Não foi possível buscar notícias novas. Todas já foram usadas.")
            return None

        if len(news_list) < 3:
            logger.warning(f"⚠️ ATENÇÃO: Apenas {len(news_list)} notícia(s) nova(s) disponível(is)!")

        # Formata notícias para o Claude
        news_context = news_fetcher.format_news_for_ai(news_list, include_usage_info=True)

        # Monta o prompt com notícias reais
        base_prompt = get_prompt_noticia_relevante()
        full_prompt = f"{base_prompt}\n\n{news_context}\n\nAgora escolha a notícia MAIS RELEVANTE da lista acima e crie uma análise detalhada seguindo EXATAMENTE o formato especificado. Use o URL real da notícia escolhida.\n\n⚠️ IMPORTANTE: Todas as notícias listadas são NOVAS (nunca foram usadas antes) - escolha a mais impactante para o público GameFi."

        system_prompt = """Você é um analista especializado em GameFi, Web3 Gaming e Crypto Gaming.
Você receberá uma lista de notícias reais e atuais.
Sua tarefa é escolher a MAIS RELEVANTE e criar uma análise detalhada.
SEMPRE use as notícias fornecidas - não invente informações.
SEMPRE inclua o URL real da notícia que você escolher.
Siga EXATAMENTE o formato estruturado solicitado.
IMPORTANTE: Retorne APENAS o conteúdo final formatado, sem tags ou análise."""

        response = self._call_claude(full_prompt, system_prompt)

        if response:
            # Extrai URL da notícia usada e marca como usada
            url_match = re.search(r'https?://[^\s\)]+', response)
            if url_match:
                used_url = url_match.group(0).rstrip('.,;)')
                news_fetcher.mark_as_used(used_url)
                logger.info(f"✓ Notícia marcada como usada: {used_url[:60]}...")
            else:
                logger.warning("URL não encontrado na resposta - não foi possível marcar como usada")

            logger.success("Notícia relevante gerada com sucesso!")
            logger.debug(f"Preview: {response[:200]}...")

        return response
    
    def test_connection(self) -> bool:
        """
        Testa conexão com a API do Claude
        
        Returns:
            True se conectado, False caso contrário
        """
        try:
            logger.processing("Testando conexão com Claude API...")
            
            test_message = self.client.messages.create(
                model=self.model,
                max_tokens=100,
                messages=[
                    {
                        "role": "user",
                        "content": "Responda apenas: OK"
                    }
                ]
            )
            
            if test_message.content[0].text:
                logger.success("Conexão com Claude API OK!")
                return True
            
        except Exception as e:
            logger.failed(f"Falha na conexão com Claude API: {str(e)}")
        
        return False


# Instância global do processador
ai = AIProcessor()


if __name__ == "__main__":
    # Teste do processador
    logger.section("TESTE DO PROCESSADOR DE IA")
    
    # Testa conexão
    if ai.test_connection():
        print("\n✅ Claude API está funcionando!\n")
    else:
        print("\n❌ Erro na conexão com Claude API!\n")