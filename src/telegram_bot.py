"""
Bot do Telegram para postar notícias no canal
"""

import asyncio
from telegram import Bot
from telegram.constants import ParseMode
from telegram.error import TelegramError

from config.config import (
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHANNEL_ID,
    CHANNEL_NAME,
    MODE
)
from utils.logger import logger
from config.config import (
    TELEGRAM_RETRIES,
    TELEGRAM_RETRY_BACKOFF,
    TELEGRAM_POOL_SIZE,
    TELEGRAM_POOL_TIMEOUT,
    TELEGRAM_READ_TIMEOUT,
    TELEGRAM_CONNECT_TIMEOUT,
)
from utils.database import db


class TelegramPoster:
    """Gerencia postagens no canal do Telegram"""
    
    def __init__(self):
        if not TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN não configurado!")
        
        self.bot = Bot(token=TELEGRAM_BOT_TOKEN)
        self.channel_id = TELEGRAM_CHANNEL_ID
        self.mode = MODE
        
        logger.info(f"Telegram Bot inicializado (Canal: {CHANNEL_NAME})")
        logger.info(f"Modo: {self.mode.upper()}")
        
        # Reconfigura cliente HTTP do Telegram com pool/timeout ajustáveis
        try:
            from telegram.request import HTTPXRequest
            request = HTTPXRequest(
                connection_pool_size=TELEGRAM_POOL_SIZE,
                pool_timeout=TELEGRAM_POOL_TIMEOUT,
                read_timeout=TELEGRAM_READ_TIMEOUT,
                connect_timeout=TELEGRAM_CONNECT_TIMEOUT,
            )
            # Substitui o bot por uma instância com request configurado
            self.bot = Bot(token=TELEGRAM_BOT_TOKEN, request=request)
        except Exception as _e:
            logger.warning("Não foi possível aplicar configuração avançada do cliente HTTP do Telegram. Usando padrão.")
    
    def _convert_markdown_to_html(self, text: str) -> str:
        """
        Converte formatação Markdown para HTML (Telegram)
        
        Args:
            text: Texto com markdown
        
        Returns:
            Texto com tags HTML
        """
        # Converte ** para negrito <b>
        import re
        
        # Negrito: **texto** -> <b>texto</b>
        text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
        
        # Itálico: *texto* -> <i>texto</i> (apenas asterisco único)
        text = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'<i>\1</i>', text)
        
        # Links: [texto](url) -> <a href="url">texto</a>
        text = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', text)
        
        return text
    
    async def _send_message(self, text: str) -> bool:
        """
        Envia mensagem para o canal
        
        Args:
            text: Texto a ser enviado
        
        Returns:
            True se enviado com sucesso, False caso contrário
        """
        try:
            # Converte markdown para HTML
            text_html = self._convert_markdown_to_html(text)
            
            await self.bot.send_message(
                chat_id=self.channel_id,
                text=text_html,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=False
            )
            return True
        except TelegramError as e:
            logger.error(f"Erro ao enviar mensagem: {str(e)}")
            return False
    
    async def post_resumo_diario(self, content: str) -> bool:
        """
        Posta resumo diário no canal
        
        Args:
            content: Conteúdo do resumo
        
        Returns:
            True se postado com sucesso
        """
        logger.section("POSTANDO RESUMO DIÁRIO")
        
        if not content:
            logger.failed("Conteúdo vazio! Nada para postar.")
            return False
        
        # Verifica duplicação
        if db.is_duplicate(content):
            logger.warning("Conteúdo duplicado detectado. Pulando postagem.")
            return False
        
        # Modo teste: apenas mostra no console
        if self.mode == "test":
            logger.info("🧪 MODO TESTE - Conteúdo que seria postado:")
            print("\n" + "="*60)
            print(content)
            print("="*60 + "\n")
            logger.info("✅ Em modo produção, seria postado no canal agora.")
            return True
        
        # Modo produção: posta no canal
        try:
            success = False
            for i in range(max(1, TELEGRAM_RETRIES)):
                success = await self._send_message(content)
                if success:
                    break
                # Pool pode estar saturado: recria cliente e aguarda backoff
                try:
                    from telegram.request import HTTPXRequest
                    request = HTTPXRequest(
                        connection_pool_size=TELEGRAM_POOL_SIZE,
                        pool_timeout=TELEGRAM_POOL_TIMEOUT,
                        read_timeout=TELEGRAM_READ_TIMEOUT,
                        connect_timeout=TELEGRAM_CONNECT_TIMEOUT,
                    )
                    self.bot = Bot(token=TELEGRAM_BOT_TOKEN, request=request)
                except Exception:
                    pass
                await asyncio.sleep(TELEGRAM_RETRY_BACKOFF * (i + 1))
            
            if success:
                logger.success(f"Resumo diário postado em {CHANNEL_NAME}!")
                db.add_post("resumo_diario", content, "Resumo Diário")
                return True
            else:
                logger.failed("Falha ao postar resumo diário")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao postar: {str(e)}")
            return False
    
    async def post_noticia_relevante(self, content: str) -> bool:
        """
        Posta notícia relevante no canal
        
        Args:
            content: Conteúdo da notícia
        
        Returns:
            True se postado com sucesso
        """
        logger.section("POSTANDO NOTÍCIA RELEVANTE")
        
        if not content:
            logger.failed("Conteúdo vazio! Nada para postar.")
            return False
        
        # Verifica duplicação
        if db.is_duplicate(content):
            logger.warning("Conteúdo duplicado detectado. Pulando postagem.")
            return False
        
        # Modo teste: apenas mostra no console
        if self.mode == "test":
            logger.info("🧪 MODO TESTE - Conteúdo que seria postado:")
            print("\n" + "="*60)
            print(content)
            print("="*60 + "\n")
            logger.info("✅ Em modo produção, seria postado no canal agora.")
            return True
        
        # Modo produção: posta no canal
        try:
            success = False
            for i in range(max(1, TELEGRAM_RETRIES)):
                success = await self._send_message(content)
                if success:
                    break
                # Pool pode estar saturado: recria cliente e aguarda backoff
                try:
                    from telegram.request import HTTPXRequest
                    request = HTTPXRequest(
                        connection_pool_size=TELEGRAM_POOL_SIZE,
                        pool_timeout=TELEGRAM_POOL_TIMEOUT,
                        read_timeout=TELEGRAM_READ_TIMEOUT,
                        connect_timeout=TELEGRAM_CONNECT_TIMEOUT,
                    )
                    self.bot = Bot(token=TELEGRAM_BOT_TOKEN, request=request)
                except Exception:
                    pass
                await asyncio.sleep(TELEGRAM_RETRY_BACKOFF * (i + 1))
            
            if success:
                logger.success(f"Notícia relevante postada em {CHANNEL_NAME}!")
                
                # Extrai título da notícia (primeira linha em negrito)
                title = content.split('\n')[0].replace('**', '').strip()
                db.add_post("noticia_relevante", content, title)
                return True
            else:
                logger.failed("Falha ao postar notícia relevante")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao postar: {str(e)}")
            return False
    
    async def test_connection(self) -> bool:
        """
        Testa conexão com o bot e permissões no canal
        
        Returns:
            True se conectado, False caso contrário
        """
        try:
            logger.processing("Testando conexão com Telegram Bot...")
            
            # Testa bot
            bot_info = await self.bot.get_me()
            logger.success(f"Bot conectado: @{bot_info.username}")
            
            # Tenta obter info do canal
            try:
                chat = await self.bot.get_chat(self.channel_id)
                logger.success(f"Canal encontrado: {chat.title}")
                
                # Verifica permissões
                bot_member = await self.bot.get_chat_member(
                    self.channel_id,
                    bot_info.id
                )
                
                if bot_member.can_post_messages or bot_member.status == 'administrator':
                    logger.success("Bot tem permissão para postar no canal!")
                    return True
                else:
                    logger.warning("Bot não tem permissão para postar no canal!")
                    logger.info("👉 Adicione o bot como administrador do canal")
                    return False
                    
            except TelegramError as e:
                logger.warning(f"Não foi possível verificar o canal: {str(e)}")
                logger.info(f"👉 Certifique-se que o bot foi adicionado ao canal: {self.channel_id}")
                logger.info("👉 O bot precisa ser administrador do canal")
                return False
                
        except TelegramError as e:
            logger.failed(f"Erro na conexão com Telegram: {str(e)}")
            logger.info("👉 Verifique se o TELEGRAM_BOT_TOKEN está correto")
            return False


# Instância global do poster
telegram = TelegramPoster()


if __name__ == "__main__":
    # Teste do bot
    logger.section("TESTE DO TELEGRAM BOT")
    
    # Testa conexão
    connected = asyncio.run(telegram.test_connection())
    
    if connected:
        print("\n✅ Telegram Bot está funcionando!")
        print(f"📢 Canal: {CHANNEL_NAME}")
        print(f"🆔 ID: {TELEGRAM_CHANNEL_ID}\n")
    else:
        print("\n❌ Problemas na conexão com Telegram!")
