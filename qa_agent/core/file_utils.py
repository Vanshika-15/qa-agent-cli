from pathlib import Path


def read_test_files(directory: str, extensions: list[str] = None) -> str:
    """
    Read all test files in a directory and return their combined contents,
    each prefixed with its filename for context.
    """
    if extensions is None:
        extensions = [".py", ".js", ".ts", ".java", ".feature"]

    path = Path(directory)

    if not path.exists():
        raise ValueError(f"Directory not found: {directory}")

    if not path.is_dir():
        raise ValueError(f"Not a directory: {directory}")

    files_content = []
    for ext in extensions:
        for file_path in path.rglob(f"*{ext}"):
            try:
                content = file_path.read_text(encoding="utf-8")
                relative = file_path.relative_to(path)
                files_content.append(f"--- File: {relative} ---\n{content}")
            except (UnicodeDecodeError, PermissionError):
                continue

    if not files_content:
        raise ValueError(f"No test files found in {directory} (looked for: {', '.join(extensions)})")

    return "\n\n".join(files_content)