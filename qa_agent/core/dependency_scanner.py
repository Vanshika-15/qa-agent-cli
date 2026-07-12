from pathlib import Path

# Folders we never want to scan into (virtual envs, git internals, caches)
IGNORE_DIRS = {"venv", ".git", "__pycache__", "node_modules", ".pytest_cache"}

CODE_EXTENSIONS = [".py", ".js", ".ts", ".jsx", ".tsx", ".java"]


def find_dependents(changed_files: list[str], project_root: str = ".") -> dict:
    """
    For each changed file, find other files in the project that appear to
    import or reference it (by module/file name).

    Returns: { changed_file: [list of files that reference it] }
    """
    root = Path(project_root)

    # Collect all candidate source files in the project (excluding ignored dirs)
    all_files = []
    for ext in CODE_EXTENSIONS:
        for file_path in root.rglob(f"*{ext}"):
            if any(part in IGNORE_DIRS for part in file_path.parts):
                continue
            all_files.append(file_path)

    dependents = {}

    for changed in changed_files:
        changed_path = Path(changed)
        # Use the filename without extension as the "module name" to search for
        module_name = changed_path.stem
        found = []

        for candidate in all_files:
            if str(candidate) == changed:
                continue  # don't count the file referencing itself
            try:
                content = candidate.read_text(encoding="utf-8")
            except (UnicodeDecodeError, PermissionError):
                continue

            if module_name and module_name in content:
                found.append(str(candidate))

        dependents[changed] = found

    return dependents