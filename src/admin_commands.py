"""
Comandos administrativos para o painel de controle
"""

import os
from datetime import datetime
from pathlib import Path
import pytz

from config.config import (
    MODE, SCHEDULE_RESUMO_DIARIO, SCHEDULE_NOTICIA_RELEVANTE_1,
    SCHEDULE_NOTICIA_RELEVANTE_2, TIMEZONE, LOG_FILE
)
from utils.database import db
from src.news_fetcher import news_fetcher
from src.ai_processor import ai
from src.telegram_bot import telegram
from utils.logger import logger


class AdminCommands:
    """Lógica dos comandos administrativos"""
    
    def __init__(self):
        self.paused = False
        self.tz = pytz.timezone(TIMEZONE)
    
    async def get_status(self) -> str:
        """Retorna status atual do bot"""
        now = datetime.now(self.tz)
        modo = os.getenv('MODE', 'test').upper()
        
        status_emoji = "✅" if not self.paused else "⏸️"
        modo_emoji = "🔴" if modo == "PRODUCTION" else "🟡"
        
        response = f"""
📊 <b>STATUS DO BOT</b>

{status_emoji} Estado: {'PAUSADO' if self.paused else 'ATIVO'}
{modo_emoji} Modo: {modo}
🕐 Hora atual: {now.strftime('%d/%m/%Y %H:%M:%S')}

⏰ <b>Próximas Postagens:</b>
• Resumo Diário: {SCHEDULE_RESUMO_DIARIO}
• Notícia Relevante 1: {SCHEDULE_NOTICIA_RELEVANTE_1}
• Notícia Relevante 2: {SCHEDULE_NOTICIA_RELEVANTE_2}

📍 Timezone: {TIMEZONE}
"""
        return response.strip()
    
    async def get_stats(self) -> str:
        """Retorna estatísticas do bot"""
        stats = db.get_stats()
        cache_stats = news_fetcher.get_cache_stats()
        
        response = f"""
📈 <b>ESTATÍSTICAS</b>

📰 <b>Postagens:</b>
• Total: {stats['total_posts']}
• Resumos Diários: {stats['resumos']}
• Notícias Relevantes: {stats['noticias']}

🗓️ <b>Histórico:</b>
• Primeiro post: {stats['first_post'] or 'Nenhum'}
• Último post: {stats['last_post'] or 'Nenhum'}

🗂️ <b>Cache de Notícias:</b>
• Notícias usadas: {cache_stats['total_used']}
• Última limpeza: {cache_stats['last_cleanup']}
"""
        return response.strip()
    
    async def get_logs(self) -> str:
        """Retorna últimas 20 linhas do log"""
        try:
            if not LOG_FILE.exists():
                return "📝 <b>LOGS</b>\n\nArquivo de log não encontrado."
            
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                last_20 = lines[-20:] if len(lines) >= 20 else lines
            
            log_text = ''.join(last_20)
            
            response = f"""
📝 <b>ÚLTIMAS 20 LINHAS DO LOG</b>

<code>{log_text}</code>
"""
            return response.strip()
        except Exception as e:
            return f"❌ Erro ao ler logs: {str(e)}"
    
    async def get_help(self) -> str:
        """Retorna ajuda com todos os comandos"""
        response = """
ℹ️ <b>COMANDOS DISPONÍVEIS</b>

<b>📊 Monitoramento:</b>
/status - Status e próximas postagens
/stats - Estatísticas completas
/logs - Últimas 20 linhas do log

<b>⚙️ Controle:</b>
⏸️ Pausar - Pausar postagens automáticas
▶️ Retomar - Retomar postagens

<b>🧪 Testes:</b>
🧪 Testar Resumo - Gerar resumo (sem postar)
🧪 Testar Notícia - Gerar notícia (sem postar)

<b>📤 Postagem Manual:</b>
📤 Postar Resumo AGORA - Força postagem imediata
📤 Postar Notícia AGORA - Força postagem imediata

<b>🗑️ Limpeza:</b>
🗑️ Limpar Cache - Remove cache de notícias
🗑️ Limpar Histórico - Remove histórico de posts

<b>🔧 Configuração:</b>
Modo Test - Simula postagens (não posta)
Modo Production - Posta no canal real
⏰ Ver Horários - Mostra horários configurados

Use /menu para acessar o painel com botões.
"""
        return response.strip()
    
    async def pause_bot(self) -> str:
        """Pausa postagens automáticas"""
        self.paused = True
        logger.warning("⏸️ Bot pausado via painel admin")
        return "⏸️ <b>Bot pausado!</b>\n\nPostagens automáticas foram desativadas temporariamente.\nUse 'Retomar' para reativar."
    
    async def resume_bot(self) -> str:
        """Retoma postagens automáticas"""
        self.paused = False
        logger.info("▶️ Bot retomado via painel admin")
        return "▶️ <b>Bot retomado!</b>\n\nPostagens automáticas foram reativadas."
    
    async def test_resumo(self) -> str:
        """Testa geração de resumo diário"""
        logger.info("🧪 Gerando resumo de teste via painel admin...")
        
        content = ai.generate_resumo_diario()
        
        if content:
            return f"✅ <b>Resumo gerado com sucesso!</b>\n\n{content[:500]}...\n\n<i>(Não foi postado no canal)</i>"
        else:
            return "❌ Erro ao gerar resumo diário."
    
    async def test_noticia(self) -> str:
        """Testa geração de notícia relevante"""
        logger.info("🧪 Gerando notícia de teste via painel admin...")
        
        content = ai.generate_noticia_relevante()
        
        if content:
            return f"✅ <b>Notícia gerada com sucesso!</b>\n\n{content[:500]}...\n\n<i>(Não foi postada no canal)</i>"
        else:
            return "❌ Erro ao gerar notícia relevante."
    
    async def post_resumo_now(self) -> str:
        """Força postagem de resumo diário"""
        logger.info("📤 Postando resumo via painel admin...")
        
        content = ai.generate_resumo_diario()
        
        if content:
            success = await telegram.post_resumo_diario(content)
            if success:
                return "✅ <b>Resumo postado com sucesso!</b>"
            else:
                return "❌ Erro ao postar resumo."
        else:
            return "❌ Erro ao gerar resumo."
    
    async def post_noticia_now(self) -> str:
        """Força postagem de notícia relevante"""
        logger.info("📤 Postando notícia via painel admin...")
        
        content = ai.generate_noticia_relevante()
        
        if content:
            success = await telegram.post_noticia_relevante(content)
            if success:
                return "✅ <b>Notícia postada com sucesso!</b>"
            else:
                return "❌ Erro ao postar notícia."
        else:
            return "❌ Erro ao gerar notícia."
    
    async def clear_cache(self) -> str:
        """Limpa cache de notícias usadas"""
        try:
            cache_file = Path("data/used_news_cache.json")
            if cache_file.exists():
                cache_file.unlink()
            
            logger.warning("🗑️ Cache de notícias limpo via painel admin")
            return "✅ <b>Cache limpo!</b>\n\nTodas as notícias podem ser usadas novamente."
        except Exception as e:
            return f"❌ Erro ao limpar cache: {str(e)}"
    
    async def clear_history(self) -> str:
        """Limpa histórico de postagens"""
        try:
            history_file = Path("data/posted_news.json")
            if history_file.exists():
                history_file.unlink()
            
            logger.warning("🗑️ Histórico de postagens limpo via painel admin")
            return "✅ <b>Histórico limpo!</b>\n\nTodas as postagens anteriores foram removidas do registro."
        except Exception as e:
            return f"❌ Erro ao limpar histórico: {str(e)}"
    
    async def set_mode_test(self) -> str:
        """Muda para modo test"""
        try:
            env_file = Path(".env")
            if env_file.exists():
                content = env_file.read_text(encoding='utf-8')
                content = content.replace('MODE=production', 'MODE=test')
                content = content.replace('MODE=PRODUCTION', 'MODE=test')
                env_file.write_text(content, encoding='utf-8')
            
            os.environ['MODE'] = 'test'
            logger.info("🔧 Modo alterado para TEST via painel admin")
            return "🟡 <b>Modo TEST ativado!</b>\n\nPostagens serão simuladas, não serão postadas no canal.\n\n⚠️ Reinicie o bot principal (main.py) para aplicar."
        except Exception as e:
            return f"❌ Erro: {str(e)}"
    
    async def set_mode_production(self) -> str:
        """Muda para modo production"""
        try:
            env_file = Path(".env")
            if env_file.exists():
                content = env_file.read_text(encoding='utf-8')
                content = content.replace('MODE=test', 'MODE=production')
                content = content.replace('MODE=TEST', 'MODE=production')
                env_file.write_text(content, encoding='utf-8')
            
            os.environ['MODE'] = 'production'
            logger.warning("🔧 Modo alterado para PRODUCTION via painel admin")
            return "🔴 <b>Modo PRODUCTION ativado!</b>\n\nPostagens serão feitas no canal real.\n\n⚠️ Reinicie o bot principal (main.py) para aplicar."
        except Exception as e:
            return f"❌ Erro: {str(e)}"
    
    async def show_schedule(self) -> str:
        """Mostra horários configurados"""
        response = f"""
⏰ <b>HORÁRIOS CONFIGURADOS</b>

📅 <b>Postagens Diárias:</b>

🌅 <b>Manhã:</b>
• {SCHEDULE_RESUMO_DIARIO} - Resumo Diário
  (5 notícias principais do dia)

🌤️ <b>Tarde:</b>
• {SCHEDULE_NOTICIA_RELEVANTE_1} - Notícia Relevante
  (Análise detalhada)

🌆 <b>Noite:</b>
• {SCHEDULE_NOTICIA_RELEVANTE_2} - Notícia Relevante
  (Análise detalhada)

📍 Timezone: {TIMEZONE}

<i>Para alterar horários, edite o arquivo .env</i>
"""
        return response.strip()