![Python](https://img.shields.io/badge/language-python-blue)
![Bash](https://img.shields.io/badge/language-bash-green)
![Ollama](https://img.shields.io/badge/Ollama-Granite_4.1--8b-orange)
![Version](https://img.shields.io/badge/version-1.0.4-blue)
![License](https://img.shields.io/badge/license-MIT-brightgreen)

# Nexus-Courier-AI 🤖✉️

## [DE]
`nexus-courier-ai` ist ein lokaler E-Mail-Assistent für Linux. Das System überwacht eine MBOX-Datei (`/var/mail/...`), verarbeitet eingehende Mails über eine lokale Ollama-Instanz und versendet die generierten Antworten per `nexus-courier.sh`.

### Architektur & Ablauf

+-------------------+      +---------------+      +---------------------+      +------------------+
|  Local MBOX File  | ---> | watch-mail.sh | ---> | mail-bot-eng-deu.py | ---> | nexus-courier.sh |
| (/var/mail/user)  |      | (inotifywait) |      | (Python venv v1.0.4)|      | (msmtp Transport)|
+-------------------+      +---------------+      +---------------------+      +------------------+

### Funktionsweise
* `watch-mail.sh` überwacht die MBOX-Datei via `inotifywait` auf Änderungen (Ignoriert Dateigrößen <= 14 Bytes, um Fehlstarts bei symbolischen Links / Symlink-Pfaden zu vermeiden).
* `mail-bot-eng-deu.py` liest die MBOX aus, dekodiert Header, entfernt vorhandene Signaturen und sendet den Inhalt an die Chat-API von Ollama.
* Die generierte Antwort wird direkt an `nexus-courier.sh` zum Versand übergeben.
* Nach erfolgreicher Verarbeitung aller Mails wird die MBOX-Datei geleert.

### ⚠️ Experimentelles Feature: Zweisprachiger Modus (DE / EN)
Mit der Version 1.0.4 wurde das Skript in `mail-bot-eng-deu.py` umbenannt. Es enthält ein **experimentelles und ungetestetes Feature** zur automatischen Erkennung und Beantwortung in der Sprache des Absenders (Deutsch oder Englisch).

#### Konfiguration der Antwortsprache
Die Steuerung der Sprache erfolgt über den System-Prompt in der Funktion `ask_ollama()` innerhalb von `mail-bot-eng-deu.py`:

* **Automatisch (DE / EN) [Standard in v1.0.4]:**
  REGELN:
  - Antworte in der Sprache, in der die eingehende E-Mail verfasst ist (Deutsch oder Englisch).
* **Rein Deutsch:**
  REGELN:
  - Antworte ausschließlich auf Deutsch.

### Voraussetzungen
* Linux (Debian/Ubuntu/Raspberry Pi OS)
* `fetchmail`, `inotify-tools`, `python3-pip`, `python3-venv`
* [Ollama](https://ollama.com/) (Getestet mit Modell `granite4.1:8b`)
* Eingerichtetes [nexus-courier](https://github.com/o-valo/nexus-courier) Skript

### Installation & Einrichtung

#### 1. Repository klonen
cd ~/progs
git clone https://github.com/o-valo/nexus-courier-ai.git
cd nexus-courier-ai

#### 2. Paketabhängigkeiten & venv
sudo apt update
sudo apt install fetchmail inotify-tools python3-pip python3-venv

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

#### 3. Ollama Modell laden
ollama pull granite4.1:8b

#### 4. Konfiguration
Passe die Pfade in `mail-bot-eng-deu.py` und `watch-mail.sh` an (`OLLAMA_HOST`, `MAILBOX_PATH`, `COURIER_PATH`, Python-Binary).

#### 5. Einbindung als Systemd User-Service (Autostart)
Um `watch-mail.sh` automatisch im Hintergrund laufen zu lassen, erstelle eine Service-Datei unter `~/.config/systemd/user/mail-watcher.service`:

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

Dienst aktivieren und starten:
systemctl --user daemon-reload
systemctl --user enable mail-watcher.service
systemctl --user start mail-watcher.service

### Nutzung
Skript manuell im Hintergrund starten:
./watch-mail.sh

Systemd User-Services neu laden/starten:
./restart-mail-services.sh

---

![Python](https://img.shields.io/badge/language-python-blue)
![Bash](https://img.shields.io/badge/language-bash-green)
![Ollama](https://img.shields.io/badge/Ollama-Granite_4.1--8b-orange)
![Version](https://img.shields.io/badge/version-1.0.4-blue)
![License](https://img.shields.io/badge/license-MIT-brightgreen)

## [ENG]
`nexus-courier-ai` is a local email assistant for Linux systems. It monitors a local MBOX file (`/var/mail/...`), processes incoming messages via a local Ollama instance, and dispatches responses using `nexus-courier.sh`.

### Architecture

+-------------------+      +---------------+      +---------------------+      +------------------+
|  Local MBOX File  | ---> | watch-mail.sh | ---> | mail-bot-eng-deu.py | ---> | nexus-courier.sh |
| (/var/mail/user)  |      | (inotifywait) |      | (Python venv v1.0.4)|      | (msmtp Transport)|
+-------------------+      +---------------+      +---------------------+      +------------------+

### How it works
* `watch-mail.sh` monitors the MBOX file using `inotifywait` (Ignores file sizes <= 14 bytes to prevent false triggers on symbolic link paths).
* `mail-bot-eng-deu.py` parses the MBOX file, decodes headers, strips incoming signatures, and queries the Ollama Chat API.
* Generated answers are forwarded directly to `nexus-courier.sh` for dispatch.
* The MBOX file is truncated after processing all messages.

### ⚠️ Experimental Feature: Bilingual Mode (DE / EN)
Starting with v1.0.4, the script is named `mail-bot-eng-deu.py` and introduces an **experimental and untested feature** for automatic language detection and response generation in either German or English.

#### Response Language Configuration
Language selection is handled via the system prompt inside the `ask_ollama()` function in `mail-bot-eng-deu.py`:

* **Automatic (DE / EN) [Default in v1.0.4]:**
  REGELN:
  - Antworte in der Sprache, in der die eingehende E-Mail verfasst ist (Deutsch oder Englisch).
* **Strict German:**
  REGELN:
  - Antworte ausschließlich auf Deutsch.

### Requirements
* Linux
* `fetchmail`, `inotify-tools`, `python3-pip`, `python3-venv`
* [Ollama](https://ollama.com/) (Tested with `granite4.1:8b`)
* Configured [nexus-courier](https://github.com/o-valo/nexus-courier) transport script

### Setup & Installation

#### 1. Clone repository
cd ~/progs
git clone https://github.com/o-valo/nexus-courier-ai.git
cd nexus-courier-ai

#### 2. Dependencies & venv
sudo apt update
sudo apt install fetchmail inotify-tools python3-pip python3-venv

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

#### 3. Pull Ollama Model
ollama pull granite4.1:8b

#### 4. Configuration
Configure local paths in `mail-bot-eng-deu.py` and `watch-mail.sh` (`OLLAMA_HOST`, `MAILBOX_PATH`, `COURIER_PATH`, Python binary).

#### 5. Systemd User Service Setup (Autostart)
To run `watch-mail.sh` automatically in the background, create `~/.config/systemd/user/mail-watcher.service`:

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

Enable and start the user service:
systemctl --user daemon-reload
systemctl --user enable mail-watcher.service
systemctl --user start mail-watcher.service

### Usage
Run manually:
./watch-mail.sh

Restart systemd user services:
./restart-mail-services.sh

---

#### Powered by AI

#EOF
