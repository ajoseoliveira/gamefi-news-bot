#!/usr/bin/env python3
"""
Script de testes para o GameFi RADAR BR Bot
Use este script para testar o bot antes de colocar em produção
"""

import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config.config import validate_config, print_config
from src.ai_processor import ai
from src.telegram_bot import telegram
from src.scheduler import scheduler
from utils.logger import logger


def test_all():
    """Executa todos os testes"""
    
    print("\n" + "="*60)
    print("🧪 TESTANDO GameFi RADAR BR Bot")
    print("="*60 + "\n")
    
    # 1. Valida configurações
    logger.section("1. VALIDANDO CONFIGURAÇÕES")
    if not validate_config():
        logger.critical("❌ Configurações inválidas!")
        return False
    logger.success("Configurações OK!")
    
    # 2. Testa Claude API
    logger.section("2. TESTANDO CLAUDE API")
    if not ai.test_connection():
        logger.critical("❌ Claude API não está funcionando!")
        return False
    logger.success("Claude API OK!")
    
    # 3. Testa Telegram Bot
    logger.section("3. TESTANDO TELEGRAM BOT")
    if not asyncio.run(telegram.test_connection()):
        logger.critical("❌ Telegram Bot não está funcionando!")
        return False
    logger.success("Telegram Bot OK!")
    
    # 4. Mostra agendamentos
    logger.section("4. VERIFICANDO AGENDAMENTOS")
    scheduler.setup_schedule()
    scheduler.get_status()
    
    logger.section("✅ TODOS OS TESTES PASSARAM!")
    
    return True


def test_resumo_diario():
    """Testa geração e postagem de resumo diário"""
    
    logger.section("🧪 TESTE: RESUMO DIÁRIO")
    
    logger.info("Gerando resumo diário...")
    content = ai.generate_resumo_diario()
    
    if content:
        print("\n" + "="*60)
        print("CONTEÚDO GERADO:")
        print("="*60)
        print(content)
        print("="*60 + "\n")
        
        resposta = input("Deseja postar este conteúdo? (s/N): ").lower()
        if resposta == 's':
            success = telegram.post_resumo_diario(content)
            if success:
                logger.success("✅ Resumo diário postado com sucesso!")
            else:
                logger.failed("❌ Falha ao postar")
        else:
            logger.info("Postagem cancelada pelo usuário")
    else:
        logger.failed("❌ Falha ao gerar conteúdo")


def test_noticia_relevante():
    """Testa geração e postagem de notícia relevante"""
    
    logger.section("🧪 TESTE: NOTÍCIA RELEVANTE")
    
    logger.info("Gerando notícia relevante...")
    content = ai.generate_noticia_relevante()
    
    if content:
        print("\n" + "="*60)
        print("CONTEÚDO GERADO:")
        print("="*60)
        print(content)
        print("="*60 + "\n")
        
        resposta = input("Deseja postar este conteúdo? (s/N): ").lower()
        if resposta == 's':
            success = telegram.post_noticia_relevante(content)
            if success:
                logger.success("✅ Notícia relevante postada com sucesso!")
            else:
                logger.failed("❌ Falha ao postar")
        else:
            logger.info("Postagem cancelada pelo usuário")
    else:
        logger.failed("❌ Falha ao gerar conteúdo")


def menu():
    """Menu interativo de testes"""
    
    while True:
        print("\n" + "="*60)
        print("🧪 MENU DE TESTES - GameFi RADAR BR Bot")
        print("="*60)
        print("\n1. Executar todos os testes")
        print("2. Testar apenas Claude API")
        print("3. Testar apenas Telegram Bot")
        print("4. Testar geração de Resumo Diário")
        print("5. Testar geração de Notícia Relevante")
        print("6. Ver status e agendamentos")
        print("7. Ver estatísticas do banco de dados")
        print("8. Executar resumo diário AGORA")
        print("9. Executar notícia relevante AGORA")
        print("0. Sair")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            test_all()
            
        elif opcao == "2":
            logger.section("TESTANDO CLAUDE API")
            if ai.test_connection():
                logger.success("✅ Claude API funcionando!")
            else:
                logger.failed("❌ Problema na Claude API")
                
        elif opcao == "3":
            logger.section("TESTANDO TELEGRAM BOT")
            if asyncio.run(telegram.test_connection()):
                logger.success("✅ Telegram Bot funcionando!")
            else:
                logger.failed("❌ Problema no Telegram Bot")
                
        elif opcao == "4":
            test_resumo_diario()
            
        elif opcao == "5":
            test_noticia_relevante()
            
        elif opcao == "6":
            scheduler.setup_schedule()
            scheduler.get_status()
            
        elif opcao == "7":
            from utils.database import db
            stats = db.get_stats()
            logger.section("ESTATÍSTICAS DO BANCO DE DADOS")
            print(f"\n📊 Total de posts: {stats['total_posts']}")
            print(f"📝 Resumos diários: {stats['resumos']}")
            print(f"📰 Notícias relevantes: {stats['noticias']}")
            if stats['first_post']:
                print(f"🗓️  Primeiro post: {stats['first_post']}")
            if stats['last_post']:
                print(f"🗓️  Último post: {stats['last_post']}")
            print()
            
        elif opcao == "8":
            logger.info("Executando resumo diário imediatamente...")
            scheduler.run_now('resumo')
            
        elif opcao == "9":
            logger.info("Executando notícia relevante imediatamente...")
            scheduler.run_now('noticia')
            
        elif opcao == "0":
            logger.info("👋 Saindo...")
            break
            
        else:
            logger.warning("⚠️  Opção inválida!")
        
        input("\nPressione ENTER para continuar...")


if __name__ == "__main__":
    try:
        menu()
    except KeyboardInterrupt:
        print("\n\n👋 Teste interrompido pelo usuário\n")
    except Exception as e:
        logger.critical(f"❌ Erro: {str(e)}")
        sys.exit(1)