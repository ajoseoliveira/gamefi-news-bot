# GitHub Actions Workflows

Este projeto utiliza GitHub Actions para automatizar o agendamento de ligar e desligar a máquina no Fly.io, economizando custos.

## Workflows Implementados

### 1. Start Machine (`start-machine.yml`)
- **Horário:** 8:30 AM (Brasília)
- **Cron:** `30 11 * * *` (UTC)
- **Função:** Liga a máquina do gamefi-news-bot automaticamente

### 2. Stop Machine (`stop-machine.yml`)
- **Horário:** 18:30 PM (Brasília)
- **Cron:** `30 21 * * *` (UTC)
- **Função:** Desliga a máquina do gamefi-news-bot automaticamente

## Configuração Necessária

### 1. Criar Token Fly.io
1. Acesse: https://fly.io/user/personal_access_tokens
2. Crie um novo token pessoal
3. Copie o token

### 2. Adicionar Secret no GitHub
1. Vá até: https://github.com/ajoseoliveira/gamefi-news-bot/settings/secrets/actions
2. Clique em "New repository secret"
3. Nome: `FLY_API_TOKEN`
4. Valor: Cole o token do Fly.io
5. Clique em "Add secret"

## IDs Importantes

- **App ID:** gamefi-news-bot
- **Machine ID:** d891dddce02318

## Nota sobre Horários

Os horários de cron estão configurados em UTC:
- **8:30 AM Brasília** = 11:30 UTC (horário de verão)
- **18:30 PM Brasília** = 21:30 UTC (horário de verão)

Se o Brasil estiver em horário padrão (UTC-2), ajuste para:
- **8:30 AM Brasília** = 10:30 UTC
- **18:30 PM Brasília** = 20:30 UTC

Você pode testar executando manualmente via GitHub Actions (workflow_dispatch).

## Teste Manual

1. Acesse: https://github.com/ajoseoliveira/gamefi-news-bot/actions
2. Selecione o workflow desejado
3. Clique em "Run workflow"
4. Verifique se a máquina ligou/desligou no Fly.io
