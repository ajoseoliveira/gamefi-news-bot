#!/usr/bin/env python3
"""
Script auxiliar para configurar o GameFi RADAR BR Bot
Ajuda a configurar e validar todas as credenciais necessárias
"""

import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config.config import validate_config
from utils.logger import logger


def print_banner():
    """Exibe banner de boas-vindas"""
    print("\n" + "="*60)
    print("🛠️  GameFi RADAR BR Bot - Assistente de Configuração")
    print("="*60 + "\n")


def check_env_file():
    """Verifica se arquivo .env existe"""
    env_file = Path(".env")
    
    if not env_file.exists():
        logger.warning("Arquivo .env não encontrado!")
        print("\n📋 Criando arquivo .env a partir do template...")
        
        env_example = Path(".env.example")
        if env_example.exists():
            import shutil
            shutil.copy(env_example, env_file)
            logger.success("Arquivo .env criado!")
        else:
            logger.error("Arquivo .env.example não encontrado!")
            return False
    
    logger.success("Arquivo .env encontrado!")
    return True


def validate_claude_api():
    """Valida Claude API"""
    logger.section("VALIDANDO CLAUDE API")
    
    try:
        from src.ai_processor import ai
        
        if ai.test_connection():
            logger.success("✅ Claude API configurada corretamente!")
            return True
        else:
            logger.failed("❌ Problema na Claude API")
            print("\n💡 Possíveis soluções:")
            print("   1. Verifique se o CLAUDE_API_KEY está correto no .env")
            print("   2. Acesse: https://console.anthropic.com/")
            print("   3. Gere uma nova API Key se necessário")
            return False
            
    except Exception as e:
        logger.failed(f"❌ Erro: {str(e)}")
        return False


def validate_telegram_bot():
    """Valida Telegram Bot"""
    logger.section("VALIDANDO TELEGRAM BOT")
    
    try:
        from src.telegram_bot import telegram
        
        if asyncio.run(telegram.test_connection()):
            logger.success("✅ Telegram Bot configurado corretamente!")
            return True
        else:
            logger.failed("❌ Problema no Telegram Bot")
            print("\n💡 Possíveis soluções:")
            print("   1. Verifique se o TELEGRAM_BOT_TOKEN está correto no .env")
            print("   2. Crie um bot em: @BotFather no Telegram")
            print("   3. Adicione o bot como administrador do canal")
            print("   4. Verifique se o TELEGRAM_CHANNEL_ID está correto")
            return False
            
    except Exception as e:
        logger.failed(f"❌ Erro: {str(e)}")
        return False


def get_channel_id_instructions():
    """Mostra instruções para obter Channel ID"""
    logger.section("COMO OBTER O ID DO CANAL")
    
    print("""
📱 MÉTODO 1 - Usando @userinfobot (Mais Fácil):

1. No Telegram, procure por: @userinfobot
2. Adicione o bot ao seu canal como administrador
3. Encaminhe qualquer mensagem do canal para o @userinfobot
4. Ele te enviará o ID do canal (ex: -1001234567890)
5. Copie esse ID e cole no .env em TELEGRAM_CHANNEL_ID


📱 MÉTODO 2 - Usando API diretamente:

1. Adicione seu bot como administrador do canal
2. Envie qualquer mensagem no canal
3. Acesse no navegador:
   https://api.telegram.org/bot<SEU_TOKEN>/getUpdates
   
4. Procure por "chat":{"id":-100XXXXXXXXX}
5. Use esse ID no .env


📱 MÉTODO 3 - Usando username (Mais Simples):

Se seu canal tem username público (@gamefiradarbr):
   TELEGRAM_CHANNEL_ID=@gamefiradarbr
   
Isso já funciona! ✅

""")
    input("Pressione ENTER para continuar...")


def check_dependencies():
    """Verifica se todas as dependências estão instaladas"""
    logger.section("VERIFICANDO DEPENDÊNCIAS")
    
    required_packages = [
        'anthropic',
        'telegram',
        'schedule',
        'requests',
        'python-dotenv',
        'python-dateutil',
        'pytz',
        'colorlog',
        'pydantic'
    ]
    
    missing = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            logger.info(f"✅ {package}")
        except ImportError:
            logger.warning(f"❌ {package} - NÃO INSTALADO")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Pacotes faltando: {len(missing)}")
        print("\n💡 Instale com:")
        print("   pip install -r requirements.txt")
        return False
    
    logger.success("\n✅ Todas as dependências instaladas!")
    return True


def setup_wizard():
    """Assistente de configuração completo"""
    
    print_banner()
    
    steps = [
        ("1. Verificando dependências", check_dependencies),
        ("2. Verificando arquivo .env", check_env_file),
        ("3. Validando Claude API", validate_claude_api),
        ("4. Validando Telegram Bot", validate_telegram_bot),
    ]
    
    results = []
    
    for step_name, step_func in steps:
        logger.info(f"\n🔄 {step_name}...")
        result = step_func()
        results.append(result)
        
        if not result:
            print(f"\n⚠️  {step_name} falhou!")
            resposta = input("\nDeseja continuar mesmo assim? (s/N): ").lower()
            if resposta != 's':
                logger.warning("Configuração interrompida")
                return False
    
    # Resumo final
    logger.section("RESUMO DA CONFIGURAÇÃO")
    
    all_ok = all(results)
    
    if all_ok:
        print("""
✅ ✅ ✅ TUDO CONFIGURADO CORRETAMENTE! ✅ ✅ ✅

🎉 Seu bot está pronto para usar!

📝 Próximos passos:

1. Para testar o bot:
   python test_bot.py

2. Para rodar em modo produção:
   - Edite o .env e mude: MODE=production
   - Execute: python main.py

3. O bot vai postar automaticamente nos horários:
   • 09:00 - Resumo Diário
   • 13:00 - Notícia Relevante
   • 18:00 - Notícia Relevante

💡 Dicas:
   - Use MODE=test para testar sem postar no canal
   - Verifique os logs em: logs/bot.log
   - Execute test_bot.py sempre que fizer mudanças

""")
    else:
        print("""
⚠️  EXISTEM PROBLEMAS NA CONFIGURAÇÃO

Revise os erros acima e corrija antes de prosseguir.

💡 Ajuda:
   - Claude API: https://console.anthropic.com/
   - Telegram Bot: @BotFather no Telegram
   - Documentação: README.md

""")
    
    return all_ok


def main():
    """Função principal"""
    
    try:
        success = setup_wizard()
        
        if success:
            logger.success("\n✅ Configuração concluída com sucesso!\n")
            sys.exit(0)
        else:
            logger.warning("\n⚠️  Configuração incompleta\n")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n👋 Configuração interrompida pelo usuário\n")
        sys.exit(1)
        
    except Exception as e:
        logger.critical(f"\n❌ Erro fatal: {str(e)}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()