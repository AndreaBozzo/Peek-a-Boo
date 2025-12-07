import os
import re
import fnmatch
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

def search_content_with_context(filepath: str, keyword: str, context: int = 2, use_regex: bool = False) -> str:
    """
    Cerca una keyword (o regex) e restituisce la riga + N righe di contesto prima e dopo.
    """
    if not os.path.exists(filepath):
        return "Errore: File non trovato."

    matches = []
    try:
        # Compila regex se richiesto
        if use_regex:
            try:
                pattern = re.compile(keyword, re.IGNORECASE)
            except re.error as e:
                return f"Errore regex invalida: {str(e)}"

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            # Match con regex o string
            if use_regex:
                match = pattern.search(line)
            else:
                match = keyword.lower() in line.lower()

            if match:
                start = max(0, i - context)
                end = min(len(lines), i + context + 1)

                snippet = "".join(lines[start:end])
                matches.append(f"--- Match at line {i+1} ---\n{snippet}\n")

                if len(matches) >= 3: break

        if not matches:
            return "Nessuna occorrenza trovata."
        return "\n".join(matches)
    except Exception as e:
        return f"Errore ricerca: {str(e)}"


def find_files(directory: str = ".", pattern: str = "*", max_results: int = 20) -> str:
    """
    Cerca file ricorsivamente per glob pattern (es. *.env, *secret*, *.py).
    Ignora cartelle pesanti.
    """
    ignored_dirs = {'.git', 'node_modules', '__pycache__', 'venv', '.idea', '.vscode'}
    results = []

    try:
        target_dir = directory if directory else "."

        for root, dirs, files in os.walk(target_dir):
            # Filtra directory da ignorare (modifica in-place per os.walk)
            dirs[:] = [d for d in dirs if d not in ignored_dirs]

            for filename in files:
                # Matcha pattern normale + pattern per dotfiles (*.env -> anche .env*)
                matches_pattern = fnmatch.fnmatch(filename, pattern)
                # Se pattern è tipo "*.env", prova anche "*env*" per dotfiles come .env.production
                if not matches_pattern and pattern.startswith("*"):
                    dotfile_pattern = f"*{pattern[1:]}*"  # *.env -> *env* (cattura .env.production)
                    matches_pattern = fnmatch.fnmatch(filename, dotfile_pattern)
                if matches_pattern:
                    filepath = os.path.join(root, filename)
                    # Path relativo per output più pulito
                    rel_path = os.path.relpath(filepath, target_dir)
                    try:
                        size_kb = os.path.getsize(filepath) / 1024
                        results.append(f"{rel_path} ({size_kb:.1f}KB)")
                    except OSError:
                        results.append(f"{rel_path} (size unknown)")

                    if len(results) >= max_results:
                        results.append(f"... (troncato a {max_results} risultati)")
                        return "\n".join(results)

        if not results:
            return f"Nessun file trovato per pattern '{pattern}'."
        return "\n".join(results)
    except Exception as e:
        return f"Errore ricerca file: {str(e)}"


def grep_recursive(directory: str, keyword: str, pattern: str = "*", context: int = 1,
                   use_regex: bool = False, max_files: int = 10, max_matches: int = 5) -> str:
    """
    Cerca una keyword in tutti i file di una directory (ricorsivo).
    Supporta filtro per pattern glob e regex opzionale.
    """
    ignored_dirs = {'.git', 'node_modules', '__pycache__', 'venv', '.idea', '.vscode'}
    binary_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.ico', '.pdf', '.zip',
                         '.tar', '.gz', '.exe', '.dll', '.so', '.pyc', '.whl'}

    results = []
    files_searched = 0
    total_matches = 0

    try:
        target_dir = directory if directory else "."

        # Compila regex se richiesto
        if use_regex:
            try:
                regex_pattern = re.compile(keyword, re.IGNORECASE)
            except re.error as e:
                return f"Errore regex invalida: {str(e)}"

        for root, dirs, files in os.walk(target_dir):
            dirs[:] = [d for d in dirs if d not in ignored_dirs]

            for filename in files:
                # Salta file binari
                _, ext = os.path.splitext(filename)
                if ext.lower() in binary_extensions:
                    continue

                # Filtra per pattern
                if not fnmatch.fnmatch(filename, pattern):
                    continue

                filepath = os.path.join(root, filename)
                rel_path = os.path.relpath(filepath, target_dir)

                # Salta file troppo grandi (>1MB)
                try:
                    if os.path.getsize(filepath) > 1 * 1024 * 1024:
                        continue
                except OSError:
                    continue

                # Cerca nel file
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                except Exception:
                    continue

                file_matches = []
                for i, line in enumerate(lines):
                    if use_regex:
                        match = regex_pattern.search(line)
                    else:
                        match = keyword.lower() in line.lower()

                    if match:
                        start = max(0, i - context)
                        end = min(len(lines), i + context + 1)
                        snippet = "".join(lines[start:end]).rstrip()
                        file_matches.append(f"  L{i+1}: {snippet}")

                        if len(file_matches) >= 2:  # Max 2 match per file
                            break

                if file_matches:
                    results.append(f"[{rel_path}]\n" + "\n".join(file_matches))
                    total_matches += len(file_matches)
                    files_searched += 1

                    if files_searched >= max_files or total_matches >= max_matches:
                        results.append(f"\n... (troncato: {files_searched} file, {total_matches} match)")
                        return "\n\n".join(results)

        if not results:
            return f"Nessuna occorrenza di '{keyword}' trovata."

        summary = f"\n--- Trovati {total_matches} match in {files_searched} file ---"
        return "\n\n".join(results) + summary
    except Exception as e:
        return f"Errore grep ricorsivo: {str(e)}"

# --- ESPORTAZIONE TOOLS PER DATAPIZZA ---

peek_tools = [
    Tool(
        name="ListFiles",
        func=fast_list_files,
        description="USALO PER PRIMO. Mostra i file nella cartella (non ricorsivo). Input: path (default '.')."
    ),
    Tool(
        name="FindFiles",
        func=find_files,
        description="Cerca file RICORSIVAMENTE per pattern glob (es. '*.env', '*secret*', '*.py'). Input: directory, pattern, max_results."
    ),
    Tool(
        name="ReadPreview",
        func=read_head_tail,
        description="Leggi inizio/fine file per capire formato/struttura. Input: filepath."
    ),
    Tool(
        name="GrepSearch",
        func=search_content_with_context,
        description="Cerca keyword/regex in UN file. Input: filepath, keyword, context (default 2), use_regex (default False)."
    ),
    Tool(
        name="GrepRecursive",
        func=grep_recursive,
        description="Cerca keyword/regex in TUTTI i file di una directory. Input: directory, keyword, pattern (glob filter), context, use_regex, max_files, max_matches."
    )
]