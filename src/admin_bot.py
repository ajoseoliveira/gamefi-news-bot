"""
Bot Administrativo - Painel de Controle GameFi RADAR BR
"""

import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode
import os

from utils.logger import logger
from src.admin_commands import AdminCommands

# Credenciais do bot administrativo
ADMIN_BOT_TOKEN = "8311083725:AAE-McyaMbDuIjFWgw1THaaPeAVtkM5totk"
ADMIN_USER_ID = 1274233631


class AdminBot:
    """Bot administrativo para gerenciar o sistema de notícias"""
    
    def __init__(self):
        self.admin_id = ADMIN_USER_ID
        self.commands = AdminCommands()
        self.app = Application.builder().token(ADMIN_BOT_TOKEN).build()
        
        # Registra handlers
        self._register_handlers()
        
        logger.info(f"Admin Bot inicializado (Autorizado: {self.admin_id})")
    
    def _check_admin(self, user_id: int) -> bool:
        """Verifica se o usuário é admin"""
        return user_id == self.admin_id
    
    def _register_handlers(self):
        """Registra todos os handlers de comandos"""
        self.app.add_handler(CommandHandler("start", self.cmd_start))
        self.app.add_handler(CommandHandler("menu", self.cmd_menu))
        self.app.add_handler(CommandHandler("status", self.cmd_status))
        self.app.add_handler(CommandHandler("stats", self.cmd_stats))
        self.app.add_handler(CommandHandler("logs", self.cmd_logs))
        self.app.add_handler(CommandHandler("help", self.cmd_help))
        
        # Callback queries (botões)
        self.app.add_handler(CallbackQueryHandler(self.handle_callback))
    
    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /start"""
        user_id = update.effective_user.id
        
        if not self._check_admin(user_id):
            await update.message.reply_text("🚫 Acesso negado. Você não tem permissão para usar este bot.")
            return
        
        await update.message.reply_text(
            "🎮 <b>GameFi RADAR BR - Painel Administrativo</b>\n\n"
            "Bem-vindo ao painel de controle!\n\n"
            "Use /menu para acessar o painel principal.",
            parse_mode=ParseMode.HTML
        )
    
    async def cmd_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Mostra menu principal com botões"""
        user_id = update.effective_user.id
        
        if not self._check_admin(user_id):
            await update.message.reply_text("🚫 Acesso negado.")
            return
        
        keyboard = [
            [
                InlineKeyboardButton("📊 Status", callback_data="status"),
                InlineKeyboardButton("📈 Estatísticas", callback_data="stats")
            ],
            [
                InlineKeyboardButton("📝 Logs", callback_data="logs"),
                InlineKeyboardButton("ℹ️ Ajuda", callback_data="help")
            ],
            [
                InlineKeyboardButton("⏸️ Pausar", callback_data="pause"),
                InlineKeyboardButton("▶️ Retomar", callback_data="resume")
            ],
            [
                InlineKeyboardButton("🧪 Testar Resumo", callback_data="test_resumo"),
                InlineKeyboardButton("🧪 Testar Notícia", callback_data="test_noticia")
            ],
            [
                InlineKeyboardButton("📤 Postar Resumo AGORA", callback_data="post_resumo"),
                InlineKeyboardButton("📤 Postar Notícia AGORA", callback_data="post_noticia")
            ],
            [
                InlineKeyboardButton("🗑️ Limpar Cache", callback_data="clear_cache"),
                InlineKeyboardButton("🗑️ Limpar Histórico", callback_data="clear_history")
            ],
            [
                InlineKeyboardButton("🔧 Modo: Test", callback_data="mode_test"),
                InlineKeyboardButton("🔧 Modo: Production", callback_data="mode_production")
            ],
            [
                InlineKeyboardButton("⏰ Ver Horários", callback_data="show_schedule")
            ]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🎛️ <b>PAINEL DE CONTROLE</b>\n\n"
            "Escolha uma opção abaixo:",
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handler para callbacks dos botões"""
        query = update.callback_query
        user_id = query.from_user.id
        
        if not self._check_admin(user_id):
            await query.answer("🚫 Acesso negado", show_alert=True)
            return
        
        await query.answer()
        
        action = query.data
        
        # Mapeia ações para métodos
        actions = {
            "status": self.commands.get_status,
            "stats": self.commands.get_stats,
            "logs": self.commands.get_logs,
            "help": self.commands.get_help,
            "pause": self.commands.pause_bot,
            "resume": self.commands.resume_bot,
            "test_resumo": self.commands.test_resumo,
            "test_noticia": self.commands.test_noticia,
            "post_resumo": self.commands.post_resumo_now,
            "post_noticia": self.commands.post_noticia_now,
            "clear_cache": self.commands.clear_cache,
            "clear_history": self.commands.clear_history,
            "mode_test": self.commands.set_mode_test,
            "mode_production": self.commands.set_mode_production,
            "show_schedule": self.commands.show_schedule
        }
        
        if action in actions:
            response = await actions[action]()
            
            # Se resposta for muito longa, divide em mensagens
            if len(response) > 4000:
                chunks = [response[i:i+4000] for i in range(0, len(response), 4000)]
                for chunk in chunks:
                    await query.message.reply_text(chunk, parse_mode=ParseMode.HTML)
            else:
                await query.message.reply_text(response, parse_mode=ParseMode.HTML)
    
    async def cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /status"""
        user_id = update.effective_user.id
        
        if not self._check_admin(user_id):
            await update.message.reply_text("🚫 Acesso negado.")
            return
        
        response = await self.commands.get_status()
        await update.message.reply_text(response, parse_mode=ParseMode.HTML)
    
    async def cmd_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /stats"""
        user_id = update.effective_user.id
        
        if not self._check_admin(user_id):
            await update.message.reply_text("🚫 Acesso negado.")
            return
        
        response = await self.commands.get_stats()
        await update.message.reply_text(response, parse_mode=ParseMode.HTML)
    
    async def cmd_logs(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /logs"""
        user_id = update.effective_user.id
        
        if not self._check_admin(user_id):
            await update.message.reply_text("🚫 Acesso negado.")
            return
        
        response = await self.commands.get_logs()
        await update.message.reply_text(response, parse_mode=ParseMode.HTML)
    
    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Comando /help"""
        user_id = update.effective_user.id
        
        if not self._check_admin(user_id):
            await update.message.reply_text("🚫 Acesso negado.")
            return
        
        response = await self.commands.get_help()
        await update.message.reply_text(response, parse_mode=ParseMode.HTML)
    
    def run(self):
        """Inicia o bot administrativo"""
        logger.info("🤖 Admin Bot iniciando...")
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    admin_bot = AdminBot()
    admin_bot.run()