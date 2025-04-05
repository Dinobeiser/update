import os
import sys
import requests
import time

VERSION = "1.2.1"

REMOTE_VERSION_URL = "https://github.com/Dinobeiser/AT-Extender/blob/main/version.txt"
REMOTE_SCRIPT_URL = "https://github.com/Dinobeiser/AT-Extender/blob/main/aldi.py"

def compare_versions(local, remote):
    def to_tuple(v): return tuple(map(int, v.strip().split(".")))
    return to_tuple(remote) > to_tuple(local)

def check_for_update():
    try:
        print("🔍 Prüfe auf Updates...")
        response = requests.get(REMOTE_VERSION_URL)
        if response.status_code != 200:
            print("⚠️  Konnte Versionsinfo nicht abrufen.")
            return

        remote_version = response.text.strip()
        if compare_versions(VERSION, remote_version):
            print(f"🚀 Neue Version verfügbar: {remote_version} (aktuell: {VERSION})")
            update = requests.get(REMOTE_SCRIPT_URL)
            if update.status_code == 200:
                script_path = os.path.realpath(sys.argv[0])
                with open(script_path, 'w', encoding='utf-8') as f:
                    f.write(update.text)
                print("✅ Update erfolgreich! Starte neu...")
                os.execv(sys.executable, ['python'] + sys.argv)
            else:
                print("❌ Fehler beim Herunterladen der neuen Version.")
        else:
            print("✅ Du verwendest die neueste Version.")
    except Exception as e:
        print("❌ Fehler beim Update-Check:", e)

# ----------------------------------

def main():
    check_for_update()  # Ruft die Update-Funktion auf
    print(f"📦 Version {VERSION}")
    print("✅ Hauptfunktion läuft...")
    time.sleep(500)

if __name__ == "__main__":
    main()
