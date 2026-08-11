#!/bin/bash
# ==============================================================================
# Dateiname: restart-mail-services.sh
# Version: 1.0.0
# ==============================================================================

SERVICES=("fetchmail.service" "mail-watcher.service")

echo "=== Mail-Bot Dienste neu starten ==="

# Systemd User-Konfiguration neu laden
systemctl --user daemon-reload

for service in "${SERVICES[@]}"; do
    echo -n "Starte $service neu... "
    if systemctl --user restart "$service"; then
        echo "[OK]"
    else
        echo "[FEHLER]"
    fi
done

echo ""
echo "=== Status-Übersicht ==="
systemctl --user status "${SERVICES[@]}" --no-pager

#EOF
