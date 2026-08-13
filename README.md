![Python](https://img.shields.io/badge/language-python-blue)
![Bash](https://img.shields.io/badge/language-bash-green)
![Ollama](https://img.shields.io/badge/Ollama-Granite_4.1--8b-orange)
![Version](https://img.shields.io/badge/version-1.0.3-blue)
![License](https://img.shields.io/badge/license-MIT-brightgreen)

# Nexus-Courier-AI 🤖✉️

## [DE]
`nexus-courier-ai` ist ein lokaler, ereignisgesteuerter E-Mail-Assistent für Linux-Systeme. Er überwacht eine lokale MBOX-Mailbox (z. B. befüllt durch `fetchmail`), generiert mithilfe lokaler LLMs (**getestet mit IBM Granite 4.1 / `granite4.1:8b`** über **Ollama**) automatische Antworten und versendet diese zuverlässig über die Transportschicht **`nexus-courier.sh`**.

100 % lokal, datenschutzfreundlich und modular aufgebaut nach der UNIX-Philosophie.

### Funktionen
- **Ereignisgesteuert:** `watch-mail.sh` lauscht per `inotifywait` auf MBOX-Änderungen und ignoriert leere Mailboxen (<= 14 Bytes).
- **MBOX-Parsing:** `mail-bot.py` verarbeitet multiple Nachrichten aus MBOX-Dateien, dekodiert MIME-Header und bereinigt Signaturen.
- **Lokale KI:** Nutzt die Ollama-Chat-API (`/api/chat`) mit striktem System-Prompt für kurze, präzise E-Mail-Antworten.
- **Transportschicht-Abstraktion:** Übergibt Antworten mit erzwungenem `Re:`-Betreff an `nexus-courier.sh`.
- **Automatischer Cleanup:** Leert die MBOX-Datei sicher nach erfolgreicher Verarbeitung aller Nachrichten.
- **Systemd-Integration:** Enthält Skripte zur Steuerung von User-Services (`fetchmail.service`, `mail-watcher.service`).

### Architektur & Ablauf
```
┌──────────────────┐      ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────────┐
│ Local MBOX File  │ ───> │  watch-mail.sh  │ ───> │   mail-bot.py   │ ───> │  nexus-courier.sh   │
│ (/var/mail/user) │      │  (inotifywait)  │      │  (Python venv)  │      │  (msmtp Transport)  │
└──────────────────┘      └─────────────────┘      └─────────────────┘      └─────────────────────┘
```

### Installation & Einrichtung
1. Installiere die System-Abhängigkeiten:
   ```bash
   sudo apt update
   sudo apt install fetchmail inotify-tools python3-pip python3-venv
   ```
2. Erstelle eine virtuelle Python-Umgebung (`venv`) und installiere die Abhängigkeiten:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Lade das Ollama-Modell:
   ```bash
   ollama pull granite4.1:8b
   ```
4. Passe die Pfade in `mail-bot.py` und `watch-mail.sh` an (`OLLAMA_HOST`, `MAILBOX_PATH`, `COURIER_PATH` sowie den Pfad zum `venv/bin/python3`).
5. Stelle sicher, dass [nexus-courier](https://github.com/o-valo/nexus-courier) einsatzbereit ist.

### Benutzung
Prozess manuell starten:
```bash
./watch-mail.sh
```

Dienste (z. B. `systemd` User-Services) neu starten:
```bash
./restart-mail-services.sh
```

---

![Python](https://img.shields.io/badge/language-python-blue)
![Bash](https://img.shields.io/badge/language-bash-green)
![Ollama](https://img.shields.io/badge/Ollama-Granite_4.1--8b-orange)
![Version](https://img.shields.io/badge/version-1.0.3-blue)
![License](https://img.shields.io/badge/license-MIT-brightgreen)

## [ENG]
`nexus-courier-ai` is a local, event-driven email assistant for Linux systems. It monitors a local MBOX file (e.g. populated via `fetchmail`), generates automated responses using local LLMs (**tested with IBM Granite 4.1 / `granite4.1:8b`** via **Ollama**), and dispatches them reliably through the **`nexus-courier.sh`** transport layer.

100% local, privacy-friendly, and built modularly following the UNIX philosophy.

### Features
- **Event-Driven:** `watch-mail.sh` monitors MBOX modifications via `inotifywait`, ignoring empty file changes (<= 14 bytes).
- **MBOX Parsing:** `mail-bot.py` parses multiple messages, decodes MIME headers, and strips incoming signatures.
- **Local AI Integration:** Uses the Ollama Chat API (`/api/chat`) with strict system prompts for short, concise replies.
- **Transport Abstraction:** Passes generated responses with forced `Re:` prefix to `nexus-courier.sh`.
- **Automatic Cleanup:** Safely truncates the MBOX file after successful processing.
- **Systemd Integration:** Includes management scripts for user-level services (`fetchmail.service`, `mail-watcher.service`).

### Architecture

### Architecture
```
┌──────────────────┐      ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────────┐
│ Local MBOX File  │ ───> │  watch-mail.sh  │ ───> │   mail-bot.py   │ ───> │  nexus-courier.sh   │
│ (/var/mail/user) │      │  (inotifywait)  │      │  (Python venv)  │      │  (msmtp Transport)  │
└──────────────────┘      └─────────────────┘      └─────────────────┘      └─────────────────────┘
```

### Installation & Setup
1. Install system dependencies:
   ```bash
   sudo apt update
   sudo apt install fetchmail inotify-tools python3-pip python3-venv
   ```
2. Create a virtual Python environment (`venv`) and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Pull the required Ollama model:
   ```bash
   ollama pull granite4.1:8b
   ```
4. Adjust paths in `mail-bot.py` and `watch-mail.sh` (`OLLAMA_HOST`, `MAILBOX_PATH`, `COURIER_PATH`, and the path to `venv/bin/python3`).
5. Ensure [nexus-courier](https://github.com/o-valo/nexus-courier) is properly configured.

### Usage
Start watching manually:
```bash
./watch-mail.sh
```

Restart background services (`systemd` user units):
```bash
./restart-mail-services.sh
```

---

#### Powered with AI

<!-- #EOF -->



