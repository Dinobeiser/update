import os
import sys
import requests
import time

VERSION = "1.2.2"  # Deine aktuelle Version

REMOTE_VERSION_URL = "https://raw.githubusercontent.com/Dinobeiser/update/main/version.txt"  # Link zur Version
REMOTE_SCRIPT_URL = "https://raw.githubusercontent.com/Dinobeiser/update/main/update.py"  # Link zum neuesten Skript

# Funktion, um Versionen zu vergleichen (Versionen in Tupel umwandeln)
def compare_versions(local, remote):
    def to_tuple(v): return tuple(map(int, v.strip().split(".")))
    return to_tuple(remote) > to_tuple(local)

# Funktion, die auf Updates prüft
def check_for_update():
    try:
        print("🔍 Prüfe auf Updates...")

        # Abrufen der Versionsnummer von der URL
        response = requests.get(REMOTE_VERSION_URL)

        # Debug-Ausgabe - Zeige den Inhalt der Antwort
        print("🌐 Response Text:", response.text[:100])  # zeigt die ersten 100 Zeichen der Antwort

        if response.status_code != 200:
            print(f"⚠️  Konnte Versionsinfo nicht abrufen, Statuscode: {response.status_code}")
            return
        
        # Extrahiere die Remote-Version und vergleiche sie mit der lokalen
        remote_version = response.text.strip()

        print(f"🔍 Lokale Version: {VERSION} | Remote Version: {remote_version}")

        if compare_versions(VERSION, remote_version):
            print(f"🚀 Neue Version verfügbar: {remote_version} (aktuell: {VERSION})")
            update = requests.get(REMOTE_SCRIPT_URL)
            if update.status_code == 200:
                print("✅ Update wird heruntergeladen...")
                # Skript aktualisieren
                script_path = os.path.realpath(sys.argv[0])
                with open(script_path, 'w', encoding='utf-8') as f:
                    f.write(update.text)
                print("✅ Update erfolgreich! Starte neu...")
                os.execv(sys.executable, ['python'] + sys.argv)
            else:
                print(f"❌ Fehler beim Herunterladen der neuen Version, Statuscode: {update.status_code}")
        else:
            print("✅ Du verwendest die neueste Version.")
    except Exception as e:
        print(f"❌ Fehler beim Update-Check: {e}")

# ----------------------------------

def main():
    check_for_update()  # Ruft die Update-Funktion auf
    print(f"📦 Version {VERSION}")
    print("✅ Hauptfunktion läuft...")
    time.sleep(500)

if __name__ == "__main__":
    main()
