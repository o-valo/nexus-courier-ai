![Python](https://img.shields.io/badge/language-python-blue)
![Bash](https://img.shields.io/badge/language-bash-green)
![Ollama](https://img.shields.io/badge/Ollama-Granite_4.1--8b-orange)
![Version](https://img.shields.io/badge/version-1.0.3-blue)
![License](https://img.shields.io/badge/license-MIT-brightgreen)

# Nexus-Courier-AI (v1.0.3) 🤖✉️

**Nexus-Courier-AI** ist ein lokaler, ereignisgesteuerter E-Mail-Assistent für Linux-Systeme. Er überwacht eingehende E-Mails (z. B. via Maildir/`inotifywait`), generiert mithilfe lokaler LLMs (**getestet mit IBM Granite 4.1 / `granite4.1:8b`** über **Ollama**) automatische Antworten und versendet diese zuverlässig über die Transportschicht **`nexus-courier`**.

100 % lokal, datenschutzfreundlich und modular aufgebaut (nach der UNIX-Philosophie).

---

## 🏗️ Architektur & Funktionsweise

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐      ┌─────────────────────┐
│  Maildir / New  │ ───> │ mail-watcher.sh  │ ───> │   mail-bot.py   │ ───> │  nexus-courier.sh   │
│ (Eingang Mail)  │      │  (inotifywait)   │      │ (Ollama Python) │      │  (msmtp Transport)  │
└─────────────────┘      └──────────────────┘      └─────────────────┘      └─────────────────────┘
```

1. **`mail-watcher.sh` (Event-Wächter v1.0.3):** Lauert über `inotify` auf neu eintreffende Dateien im Mail-Ordner.
2. **`mail-bot.py` (Gehirn v1.0.3):** Parst die E-Mail, schickt den Inhalt an IBM Granite 4.1 (`granite4.1:8b`) via Ollama und erstellt die Antwort.
3. **`nexus-courier.sh` (Postbote):** Übernimmt den E-Mail-Versand via `msmtp` mit Betreff (`-s`) und Anhängen (`-a`).

---

## 🚀 System-Voraussetzungen

- **Linux-Server / Raspberry Pi**
- **[Ollama](https://ollama.com/)** (Getestet mit Modell **`granite4.1:8b`**)
- **`msmtp`** (für den Mailversand)
- **`inotify-tools`** (für das File-System-Monitoring)
- **Python 3.8+**

---

## 🛠️ Quickstart

```bash
# Modell in Ollama bereitstellen
ollama pull granite4.1:8b

# Bot mit Beispiel-Mail testen
python3 mail-bot.py /path/to/sample_email.eml
```

---

## 📜 Lizenz

MIT License – Siehe [LICENSE](LICENSE) für Details.

---

#### Powered with AI

<!-- #EOF -->
