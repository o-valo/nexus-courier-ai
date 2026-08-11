![Python](https://img.shields.io/badge/language-python-blue)
![Bash](https://img.shields.io/badge/language-bash-green)
![Ollama](https://img.shields.io/badge/Ollama-Granite_4.1--8b-orange)
![Version](https://img.shields.io/badge/version-1.0.3-blue)
![License](https://img.shields.io/badge/license-MIT-brightgreen)

# Nexus-Courier-AI 🤖✉️

## [DE]
`nexus-courier-ai` ist ein lokaler E-Mail-Assistent für Linux. Das System überwacht eine MBOX-Datei (`/var/mail/...`), verarbeitet eingehende Mails über eine lokale Ollama-Instanz und versendet die generierten Antworten per `nexus-courier.sh`.

### Architektur & Ablauf
```
┌──────────────────┐      ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────────┐
│ Local MBOX File  │ ───> │  watch-mail.sh  │ ───> │   mail-bot.py   │ ───> │  nexus-courier.sh   │
│ (/var/mail/user) │      │  (inotifywait)  │      │  (Python venv)  │      │  (msmtp Transport)  │
└──────────────────┘      └─────────────────┘      └─────────────────┘      └─────────────────────┘
```

### Funktionsweise
* `watch-mail.sh` überwacht die MBOX-Datei via `inotifywait` auf Änderungen (Dateigröße > 14 Bytes).
* `mail-bot.py` liest die MBOX aus, dekodiert Header, entfernt vorhandene Signaturen und sendet den Inhalt an die Chat-API von Ollama.
* Die generierte Antwort wird direkt an `nexus-courier.sh` zum Versand übergeben.
* Nach erfolgreicher Verarbeitung aller Mails wird die MBOX-Datei geleert.

### Voraussetzungen
* Linux (Debian/Ubuntu/Raspberry Pi OS)
* `fetchmail`, `inotify-tools`, `python3-pip`, `python3-venv`
* [Ollama](https://ollama.com/) (Getestet mit Modell `granite4.1:8b`)
* Eingereichtes [nexus-courier](https://github.com/o-valo/nexus-courier) Skript

### Installation
1. Paketabhängigkeiten installieren:
   ```bash
   sudo apt update
   sudo apt install fetchmail inotify-tools python3-pip python3-venv
   ```
2. Virtuelle Python-Umgebung einrichten:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Modell laden:
   ```bash
   ollama pull granite4.1:8b
   ```
4. Pfade in `mail-bot.py` und `watch-mail.sh` anpassen (`OLLAMA_HOST`, `MAILBOX_PATH`, `COURIER_PATH`, Python-Binary).

### Nutzung
Skript manuell im Hintergrund starten:
```bash
./watch-mail.sh
```

Systemd User-Services neu laden/starten:
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
`nexus-courier-ai` is a local email assistant for Linux systems. It monitors a local MBOX file (`/var/mail/...`), processes incoming messages via a local Ollama instance, and dispatches responses using `nexus-courier.sh`.

### Architecture
```
┌──────────────────┐      ┌─────────────────┐      ┌─────────────────┐      ┌─────────────────────┐
│ Local MBOX File  │ ───> │  watch-mail.sh  │ ───> │   mail-bot.py   │ ───> │  nexus-courier.sh   │
│ (/var/mail/user) │      │  (inotifywait)  │      │  (Python venv)  │      │  (msmtp Transport)  │
└──────────────────┘      └─────────────────┘      └─────────────────┘      └─────────────────────┘
```

### How it works
* `watch-mail.sh` monitors the MBOX file using `inotifywait` (triggers on file size > 14 bytes).
* `mail-bot.py` parses the MBOX file, decodes headers, strips incoming signatures, and queries the Ollama Chat API.
* Generated answers are forwarded directly to `nexus-courier.sh` for dispatch.
* The MBOX file is truncated after processing all messages.

### Requirements
* Linux
* `fetchmail`, `inotify-tools`, `python3-pip`, `python3-venv`
* [Ollama](https://ollama.com/) (Tested with `granite4.1:8b`)
* Active [nexus-courier](https://github.com/o-valo/nexus-courier) transport script

### Setup
1. Install system dependencies:
   ```bash
   sudo apt update
   sudo apt install fetchmail inotify-tools python3-pip python3-venv
   ```
2. Setup Python environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
3. Pull the LLM model:
   ```bash
   ollama pull granite4.1:8b
   ```
4. Configure local paths in `mail-bot.py` and `watch-mail.sh`.

### Usage
Run manually:
```bash
./watch-mail.sh
```

Restart systemd user services:
```bash
./restart-mail-services.sh
```





#### Powered with AI

<!-- #EOF -->
