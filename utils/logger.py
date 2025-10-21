"""
Sistema de logs personalizado para o GameFi RADAR BR Bot
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
import colorlog

from config.config import LOG_LEVEL, LOG_FILE, LOGS_DIR


class BotLogger:
    """Logger personalizado com cores e formatação"""
    
    def __init__(self, name="GameFiBot"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, LOG_LEVEL))
        
        # Remove handlers existentes
        self.logger.handlers = []
        
        # Handler para console (com cores)
        self._setup_console_handler()
        
        # Handler para arquivo
        self._setup_file_handler()
    
    def _setup_console_handler(self):
        """Configura handler colorido para o console"""
        console_handler = colorlog.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, LOG_LEVEL))
        
        # Formato colorido
        console_format = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s [%(levelname)s]%(reset)s %(message)s',
            datefmt='%H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            }
        )
        
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)
    
    def _setup_file_handler(self):
        """Configura handler para arquivo de log"""
        # Garante que o diretório existe
        LOGS_DIR.mkdir(exist_ok=True)
        
        file_handler = logging.FileHandler(
            LOG_FILE,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)  # Arquivo sempre grava tudo
        
        # Formato para arquivo (sem cores)
        file_format = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        file_handler.setFormatter(file_format)
        self.logger.addHandler(file_handler)
    
    def info(self, message):
        """Log de informação"""
        self.logger.info(message)
    
    def debug(self, message):
        """Log de debug"""
        self.logger.debug(message)
    
    def warning(self, message):
        """Log de aviso"""
        self.logger.warning(message)
    
    def error(self, message):
        """Log de erro"""
        self.logger.error(message)
    
    def critical(self, message):
        """Log crítico"""
        self.logger.critical(message)
    
    def section(self, title):
        """Cria uma seção visual no log"""
        separator = "=" * 60
        self.logger.info(f"\n{separator}")
        self.logger.info(f"  {title}")
        self.logger.info(f"{separator}\n")
    
    def success(self, message):
        """Log de sucesso (info com emoji)"""
        self.logger.info(f"✅ {message}")
    
    def failed(self, message):
        """Log de falha (error com emoji)"""
        self.logger.error(f"❌ {message}")
    
    def processing(self, message):
        """Log de processamento (info com emoji)"""
        self.logger.info(f"⚙️  {message}")
    
    def posting(self, message):
        """Log de postagem (info com emoji)"""
        self.logger.info(f"📤 {message}")


# Instância global do logger
logger = BotLogger()


def log_execution(func):
    """Decorator para logar execução de funções"""
    def wrapper(*args, **kwargs):
        logger.debug(f"Executando: {func.__name__}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Concluído: {func.__name__}")
            return result
        except Exception as e:
            logger.error(f"Erro em {func.__name__}: {str(e)}")
            raise
    return wrapper


if __name__ == "__main__":
    # Teste do logger
    logger.section("TESTE DO SISTEMA DE LOGS")
    logger.info("Mensagem de informação")
    logger.debug("Mensagem de debug")
    logger.warning("Mensagem de aviso")
    logger.error("Mensagem de erro")
    logger.success("Operação bem-sucedida!")
    logger.failed("Operação falhou!")
    logger.processing("Processando dados...")
    logger.posting("Postando no canal...")
    print(f"\n📁 Logs salvos em: {LOG_FILE}")