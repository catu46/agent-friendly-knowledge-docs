@echo off
REM ---------------------------------------------------------------
REM  Falar com meus arquivos
REM  Duplo-clique para conversar com a IA sobre os arquivos desta
REM  pasta. Nao precisa saber nada de codigo.
REM  (Gerado pela skill agent-friendly-knowledge-docs.)
REM ---------------------------------------------------------------

REM Usa UTF-8 para acentos e emoji (melhor esforco em consoles antigos).
chcp 65001 >nul 2>nul

REM Entra na pasta onde este arquivo esta (a "pasta mae").
cd /d "%~dp0"

REM Limpa a tela para nao assustar com texto tecnico.
cls

echo(
echo    Oi! 👋
echo(
echo    Eu sou a IA que conhece os arquivos desta pasta.
echo    Pode me perguntar qualquer coisa sobre eles.
echo(
echo    Por exemplo:
echo    - "o que tem nesta pasta?"
echo    - "resume a proposta do cliente X"
echo    - "qual a versao mais recente do modelo?"
echo(
echo    E so escrever aqui embaixo e apertar Enter.
echo    (Para sair quando terminar, escreva /exit e Enter.)
echo(
echo    --------------------------------------------------
echo(

REM Abre o chat da IA ja dentro desta pasta.
REM 1) Se o Claude Code estiver instalado direto no Windows, usa ele.
where claude >nul 2>nul
if %errorlevel%==0 (
  claude
  goto despedida
)

REM 2) Se estiver via WSL (Linux dentro do Windows), tenta por la.
where wsl >nul 2>nul
if %errorlevel%==0 (
  wsl claude
  goto despedida
)

REM 3) Nao achou de jeito nenhum: recado gentil, sem erro tecnico.
echo    Quase la! So falta instalar o assistente uma vez.
echo    Peca ajuda para instalar o "Claude Code":
echo    https://claude.com/claude-code
echo(
echo    Depois de instalado, e so dar duplo-clique aqui de novo.
echo(
pause
exit /b 0

:despedida
echo(
echo    Pronto! Pode fechar esta janela. Ate a proxima 👋
echo(
