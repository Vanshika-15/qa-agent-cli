import re
from pathlib import Path

IGNORE_DIRS = {"venv", ".git", "__pycache__", "node_modules", ".pytest_cache"}
CODE_EXTENSIONS = [".py", ".js", ".ts", ".jsx", ".tsx", ".java"]
MAX_LINES_PER_FILE = 150


def find_relevant_code(error_text: str, project_root: str = ".") -> str:
    """
    Look for filenames mentioned in an error/stack trace, and pull in the
    actual content of those files from the project (truncated), so the AI
    can reason about real code instead of guessing from the error text alone.
    """
    root = Path(project_root)

    # Find things that look like filenames in the error text, e.g. "git_utils.py", "main.js"
    mentioned = set(re.findall(r"[\w\-/]+\.(?:py|js|ts|jsx|tsx|java)", error_text))

    if not mentioned:
        return "(No specific filenames detected in the error text — analysis will rely on the error message alone.)"

    snippets = []
    for file_path in root.rglob("*"):
        if any(part in IGNORE_DIRS for part in file_path.parts):
            continue
        if file_path.suffix not in CODE_EXTENSIONS:
            continue

        # Match if the file's name (e.g. "git_utils.py") appears in the mentioned set
        if file_path.name in mentioned or any(m.endswith(file_path.name) for m in mentioned):
            try:
                lines = file_path.read_text(encoding="utf-8").splitlines()
            except (UnicodeDecodeError, PermissionError):
                continue

            truncated = "\n".join(lines[:MAX_LINES_PER_FILE])
            note = "" if len(lines) <= MAX_LINES_PER_FILE else f"\n... (truncated, {len(lines)} total lines)"
            snippets.append(f"--- {file_path} ---\n{truncated}{note}")

    if not snippets:
        return f"(Mentioned files {', '.join(mentioned)} were not found in this project — analysis will rely on the error message alone.)"

    return "\n\n".join(snippets)