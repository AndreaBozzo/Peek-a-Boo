import os
from datapizza.tools import Tool # type: ignore

# --- DEFINIZIONE FUNZIONI PYTHON ---

def fast_list_files(directory: str = ".") -> str:
    """
    Elenca i file nella directory ignorando cartelle pesanti (node_modules, venv).
    Restituisce: Nome file e dimensione.
    """
    output = []
    ignored = {'.git', 'node_modules', '__pycache__', 'venv', '.idea', '.vscode'}
    
    try:
        # Se l'input è vuoto, usa la directory corrente
        target_dir = directory if directory else "."
        
        with os.scandir(target_dir) as entries:
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
        return "\n".join(output[:30]) # Tronchiamo per sicurezza
    except Exception as e:
        return f"Errore accesso directory: {str(e)}"

def read_head_tail(filepath: str) -> str:
    """
    Legge le prime 5 e ultime 5 righe.
    """
    if not os.path.exists(filepath):
        return "Errore: File non trovato."
    
    try:
        if os.path.getsize(filepath) > 50 * 1024 * 1024: # > 50MB
            return "File troppo grande (>50MB). Usa 'GrepSearch' o leggi parzialmente."

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            
        if len(lines) <= 10:
            return "".join(lines)
        
        preview = "".join(lines[:5]) + "\n... [SKIP] ...\n" + "".join(lines[-5:])
        return preview
    except Exception as e:
        return f"Errore lettura: {str(e)}"

def search_content(filepath: str, keyword: str) -> str:
    """
    Grep simulato: cerca keyword e restituisce la riga + numero riga.
    """
    if not os.path.exists(filepath):
        return "Errore: File non trovato."

    matches = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f):
                if keyword.lower() in line.lower():
                    clean = line.strip()[:200] # Max 200 char per riga
                    matches.append(f"Riga {i+1}: {clean}")
                    if len(matches) >= 5: break
        
        if not matches:
            return "Nessuna occorrenza trovata."
        return "\n".join(matches)
    except Exception as e:
        return f"Errore ricerca: {str(e)}"

# --- ESPORTAZIONE TOOLS PER DATAPIZZA ---

peek_tools = [
    Tool(
        name="ListFiles",
        func=fast_list_files,
        description="USALO PER PRIMO. Mostra i file nella cartella. Input: path (default '.')."
    ),
    Tool(
        name="ReadPreview",
        func=read_head_tail,
        description="Leggi inizio/fine file per capire formato/struttura. Input: filepath."
    ),
    Tool(
        name="GrepSearch",
        func=search_content,
        description="Cerca stringhe (password, key, error) nel file senza leggerlo tutto. Input: filepath, keyword."
    )
]