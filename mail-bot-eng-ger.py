#!/usr/bin/env python3
# ==============================================================================
# Dateiname: mail-bot.py
# Version: 1.0.4
# ==============================================================================

import email
import email.header
import email.utils
import os
import subprocess
import requests

# Konfiguration (Anpassen an dein System)
OLLAMA_HOST = "http://localhost:11434"
MODEL_NAME = "granite4.1:8b"
MAILBOX_PATH = os.path.expanduser("/var/mail/username")
COURIER_PATH = os.path.expanduser("~/nexus-courier/nexus-courier.sh")

# Signatur-Einstellung
SIGNATURE = """-- 
Diese E-Mail wurde automatisch von meinem Mail-Bot generiert.
Viele Grüße,
Dein Name"""

def decode_header_value(header_val):
    """
    Dekodiert Mime-kodierte Header-Werte (z.B. UTF-8 Betreffzeilen).
    """
    if not header_val:
        return "Kein Betreff"
    decoded_parts = email.header.decode_header(header_val)
    header_text = ""
    for part, encoding in decoded_parts:
        if isinstance(part, bytes):
            header_text += part.decode(encoding or "utf-8", errors="ignore")
        else:
            header_text += part
    return header_text.strip()

def clean_email_body(body):
    """
    Entfernt E-Mail-Signaturen (ab '-- ') und überflüssigen Leerraum.
    """
    if not body:
        return ""
    
    lines = body.splitlines()
    cleaned_lines = []
    
    for line in lines:
        if line.strip() == "--" or line.startswith("-- "):
            break
        cleaned_lines.append(line)
        
    return "\n".join(cleaned_lines).strip()

def ask_ollama(mail_content):
    url = f"{OLLAMA_HOST}/api/chat"
    
    combined_prompt = f"""Du bist ein mehrsprachiger E-Mail-Assistent. 

AUFGABE: Beantworte die folgende E-Mail direkt, präzise und höflich. Gehe genau auf Fragen oder Bitten ein.

REGELN:
- Antworte in der Sprache, in der die eingehende E-Mail verfasst ist (Deutsch oder Englisch).
- Gib NUR den Antworttext aus (keine Header, kein "Subject:", keine Meta-Kommentare, keine Grußformel/Signatur am Ende).

EINGEHENDE E-MAIL:
{mail_content}

ANTWORT:"""

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "user", "content": combined_prompt}
        ],
        "stream": False,
        "options": {
            "temperature": 0.4,
            "top_p": 0.9,
            "repeat_penalty": 1.05,
            "num_predict": 300
        }
    }
    
    print(f"[DEBUG] Sende Prompt an Ollama ({OLLAMA_HOST}, Modell: {MODEL_NAME})...")
    try:
        response = requests.post(url, json=payload, timeout=300)
        print(f"[DEBUG] Ollama HTTP-Statuscode: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            content = data.get("message", {}).get("content", "").strip()
            print(f"[DEBUG] Raw Modell-Output:\n'{content}'")
            return content if content else "Fehler: Modell hat leeren Text geliefert."
        else:
            print(f"[ERROR] Ollama antwortete mit Status: {response.status_code}")
            return f"Fehler bei Ollama API: {response.status_code}"
    except Exception as e:
        print(f"[ERROR] Verbindung zu Ollama fehlgeschlagen: {e}")
        return f"Verbindungsfehler zu Ollama: {str(e)}"

def send_reply(recipient, subject, body):
    if SIGNATURE.strip():
        full_body = f"{body}\n\n{SIGNATURE}"
    else:
        full_body = body

    # Erzwinge das "Re:" Präfix
    clean_subj = subject.strip()
    if clean_subj.lower().startswith("re:"):
        reply_subject = clean_subj
    else:
        reply_subject = f"Re: {clean_subj}"

    print(f"[DEBUG] Rufe Courier-Skript auf ({COURIER_PATH})")
    print(f"[DEBUG] Empfänger: '{recipient}'")
    print(f"[DEBUG] Betreff für Versand: '{reply_subject}'")

    try:
        cmd = [COURIER_PATH, "-s", reply_subject, recipient]
        subprocess.run(
            cmd,
            input=full_body.encode("utf-8"),
            check=True
        )
        print(f"[DEBUG] Courier-Skript erfolgreich ausgeführt.")
    except Exception as e:
        print(f"[ERROR] Fehler beim Senden der Antwort an {recipient}: {e}")

def parse_mbox_file(filepath):
    with open(filepath, 'rb') as f:
        content = f.read()

    if not content.strip():
        return []

    raw_messages = content.split(b'\nFrom ')
    messages = []

    for idx, raw in enumerate(raw_messages):
        if not raw.strip():
            continue
        
        msg_bytes = raw if idx == 0 and not content.startswith(b'From ') else b'From ' + raw
        msg = email.message_from_bytes(msg_bytes)
        messages.append(msg)

    return messages

def extract_body(message):
    body_content = ""
    if message.is_multipart():
        for part in message.walk():
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True)
                charset = part.get_content_charset() or "utf-8"
                if payload:
                    body_content = payload.decode(charset, errors="ignore")
                    break
    else:
        payload = message.get_payload(decode=True)
        charset = message.get_content_charset() or "utf-8"
        if payload:
            body_content = payload.decode(charset, errors="ignore")
            
    return body_content

def process_mails():
    print("=== Mail-Bot gestartet ===")
    print(f"[DEBUG] Prüfe Mailbox-Pfad: {MAILBOX_PATH}")

    if not os.path.exists(MAILBOX_PATH):
        print(f"[DEBUG] Mailbox-Datei existiert nicht: {MAILBOX_PATH}")
        print("=== Mail-Bot beendet ===")
        return

    mailbox_size = os.path.getsize(MAILBOX_PATH)
    print(f"[DEBUG] Größe der Mailbox-Datei: {mailbox_size} Bytes")

    if mailbox_size == 0:
        print("[DEBUG] Mailbox ist leer. Keine Aktion erforderlich.")
        print("=== Mail-Bot beendet ===")
        return

    try:
        messages = parse_mbox_file(MAILBOX_PATH)
        print(f"[DEBUG] Anzahl erfolgreich geparster E-Mails: {len(messages)}")

        for idx, message in enumerate(messages):
            print(f"\n--- Verarbeite E-Mail Index {idx} ---")
            
            from_header = message.get("From") or message.get("Return-Path") or message.get("X-Envelope-From")
            raw_subject = message.get("Subject", "Kein Betreff")
            subject = decode_header_value(raw_subject)

            if not from_header:
                print("[DEBUG] Überspringe E-Mail: Kein Absender-Header gefunden.")
                continue

            parsed_name, sender_email = email.utils.parseaddr(from_header)
            sender_email = sender_email.strip("<>")

            if not sender_email:
                print("[DEBUG] Überspringe E-Mail: Keine gültige Absenderadresse extrahierbar.")
                continue

            raw_body = extract_body(message)
            cleaned_body = clean_email_body(raw_body)

            print(f"[DEBUG] Extrahierte E-Mail-Adresse: '{sender_email}'")
            print(f"[DEBUG] Extrahierter Betreff: '{subject}'")
            print(f"[DEBUG] Rohinhalt-Länge: {len(raw_body)} Zeichen | Bereinigter Inhalt: {len(cleaned_body)} Zeichen")

            if not cleaned_body:
                print("[DEBUG] Überspringe E-Mail: Nach Bereinigung kein Inhalt vorhanden.")
                continue

            ai_response = ask_ollama(cleaned_body)

            print(f"[DEBUG] KI-Antwort generiert (Länge: {len(ai_response)} Zeichen)")
            send_reply(sender_email, subject, ai_response)

        with open(MAILBOX_PATH, 'w') as f:
            f.truncate(0)
        print("[DEBUG] Mailbox-Datei nach erfolgreicher Verarbeitung geleert.")

    except Exception as e:
        print(f"[ERROR] Fehler beim Verarbeiten der Mails: {e}")
    finally:
        print("=== Mail-Bot beendet ===")

if __name__ == "__main__":
    process_mails()

#EOF
