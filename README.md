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
* `watch-mail.sh` überwacht die MBOX-Datei via `inotifywait` auf Änderungen (Ignoriert Dateigrößen <= 14 Bytes, um Fehlstarts bei symbolischen Links / Symlink-Pfaden zu vermeiden).
* `mail-bot.py` liest die MBOX aus, dekodiert Header, entfernt vorhandene Signaturen und sendet den Inhalt an die Chat-API von Ollama.
* Die generierte Antwort wird direkt an `nexus-courier.sh` zum Versand übergeben.
* Nach erfolgreicher Verarbeitung aller Mails wird die MBOX-Datei geleert.

### Voraussetzungen
* Linux (Debian/Ubuntu/Raspberry Pi OS)
* `fetchmail`, `inotify-tools`, `python3-pip`, `python3-venv`
* [Ollama](https://ollama.com/) (Getestet mit Modell `granite4.1:8b`)
* Eingerichtetes [nexus-courier](https://github.com/o-valo/nexus-courier) Skript

### Installation & Einrichtung

#### 1. Repository klonen
```bash
cd ~/progs
git clone [https://github.com/o-valo/nexus-courier-ai.git](https://github.com/o-valo/nexus-courier-ai.git)
cd nexus-courier-ai
```

#### 2. Paketabhängigkeiten & venv
```bash
sudo apt update
sudo apt install fetchmail inotify-tools python3-pip python3-venv

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 3. Ollama Modell laden
```bash
ollama pull granite4.1:8b
```

#### 4. Konfiguration
Passe die Pfade in `mail-bot.py` und `watch-mail.sh` an (`OLLAMA_HOST`, `MAILBOX_PATH`, `COURIER_PATH`, Python-Binary).

#### 5. Einbindung als Systemd User-Service (Autostart)
Um `watch-mail.sh` automatisch im Hintergrund laufen zu lassen, erstelle eine Service-Datei unter `~/.config/systemd/user/mail-watcher.service`:

```ini
[Unit]
Description=Mail Watcher Service for Nexus Courier AI
After=network.target

[Service]
Type=simple
ExecStart=%h/progs/nexus-courier-ai/watch-mail.sh
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
```

Dienst aktivieren und starten:
```bash
systemctl --user daemon-reload
systemctl --user enable mail-watcher.service
systemctl --user start mail-watcher.service
```

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
* `watch-mail.sh` monitors the MBOX file using `inotifywait` (Ignores file sizes <= 14 bytes to prevent false triggers on symbolic link paths).
* `mail-bot.py` parses the MBOX file, decodes headers, strips incoming signatures, and queries the Ollama Chat API.
* Generated answers are forwarded directly to `nexus-courier.sh` for dispatch.
* The MBOX file is truncated after processing all messages.

### Requirements
* Linux
* `fetchmail`, `inotify-tools`, `python3-pip`, `python3-venv`
* [Ollama](https://ollama.com/) (Tested with `granite4.1:8b`)
* Configured [nexus-courier](https://github.com/o-valo/nexus-courier) transport script

### Setup & Installation

#### 1. Clone repository
```bash
cd ~/progs
git clone [https://github.com/o-valo/nexus-courier-ai.git](https://github.com/o-valo/nexus-courier-ai.git)
cd nexus-courier-ai
```

#### 2. Dependencies & venv
```bash
sudo apt update
sudo apt install fetchmail inotify-tools python3-pip python3-venv

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 3. Pull Ollama Model
```bash
ollama pull granite4.1:8b
```

#### 4. Configuration
Configure local paths in `mail-bot.py` and `watch-mail.sh` (`OLLAMA_HOST`, `MAILBOX_PATH`, `COURIER_PATH`, Python binary).

#### 5. Systemd User Service Setup (Autostart)
To run `watch-mail.sh` automatically in the background, create `~/.config/systemd/user/mail-watcher.service`:

```ini
[Unit]
Description=Mail Watcher Service for Nexus Courier AI
After=network.target

[Service]
Type=simple
ExecStart=%h/progs/nexus-courier-ai/watch-mail.sh
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
```

Enable and start the user service:
```bash
systemctl --user daemon-reload
systemctl --user enable mail-watcher.service
systemctl --user start mail-watcher.service
```

### Usage
Run manually:
```bash
./watch-mail.sh
```

Restart systemd user services:
```bash
./restart-mail-services.sh
```

---

<p align="center">
  <sub>Powered by AI (IBM Granite 4.1 via Ollama)</sub>
</p>

<!-- #EOF -->




#### Powered with AI

<!-- #EOF -->
