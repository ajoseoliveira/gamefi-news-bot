"""
Sistema de agendamento para postagens automáticas
"""
import asyncio
import schedule
import time
from datetime import datetime
import pytz

from config.config import (
    SCHEDULE_RESUMO_DIARIO,
    SCHEDULE_NOTICIA_RELEVANTE_1,
    SCHEDULE_NOTICIA_RELEVANTE_2,
    TIMEZONE,
    CHANNEL_NAME
)
from src.ai_processor import ai
from src.telegram_bot import telegram
from utils.logger import logger
from utils.database import db


class BotScheduler:
    """Gerencia o agendamento de todas as postagens"""
    
    def __init__(self):
        self.timezone = pytz.timezone(TIMEZONE)
        self.is_running = False
        logger.info(f"Scheduler inicializado (Timezone: {TIMEZONE})")
    
    def job_resumo_diario(self):
        """Job: Gera e posta o resumo diário"""
        logger.section(f"🕐 EXECUTANDO JOB: RESUMO DIÁRIO ({self._get_current_time()})")
        
        try:
            # Gera conteúdo com IA
            content = ai.generate_resumo_diario()
            
            if content:
                # Posta no Telegram
                success = asyncio.run(telegram.post_resumo_diario(content))
                
                if success:
                    logger.success("✅ Resumo diário completado com sucesso!")
                else:
                    logger.failed("❌ Falha ao postar resumo diário")
            else:
                logger.failed("❌ Falha ao gerar conteúdo do resumo diário")
                
        except Exception as e:
            logger.error(f"Erro no job de resumo diário: {str(e)}")
    
    def job_noticia_relevante(self):
        """Job: Gera e posta uma notícia relevante"""
        logger.section(f"🕐 EXECUTANDO JOB: NOTÍCIA RELEVANTE ({self._get_current_time()})")
        
        try:
            # Gera conteúdo com IA
            content = ai.generate_noticia_relevante()
            
            if content:
                # Posta no Telegram
                success = asyncio.run(telegram.post_noticia_relevante(content))
                
                if success:
                    logger.success("✅ Notícia relevante completada com sucesso!")
                else:
                    logger.failed("❌ Falha ao postar notícia relevante")
            else:
                logger.failed("❌ Falha ao gerar conteúdo da notícia relevante")
                
        except Exception as e:
            logger.error(f"Erro no job de notícia relevante: {str(e)}")
    
    def _get_current_time(self) -> str:
        """Retorna horário atual formatado"""
        now = datetime.now(self.timezone)
        return now.strftime("%d/%m/%Y %H:%M:%S")
    
    def setup_schedule(self):
        """Configura todos os agendamentos"""
        logger.section("CONFIGURANDO AGENDAMENTOS")
        
        # Limpa agendamentos anteriores
        schedule.clear()
        
        # Resumo Diário
        schedule.every().day.at(SCHEDULE_RESUMO_DIARIO).do(self.job_resumo_diario)
        logger.info(f"✅ Resumo Diário agendado para {SCHEDULE_RESUMO_DIARIO}")
        
        # Notícia Relevante 1
        schedule.every().day.at(SCHEDULE_NOTICIA_RELEVANTE_1).do(self.job_noticia_relevante)
        logger.info(f"✅ Notícia Relevante 1 agendada para {SCHEDULE_NOTICIA_RELEVANTE_1}")
        
        # Notícia Relevante 2
        schedule.every().day.at(SCHEDULE_NOTICIA_RELEVANTE_2).do(self.job_noticia_relevante)
        logger.info(f"✅ Notícia Relevante 2 agendada para {SCHEDULE_NOTICIA_RELEVANTE_2}")
        
        # Limpeza de banco de dados (todo dia às 00:00)
        schedule.every().day.at("00:00").do(self._cleanup_job)
        logger.info(f"✅ Limpeza de banco agendada para 00:00")
        
        logger.success("Todos os agendamentos configurados!")
    
    def _cleanup_job(self):
        """Job de limpeza do banco de dados"""
        logger.info("🧹 Executando limpeza do banco de dados...")
        db.clean_old_posts(days=30)
    
    def run_now(self, job_type: str):
        """
        Executa um job imediatamente (para testes)
        
        Args:
            job_type: 'resumo' ou 'noticia'
        """
        if job_type == 'resumo':
            self.job_resumo_diario()
        elif job_type == 'noticia':
            self.job_noticia_relevante()
        else:
            logger.error(f"Tipo de job inválido: {job_type}")
    
    def start(self):
        """Inicia o loop do scheduler"""
        self.setup_schedule()
        self.is_running = True
        
        logger.section(f"BOT INICIADO: {CHANNEL_NAME}")
        logger.info(f"⏰ Horário atual: {self._get_current_time()}")
        logger.info(f"📅 Próximas execuções:")
        
        for job in schedule.get_jobs():
            next_run = job.next_run
            if next_run:
                next_run_str = next_run.strftime("%d/%m/%Y %H:%M:%S")
                logger.info(f"   • {next_run_str}")
        
        logger.info("\n🤖 Bot rodando... (Ctrl+C para parar)\n")
        
        try:
            while self.is_running:
                schedule.run_pending()
                time.sleep(30)  # Checa a cada 30 segundos
                
        except KeyboardInterrupt:
            logger.warning("\n⚠️  Interrompido pelo usuário")
            self.stop()
    
    def stop(self):
        """Para o scheduler"""
        self.is_running = False
        schedule.clear()
        logger.info("🛑 Scheduler parado")
    
    def get_status(self):
        """Retorna status dos agendamentos"""
        logger.section("STATUS DO SCHEDULER")
        
        if not schedule.get_jobs():
            logger.warning("Nenhum job agendado")
            return
        
        logger.info(f"⏰ Horário atual: {self._get_current_time()}")
        logger.info(f"📊 Total de jobs: {len(schedule.get_jobs())}")
        logger.info("\n📅 Próximas execuções:")
        
        for i, job in enumerate(schedule.get_jobs(), 1):
            next_run = job.next_run
            if next_run:
                next_run_str = next_run.strftime("%d/%m/%Y %H:%M:%S")
                logger.info(f"   {i}. {next_run_str}")
        
        # Estatísticas do banco
        stats = db.get_stats()
        logger.info(f"\n📊 Estatísticas:")
        logger.info(f"   • Total de posts: {stats['total_posts']}")
        logger.info(f"   • Resumos diários: {stats['resumos']}")
        logger.info(f"   • Notícias relevantes: {stats['noticias']}")
        if stats['last_post']:
            logger.info(f"   • Último post: {stats['last_post']}")


# Instância global do scheduler
scheduler = BotScheduler()


if __name__ == "__main__":
    # Teste do scheduler
    logger.section("TESTE DO SCHEDULER")
    
    scheduler.setup_schedule()
    scheduler.get_status()
    
    print("\n💡 Para testar execução imediata:")
    print("   scheduler.run_now('resumo')  # Testa resumo diário")
    print("   scheduler.run_now('noticia')  # Testa notícia relevante")