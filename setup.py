#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup per compilazione Gestionale Gitemania PORTABLE (Versione Definitiva con Icona)
"""
import os
import sys
import subprocess
import shutil

# --- CONFIGURAZIONE ---
APP_NAME = "GestionaleGitemania"
ENTRY_POINT = "gestionale_gitemania.py"
ICON_PATH = "assets/icon.ico"
SPEC_FILE_NAME = f"{APP_NAME}.spec"

def create_spec_file():
    """
    Crea un file .spec dettagliato per PyInstaller.
    Questo metodo è più affidabile per impostare l'icona e altri dettagli.
    """
    print("Creazione del file .spec per la compilazione...")

    # Lista dei file e delle cartelle da includere nella build
    datas_list = [
        ('assets', 'assets') # Aggiunge l'intera cartella 'assets'
    ]
    
    # Converte la lista per il formato .spec
    formatted_datas = ", ".join([f"('{src}', '{dest}')" for src, dest in datas_list])

    spec_content = f"""
# -*- mode: python ; coding: utf-8 -*-

# Questo file viene generato automaticamente da setup.py

a = Analysis(
    ['{ENTRY_POINT}'],
    pathex=['.'],
    binaries=[],
    datas=[{formatted_datas}],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='{APP_NAME}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False, # Imposta a False per nascondere la finestra di comando
    icon='{ICON_PATH}' # <-- ISTRUZIONE ESPLICITA E CORRETTA PER L'ICONA
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='{APP_NAME}'
)
"""
    with open(SPEC_FILE_NAME, 'w', encoding='utf-8') as f:
        f.write(spec_content)
    print(f"File '{SPEC_FILE_NAME}' creato con successo.")

def build_from_spec():
    """Esegue PyInstaller usando il file .spec generato."""
    if os.path.exists('dist'): shutil.rmtree('dist')
    if os.path.exists('build'): shutil.rmtree('build')
    
    print(f"Avvio compilazione usando '{SPEC_FILE_NAME}'...")
    
    command = ['pyinstaller', '--noconfirm', '--log-level=WARN', SPEC_FILE_NAME]
    
    try:
        # Usiamo .run() per catturare l'output in caso di errore
        result = subprocess.run(command, check=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        print(result.stdout) # Stampa l'output di PyInstaller
        
        print("\\nCOMPILAZIONE COMPLETATA CON SUCCESSO!")
        print(f"Cartella eseguibile creata in: dist/{APP_NAME}/")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\\nERRORE DURANTE LA COMPILAZIONE DI PYINSTALLER")
        print(f"Errore: {e.stderr}")
        return False
    except Exception as e:
        print(f"\\nUn errore imprevisto e' accaduto: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        try:
            print("Verifica PyInstaller...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
        except Exception as e:
            print(f"Errore installazione PyInstaller: {e}")
            sys.exit(1)
        
        create_spec_file()
        success = build_from_spec()
        sys.exit(0 if success else 1)
    else:
        print("Usa 'python setup.py build' per avviare la compilazione.")
