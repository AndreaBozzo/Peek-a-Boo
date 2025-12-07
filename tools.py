import os
import re
import fnmatch
from datapizza.tools import Tool  # type: ignore

# --- PYTHON FUNCTION DEFINITIONS ---


def fast_list_files(directory: str = ".") -> str:
    """
    List files in directory, ignoring heavy folders (node_modules, venv).
    Returns: filename and size.
    """
    output = []
    ignored = {'.git', 'node_modules', '__pycache__', 'venv', '.idea', '.vscode'}

    try:
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
            return "Empty directory."
        return "\n".join(output[:30])  # Truncate for safety
    except Exception as e:
        return f"Error accessing directory: {str(e)}"


def read_head_tail(filepath: str) -> str:
    """
    Read first 5 and last 5 lines of a file.
    """
    if not os.path.exists(filepath):
        return "Error: File not found."

    try:
        if os.path.getsize(filepath) > 50 * 1024 * 1024:  # > 50MB
            return "File too large (>50MB). Use 'GrepSearch' or read partially."

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        if len(lines) <= 10:
            return "".join(lines)

        preview = "".join(lines[:5]) + "\n... [SKIP] ...\n" + "".join(lines[-5:])
        return preview
    except Exception as e:
        return f"Error reading file: {str(e)}"


def search_content_with_context(filepath: str, keyword: str, context: int = 2, use_regex: bool = False) -> str:
    """
    Search for a keyword (or regex) and return the line + N lines of context before/after.
    """
    if not os.path.exists(filepath):
        return "Error: File not found."

    matches = []
    try:
        # Compile regex if requested
        if use_regex:
            try:
                pattern = re.compile(keyword, re.IGNORECASE)
            except re.error as e:
                return f"Error: Invalid regex: {str(e)}"

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            # Match with regex or string
            if use_regex:
                found = pattern.search(line) is not None
            else:
                found = keyword.lower() in line.lower()

            if found:
                start = max(0, i - context)
                end = min(len(lines), i + context + 1)

                snippet = "".join(lines[start:end])
                matches.append(f"--- Match at line {i+1} ---\n{snippet}\n")

                if len(matches) >= 3:
                    break

        if not matches:
            return "No matches found."
        return "\n".join(matches)
    except Exception as e:
        return f"Error searching: {str(e)}"


def find_files(directory: str = ".", pattern: str = "*", max_results: int = 20) -> str:
    """
    Search files recursively by glob pattern (e.g. *.env, *secret*, *.py).
    Ignores heavy directories.
    """
    ignored_dirs = {'.git', 'node_modules', '__pycache__', 'venv', '.idea', '.vscode'}
    results = []

    try:
        target_dir = directory if directory else "."

        for root, dirs, files in os.walk(target_dir):
            # Filter directories to ignore (in-place modification for os.walk)
            dirs[:] = [d for d in dirs if d not in ignored_dirs]

            for filename in files:
                # Match normal pattern + dotfile pattern (*.env -> also .env*)
                matches_pattern = fnmatch.fnmatch(filename, pattern)
                # If pattern is like "*.env", also try "*env*" for dotfiles like .env.production
                if not matches_pattern and pattern.startswith("*"):
                    dotfile_pattern = f"*{pattern[1:]}*"  # *.env -> *env* (catches .env.production)
                    matches_pattern = fnmatch.fnmatch(filename, dotfile_pattern)
                if matches_pattern:
                    filepath = os.path.join(root, filename)
                    # Relative path for cleaner output
                    rel_path = os.path.relpath(filepath, target_dir)
                    try:
                        size_kb = os.path.getsize(filepath) / 1024
                        results.append(f"{rel_path} ({size_kb:.1f}KB)")
                    except OSError:
                        results.append(f"{rel_path} (size unknown)")

                    if len(results) >= max_results:
                        results.append(f"... (truncated to {max_results} results)")
                        return "\n".join(results)

        if not results:
            return f"No files found for pattern '{pattern}'."
        return "\n".join(results)
    except Exception as e:
        return f"Error searching files: {str(e)}"


def grep_recursive(directory: str, keyword: str, pattern: str = "*", context: int = 1,
                   use_regex: bool = False, max_files: int = 10, max_matches: int = 5) -> str:
    """
    Search for a keyword in all files of a directory (recursive).
    Supports glob pattern filter and optional regex.
    """
    ignored_dirs = {'.git', 'node_modules', '__pycache__', 'venv', '.idea', '.vscode'}
    binary_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.ico', '.pdf', '.zip',
                         '.tar', '.gz', '.exe', '.dll', '.so', '.pyc', '.whl'}

    results = []
    files_searched = 0
    total_matches = 0

    try:
        target_dir = directory if directory else "."

        # Compile regex if requested
        if use_regex:
            try:
                regex_pattern = re.compile(keyword, re.IGNORECASE)
            except re.error as e:
                return f"Error: Invalid regex: {str(e)}"

        for root, dirs, files in os.walk(target_dir):
            dirs[:] = [d for d in dirs if d not in ignored_dirs]

            for filename in files:
                # Skip binary files
                _, ext = os.path.splitext(filename)
                if ext.lower() in binary_extensions:
                    continue

                # Filter by pattern
                if not fnmatch.fnmatch(filename, pattern):
                    continue

                filepath = os.path.join(root, filename)
                rel_path = os.path.relpath(filepath, target_dir)

                # Skip files too large (>1MB)
                try:
                    if os.path.getsize(filepath) > 1 * 1024 * 1024:
                        continue
                except OSError:
                    continue

                # Search in file
                try:
                    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                        lines = f.readlines()
                except Exception:
                    continue

                file_matches = []
                for i, line in enumerate(lines):
                    if use_regex:
                        found = regex_pattern.search(line) is not None
                    else:
                        found = keyword.lower() in line.lower()

                    if found:
                        start = max(0, i - context)
                        end = min(len(lines), i + context + 1)
                        snippet = "".join(lines[start:end]).rstrip()
                        file_matches.append(f"  L{i+1}: {snippet}")

                        if len(file_matches) >= 2:  # Max 2 matches per file
                            break

                if file_matches:
                    results.append(f"[{rel_path}]\n" + "\n".join(file_matches))
                    total_matches += len(file_matches)
                    files_searched += 1

                    if files_searched >= max_files or total_matches >= max_matches:
                        results.append(f"\n... (truncated: {files_searched} files, {total_matches} matches)")
                        return "\n\n".join(results)

        if not results:
            return f"No occurrences of '{keyword}' found."

        summary = f"\n--- Found {total_matches} matches in {files_searched} files ---"
        return "\n\n".join(results) + summary
    except Exception as e:
        return f"Error in recursive grep: {str(e)}"


# --- TOOL EXPORT FOR DATAPIZZA ---

peek_tools = [
    Tool(
        name="ListFiles",
        func=fast_list_files,
        description="USE THIS FIRST. Shows files in folder (non-recursive). Input: path (default '.')."
    ),
    Tool(
        name="FindFiles",
        func=find_files,
        description="Search files RECURSIVELY by glob pattern (e.g. '*.env', '*secret*', '*.py'). Input: directory, pattern, max_results."
    ),
    Tool(
        name="ReadPreview",
        func=read_head_tail,
        description="Read start/end of file to understand format/structure. Input: filepath."
    ),
    Tool(
        name="GrepSearch",
        func=search_content_with_context,
        description="Search keyword/regex in ONE file. Input: filepath, keyword, context (default 2), use_regex (default False)."
    ),
    Tool(
        name="GrepRecursive",
        func=grep_recursive,
        description="Search keyword/regex in ALL files of a directory. Input: directory, keyword, pattern (glob filter), context, use_regex, max_files, max_matches."
    )
]
