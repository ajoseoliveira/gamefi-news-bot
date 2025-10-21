#!/usr/bin/env python3
"""
Painel Administrativo - GameFi RADAR BR Bot
"""

import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
sys.path.insert(0, str(Path(__file__).parent))

from src.admin_bot import AdminBot

if __name__ == "__main__":
    admin_bot = AdminBot()
    admin_bot.run()