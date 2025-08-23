#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup per compilazione Gestionale Gitemania PORTABLE (Modalita Cartella Veloce)
"""

import os
import sys
import subprocess
import shutil

# --- CONFIGURAZIONE ---
APP_NAME = "GestionaleGitemania"
ENTRY_POINT = "gestionale_gitemania.py"
ICON_PATH = "assets/icon.ico"

def build_executable():
    """
    Esegue PyInstaller per creare una build in modalità cartella.
    """
    # Pulisce le build precedenti
    if os.path.exists('dist'): shutil.rmtree('dist')
    if os.path.exists('build'): shutil.rmtree('build')
    
    print("Avvio compilazione in modalita cartella (piu veloce)...")
    
    pyinstaller_command = [
        'pyinstaller',
        '--noconfirm',
        '--log-level=WARN',
        '--name', APP_NAME,
        '--icon', ICON_PATH,
        '--windowed',  # Nasconde la console di comando all'avvio
        '--add-data', 'assets;assets', # Aggiunge la cartella assets
        ENTRY_POINT
    ]
    
    try:
        print(f"Comando eseguito: {' '.join(pyinstaller_command)}")
        subprocess.run(pyinstaller_command, check=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        
        if os.path.exists(f'dist/{APP_NAME}'):
            print("\nCOMPILAZIONE COMPLETATA CON SUCCESSO!")
            print(f"Cartella eseguibile creata in: dist/{APP_NAME}/")
            return True
        else:
            print("\nERRORE: La cartella dell'eseguibile non e' stata trovata dopo la compilazione.")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"\nERRORE DURANTE LA COMPILAZIONE DI PYINSTALLER")
        print(f"Exit code: {e.returncode}")
        if e.stdout: print(f"Output:\n{e.stdout}")
        if e.stderr: print(f"Error:\n{e.stderr}")
        return False
    except Exception as e:
        print(f"\nUn errore imprevisto e' accaduto: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "build":
        # Installa PyInstaller se non presente
        try:
            print("Verifica PyInstaller...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
        except Exception as e:
            print(f"Errore installazione PyInstaller: {e}")
            sys.exit(1)
            
        success = build_executable()
        sys.exit(0 if success else 1)
    else:
        print("Usa 'python setup.py build' per avviare la compilazione.")
