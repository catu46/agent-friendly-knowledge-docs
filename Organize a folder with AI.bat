@echo off
REM ---------------------------------------------------------------
REM  Organize a folder with AI
REM  Double-click, pick a folder, pick an assistant, watch the AI
REM  set that folder up to be navigable and self-updating.
REM  Carries its own skill, so it installs itself on first run.
REM  (agent-friendly-knowledge-docs)
REM ---------------------------------------------------------------
chcp 65001 >nul 2>nul
set "SKILL_DIR=%~dp0"
if "%SKILL_DIR:~-1%"=="\" set "SKILL_DIR=%SKILL_DIR:~0,-1%"
set "SKILL_NAME=agent-friendly-knowledge-docs"
cls

echo(
echo    Let's organize a folder with AI
echo(
echo    Pick a folder, pick an assistant, and watch the AI set it up.
echo(
echo    ----------------------------------------------
echo(

REM 1) Install the skill for both assistants (directory junction, no admin needed).
for %%B in ("%USERPROFILE%\.claude\skills" "%USERPROFILE%\.agents\skills") do (
  if not exist "%%~B" mkdir "%%~B"
  if not exist "%%~B\%SKILL_NAME%" mklink /J "%%~B\%SKILL_NAME%" "%SKILL_DIR%" >nul 2>nul
)

REM 2) Native folder picker.
echo    Opening a window to choose the folder...
for /f "usebackq delims=" %%I in (`powershell -NoProfile -Command "Add-Type -AssemblyName System.Windows.Forms | Out-Null; $f=New-Object System.Windows.Forms.FolderBrowserDialog; $f.Description='Which folder should the AI organize?'; if($f.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK){Write-Output $f.SelectedPath}"`) do set "TARGET=%%I"
if not defined TARGET (
  echo    No folder chosen. You can close this window.
  echo(
  pause
  exit /b 0
)
echo    Folder: %TARGET%
echo(

REM 3) Which assistant?
set HAVE_CLAUDE=0
where claude >nul 2>nul && set HAVE_CLAUDE=1
set HAVE_CODEX=0
where codex >nul 2>nul && set HAVE_CODEX=1
set "S1=not installed"
if "%HAVE_CLAUDE%"=="1" set "S1=installed"
set "S2=not installed"
if "%HAVE_CODEX%"=="1" set "S2=installed"
echo    Which assistant should apply it?
echo(
echo    [1] Claude Code   %S1%
echo    [2] Codex         %S2%
echo(
choice /c 12 /n /m "   Type 1 or 2: "
if errorlevel 2 ( set "SEL=codex" & set "SELOK=%HAVE_CODEX%" ) else ( set "SEL=claude" & set "SELOK=%HAVE_CLAUDE%" )

if not "%SELOK%"=="1" (
  echo(
  echo    That assistant isn't installed yet. Install it once, then run this again.
  if "%SEL%"=="codex" ( start "" "https://learn.chatgpt.com/docs/codex/cli" ) else ( start "" "https://claude.com/claude-code" )
  echo(
  pause
  exit /b 0
)

REM 4) Apply the skill inside the chosen folder.
cd /d "%TARGET%"
set "PROMPT=Use the %SKILL_NAME% skill to organize this folder (the current directory) so an AI can navigate it and keep it updated. Interview me in my language, then set it up."
echo(
echo    Applying the skill in your folder now -- watch below.
echo(
if "%SEL%"=="codex" ( codex "%PROMPT%" ) else ( claude "%PROMPT%" )
echo(
echo    Done! You can close this window.
echo(
