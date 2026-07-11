import subprocess


def get_diff(base: str = None) -> str:
    """
    Get the git diff for the current repo.
    - If `base` is given (e.g. 'main'), diffs current branch against it.
    - If not, diffs your uncommitted changes (working directory).
    """
    if base:
        command = ["git", "diff", base]
    else:
        command = ["git", "diff"]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError(f"Git command failed: {result.stderr}")

    if not result.stdout.strip():
        raise ValueError("No diff found. Make sure you're in a git repo with changes, or check your --base branch name.")

    return result.stdout