import os
import re
from typing import Optional

# 1. IL NAVIGATORE (Peek Structure)
# Sostituisce 'ls -R'. Restituisce solo i file, ignorando le cartelle di sistema pesanti.
def fast_list_files(directory: str = ".") -> str:
    """
    Elenca i file nella directory corrente mostrando nome e dimensione.
    Ignora cartelle nascoste o giganti come node_modules o venv.
    """
    output = []
    ignored = {'.git', 'node_modules', '__pycache__', 'venv', '.idea'}
    
    try:
        with os.scandir(directory) as entries:
            for entry in entries:
                if entry.name in ignored:
                    continue
                
                if entry.is_file():
                    size_kb = entry.stat().st_size / 1024
                    output.append(f"[FILE] {entry.name} ({size_kb:.1f}KB)")
                elif entry.is_dir():
                    output.append(f"[DIR]  {entry.name}/")
        
        if not output:
            return "Directory vuota."
        return "\n".join(output[:30]) # Max 30 file per non intasare il contesto
    except Exception as e:
        return f"Errore di accesso: {str(e)}"

# 2. LO STETOSCOPIO (Peek Head & Tail)
# Legge solo l'inizio e la fine per capire il formato del file.
def read_head_tail(filepath: str) -> str:
    """
    Legge le prime 5 e le ultime 5 righe di un file.
    Non carica mai l'intero file in memoria.
    """
    if not os.path.exists(filepath):
        return "Errore: File non trovato."
    
    try:
        # Controllo dimensione per sicurezza (max 100MB per il 'seek', ma leggiamo poco)
        if os.path.getsize(filepath) > 100 * 1024 * 1024: 
            return "File troppo grande (>100MB). Usa 'search_content' invece."

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            
        if len(lines) <= 10:
            return "".join(lines) # Se è piccolo, restituiscilo tutto
        
        preview = "".join(lines[:5]) + "\n... [CONTENT SKIPPED] ...\n" + "".join(lines[-5:])
        return preview
    except Exception as e:
        return f"Errore di lettura: {str(e)}"

# 3. IL BISTURI (Search/Grep)
# Cerca un ago nel pagliaio.
def search_content(filepath: str, keyword: str) -> str:
    """
    Cerca una keyword nel file e restituisce SOLO la riga che la contiene.
    Case insensitive.
    """
    if not os.path.exists(filepath):
        return "Errore: File non trovato."

    matches = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f):
                if keyword.lower() in line.lower():
                    # Pulizia: togliamo spazi eccessivi e tronchiamo righe chilometriche
                    clean_line = line.strip()[:150] 
                    matches.append(f"Riga {i+1}: {clean_line}")
                    
                    if len(matches) >= 5: # Max 5 risultati
                        matches.append("... [Altri risultati omessi]")
                        break
        
        if not matches:
            return f"Nessuna occorrenza di '{keyword}' trovata in {filepath}."
        
        return "\n".join(matches)
    except Exception as e:
        return f"Errore durante la ricerca: {str(e)}"