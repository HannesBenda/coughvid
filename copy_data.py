import os
import json
import glob
import shutil

# 1. Pfade definieren
work_dir = os.getcwd()
source_folder = f"{work_dir}/coughvid_20211012"
target_folder = f"{work_dir}/08_coughvid" # Der neue Ordner für die EDA
threshold = 0.8

# Erstelle den Zielordner, falls er noch nicht existiert
if not os.path.exists(target_folder):
    os.makedirs(target_folder)
    print(f"Ordner '{target_folder}' wurde erstellt.")

# 2. Alle JSON-Dateien finden
json_files = glob.glob(os.path.join(source_folder, "*.json"))
copied_count = 0

print(f"Analysiere {len(json_files)} Dateien...")

for json_path in json_files:
    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
            # Prüfe den cough_detected Wert (Konvertierung zu float zur Sicherheit)
            cough_score = float(data.get('cough_detected', 0))
            
            if cough_score >= threshold:
                # Basis-Dateiname ohne Endung extrahieren (z.B. "00a1e1ea...")
                base_name = os.path.splitext(os.path.basename(json_path))[0]
                
                # Finde alle Dateien mit diesem Basisnamen (json, wav, webm, etc.)
                matching_files = glob.glob(os.path.join(source_folder, base_name + ".*"))
                
                for file_to_copy in matching_files:
                    shutil.copy(file_to_copy, target_folder)
                
                copied_count += 1
                
        except (ValueError, json.JSONDecodeError) as e:
            print(f"Fehler bei Datei {json_path}: {e}")

print(f"Fertig! {copied_count} Datensätze (JSON + Audio) wurden nach '{target_folder}' kopiert.")