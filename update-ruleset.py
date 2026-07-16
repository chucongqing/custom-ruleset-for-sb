#!/usr/bin/env python3
"""Initialize and update all Git submodules to their tracked remote branch."""

import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: Path | None = None) -> None:
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd)
    if result.returncode != 0:
        print(f"Command failed with exit code {result.returncode}", file=sys.stderr)
        sys.exit(result.returncode)


def get_submodules(repo_root: Path) -> list[str]:
    """Read submodule names from .gitmodules."""
    gitmodules = repo_root / ".gitmodules"
    if not gitmodules.exists():
        return []

    result = subprocess.run(
        ["git", "config", "-f", str(gitmodules), "--get-regexp", "^submodule\\..*\\.path$"],
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return []

    submodules = []
    for line in result.stdout.splitlines():
        key, _ = line.split(maxsplit=1)
        # key is like "submodule.<name>.path"
        parts = key.split(".")
        if len(parts) >= 3:
            submodules.append(parts[1])
    return submodules


def main() -> None:
    repo_root = Path(__file__).parent.resolve()
    submodules = get_submodules(repo_root)

    if not submodules:
        print("No submodules found in .gitmodules.")
        return

    print("Initializing submodules...")
    run(["git", "submodule", "update", "--init", "--recursive"], cwd=repo_root)

    for name in submodules:
        print(f"Updating submodule '{name}' to latest remote branch...")
        run(["git", "submodule", "update", "--remote", name], cwd=repo_root)

    print("Done.")


if __name__ == "__main__":
    main()
