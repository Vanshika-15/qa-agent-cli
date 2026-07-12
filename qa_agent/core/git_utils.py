import subprocess


def get_diff(base: str = None) -> str:
    """
    Get the git diff for the current repo.
    - If `base` is given (e.g. 'main'), diffs current branch against it.
    - If not, diffs your uncommitted changes (working directory).
    """
    command = ["git", "diff", base] if base else ["git", "diff"]

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Git command failed: {result.stderr}")

    if not result.stdout.strip():
        raise ValueError("No diff found. Make sure you're in a git repo with changes, or check your --base branch name.")

    return result.stdout


def get_changed_files(base: str = None) -> list[str]:
    """
    Get just the list of changed file paths (no content), relative to repo root.
    """
    command = ["git", "diff", "--name-only"]
    if base:
        command.append(base)

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        raise RuntimeError(f"Git command failed: {result.stderr}")

    files = [f.strip() for f in result.stdout.splitlines() if f.strip()]

    if not files:
        raise ValueError("No changed files found. Make sure you're in a git repo with changes, or check your --base branch name.")

    return files