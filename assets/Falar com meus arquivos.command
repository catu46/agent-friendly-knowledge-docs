#!/bin/bash
# ─────────────────────────────────────────────────────────────
# Falar com meus arquivos
# Duplo-clique para conversar com a IA sobre os arquivos desta
# pasta. Não precisa saber nada de código.
# (Gerado pela skill agent-friendly-knowledge-docs.)
# ─────────────────────────────────────────────────────────────

# Entra na pasta onde este arquivo está (a "pasta mãe").
cd "$(dirname "$0")" || exit 1

# Limpa a tela para não assustar com texto técnico.
clear

# Cores calmas (azul suave + cinza), com fallback se o terminal não suportar.
if [ -t 1 ]; then
  B=$'\033[1m'; DIM=$'\033[2m'; BLUE=$'\033[38;5;68m'; R=$'\033[0m'
else
  B=""; DIM=""; BLUE=""; R=""
fi

printf '\n'
printf '   %s%sOi! 👋%s\n' "$B" "$BLUE" "$R"
printf '\n'
printf '   Eu sou a IA que conhece os arquivos desta pasta.\n'
printf '   Pode me perguntar qualquer coisa sobre eles.\n'
printf '\n'
printf '   %sPor exemplo:%s\n' "$DIM" "$R"
printf '   %s· "o que tem nesta pasta?"%s\n' "$DIM" "$R"
printf '   %s· "resume a proposta do cliente X"%s\n' "$DIM" "$R"
printf '   %s· "qual a versão mais recente do modelo?"%s\n' "$DIM" "$R"
printf '\n'
printf '   %sÉ só escrever aqui embaixo e apertar Enter.%s\n' "$B" "$R"
printf '   %s(Para sair quando terminar, escreva /exit e Enter.)%s\n' "$DIM" "$R"
printf '\n'
printf '   %s────────────────────────────────────────────%s\n' "$DIM" "$R"
printf '\n'

# Se o Claude Code ainda não estiver instalado, explica com calma
# em vez de mostrar um erro técnico assustador.
if ! command -v claude >/dev/null 2>&1; then
  printf '   %sQuase lá!%s Só falta instalar o assistente uma vez.\n' "$B" "$R"
  printf '   Peça ajuda para instalar o "Claude Code":\n'
  printf '   %shttps://claude.com/claude-code%s\n\n' "$BLUE" "$R"
  printf '   Depois de instalado, é só dar duplo-clique aqui de novo.\n\n'
  printf '   %s(Pode fechar esta janela.)%s\n\n' "$DIM" "$R"
  exit 0
fi

# Abre o chat da IA já dentro desta pasta.
claude

# Despedida gentil quando a conversa termina.
printf '\n   %sPronto! Pode fechar esta janela. Até a próxima 👋%s\n\n' "$BLUE" "$R"
