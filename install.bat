@echo off
REM Script de instalação automática - GameFi RADAR BR Bot
REM Para Windows

echo ==========================================
echo 🎮 GameFi RADAR BR Bot - Instalacao 🚀
echo ==========================================
echo.

REM 1. Verificar Python
echo 📦 Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python nao encontrado!
    echo    Instale Python 3.8+ em: https://www.python.org/
    echo    ⚠️ Marque "Add Python to PATH" durante instalacao
    pause
    exit /b 1
)

python --version
echo ✅ Python instalado
echo.

REM 2. Verificar pip
echo 📦 Verificando pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip nao encontrado!
    echo    Instalando pip...
    python -m ensurepip --upgrade
)
pip --version
echo ✅ pip instalado
echo.

REM 3. Criar ambiente virtual
echo 🔧 Criando ambiente virtual...
if exist "venv\" (
    echo ⚠️ Ambiente virtual ja existe
    set /p recreate="   Deseja recriar? (s/N): "
    if /i "%recreate%"=="s" (
        rmdir /s /q venv
        python -m venv venv
        echo ✅ Ambiente virtual recriado
    )
) else (
    python -m venv venv
    echo ✅ Ambiente virtual criado
)
echo.

REM 4. Ativar ambiente virtual
echo 🔄 Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM 5. Atualizar pip
echo.
echo ⬆️ Atualizando pip...
python -m pip install --upgrade pip

REM 6. Instalar dependências
echo.
echo 📥 Instalando dependencias...
if exist "requirements.txt" (
    pip install -r requirements.txt
    if %errorlevel% equ 0 (
        echo ✅ Dependencias instaladas com sucesso
    ) else (
        echo ❌ Erro ao instalar dependencias
        pause
        exit /b 1
    )
) else (
    echo ❌ Arquivo requirements.txt nao encontrado
    pause
    exit /b 1
)

REM 7. Criar diretórios necessários
echo.
echo 📁 Criando estrutura de diretorios...
if not exist "data" mkdir data
if not exist "logs" mkdir logs
if not exist "config" mkdir config
if not exist "src" mkdir src
if not exist "utils" mkdir utils
echo ✅ Diretorios criados

REM 8. Verificar .env
echo.
echo ⚙️ Verificando arquivo .env...
if exist ".env" (
    echo ✅ Arquivo .env encontrado
) else (
    echo ⚠️ Arquivo .env nao encontrado
    if exist ".env.example" (
        copy .env.example .env
        echo ✅ Arquivo .env criado a partir do template
        echo ⚠️ IMPORTANTE: Edite o .env com suas credenciais!
    )
)

REM 9. Criar arquivos __init__.py
echo.
echo 📝 Criando arquivos de modulo...
type nul > config\__init__.py
type nul > src\__init__.py
type nul > utils\__init__.py
echo ✅ Arquivos de modulo criados

REM 10. Resumo final
echo.
echo ==========================================
echo ✅ INSTALACAO CONCLUIDA COM SUCESSO!
echo ==========================================
echo.
echo 📋 Proximos passos:
echo.
echo 1. Edite o arquivo .env com suas credenciais
echo    notepad .env
echo.
echo 2. Execute o assistente de configuracao:
echo    python setup_helper.py
echo.
echo 3. Teste o bot:
echo    python test_bot.py
echo.
echo 4. Execute o bot:
echo    python main.py
echo.
echo 💡 Dica: Ative o ambiente virtual sempre que usar:
echo    venv\Scripts\activate
echo.
echo 📚 Documentacao completa: README.md
echo.
echo 🎮 Boas postagens! 🚀
echo.
pause