#!/bin/bash

# Script de instalação automática - GameFi RADAR BR Bot
# Para Linux e Mac

echo "=========================================="
echo "🎮 GameFi RADAR BR Bot - Instalação 🚀"
echo "=========================================="
echo ""

# Cores para output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para verificar comando
check_command() {
    if command -v $1 &> /dev/null; then
        echo -e "${GREEN}✅ $1 instalado${NC}"
        return 0
    else
        echo -e "${RED}❌ $1 não encontrado${NC}"
        return 1
    fi
}

# 1. Verificar Python
echo "📦 Verificando Python..."
if check_command python3; then
    PYTHON_VERSION=$(python3 --version)
    echo "   Versão: $PYTHON_VERSION"
else
    echo -e "${RED}❌ Python 3 não encontrado!${NC}"
    echo "   Instale Python 3.8+ em: https://www.python.org/"
    exit 1
fi

# 2. Verificar pip
echo ""
echo "📦 Verificando pip..."
if check_command pip3; then
    PIP_VERSION=$(pip3 --version)
    echo "   Versão: $PIP_VERSION"
else
    echo -e "${RED}❌ pip não encontrado!${NC}"
    echo "   Instalando pip..."
    python3 -m ensurepip --upgrade
fi

# 3. Criar ambiente virtual
echo ""
echo "🔧 Criando ambiente virtual..."
if [ -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Ambiente virtual já existe${NC}"
    read -p "   Deseja recriar? (s/N): " recreate
    if [ "$recreate" = "s" ] || [ "$recreate" = "S" ]; then
        rm -rf venv
        python3 -m venv venv
        echo -e "${GREEN}✅ Ambiente virtual recriado${NC}"
    fi
else
    python3 -m venv venv
    echo -e "${GREEN}✅ Ambiente virtual criado${NC}"
fi

# 4. Ativar ambiente virtual
echo ""
echo "🔄 Ativando ambiente virtual..."
source venv/bin/activate

# 5. Atualizar pip
echo ""
echo "⬆️  Atualizando pip..."
pip install --upgrade pip

# 6. Instalar dependências
echo ""
echo "📥 Instalando dependências..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Dependências instaladas com sucesso${NC}"
    else
        echo -e "${RED}❌ Erro ao instalar dependências${NC}"
        exit 1
    fi
else
    echo -e "${RED}❌ Arquivo requirements.txt não encontrado${NC}"
    exit 1
fi

# 7. Criar diretórios necessários
echo ""
echo "📁 Criando estrutura de diretórios..."
mkdir -p data logs config src utils
echo -e "${GREEN}✅ Diretórios criados${NC}"

# 8. Verificar .env
echo ""
echo "⚙️  Verificando arquivo .env..."
if [ -f ".env" ]; then
    echo -e "${GREEN}✅ Arquivo .env encontrado${NC}"
else
    echo -e "${YELLOW}⚠️  Arquivo .env não encontrado${NC}"
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo -e "${GREEN}✅ Arquivo .env criado a partir do template${NC}"
        echo -e "${YELLOW}⚠️  IMPORTANTE: Edite o .env com suas credenciais!${NC}"
    fi
fi

# 9. Criar arquivos __init__.py
echo ""
echo "📝 Criando arquivos de módulo..."
touch config/__init__.py
touch src/__init__.py
touch utils/__init__.py
echo -e "${GREEN}✅ Arquivos de módulo criados${NC}"

# 10. Resumo final
echo ""
echo "=========================================="
echo "✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!"
echo "=========================================="
echo ""
echo "📋 Próximos passos:"
echo ""
echo "1. Edite o arquivo .env com suas credenciais:"
echo "   nano .env"
echo ""
echo "2. Execute o assistente de configuração:"
echo "   python3 setup_helper.py"
echo ""
echo "3. Teste o bot:"
echo "   python3 test_bot.py"
echo ""
echo "4. Execute o bot:"
echo "   python3 main.py"
echo ""
echo "💡 Dica: Ative o ambiente virtual sempre que usar:"
echo "   source venv/bin/activate"
echo ""
echo "📚 Documentação completa: README.md"
echo ""
echo "🎮 Boas postagens! 🚀"
echo ""