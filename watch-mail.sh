#!/bin/bash
# ==============================================================================
# Dateiname: watch-mail.sh
# Version: 1.0.1
# ==============================================================================

MAILBOX="/var/mail/username"
PYTHON_BIN="$HOME/nexus-courier-ai/venv/bin/python3"
BOT_SCRIPT="$HOME/nexus-courier-ai/mail-bot.py"

logger -t mail-watcher "[WATCHER] Gestartet. Überwache $MAILBOX..."

while true; do
    inotifywait -q -e modify,close_write "$MAILBOX"
    
    if [ -f "$MAILBOX" ]; then
        FILESIZE=$(stat -c%s "$MAILBOX" 2>/dev/null || echo 0)
        
        if [ "$FILESIZE" -gt 14 ]; then
            logger -t mail-watcher "[WATCHER] Datei geändert ($FILESIZE Bytes > 14 Bytes). Starte Mail-Bot..."
            $PYTHON_BIN $BOT_SCRIPT 2>&1 | logger -t mail-bot
        else
            logger -t mail-watcher "[WATCHER] Datei geändert, aber nur $FILESIZE Bytes (<= 14 Bytes). Ignoriere."
        fi
    fi
done

#EOF
