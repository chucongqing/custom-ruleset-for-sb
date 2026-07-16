#!/usr/bin/env python3
"""Update the sing-geosite submodule to the latest rule-set branch."""

import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: Path | None = None) -> None:
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd)
    if result.returncode != 0:
        print(f"Command failed with exit code {result.returncode}", file=sys.stderr)
        sys.exit(result.returncode)


def main() -> None:
    repo_root = Path(__file__).parent.resolve()

    print("Updating sing-geosite submodule to latest rule-set...")
    run(["git", "submodule", "update", "--init", "--recursive"], cwd=repo_root)
    run(["git", "submodule", "update", "--remote", "sing-geosite"], cwd=repo_root)
    print("Done.")


if __name__ == "__main__":
    main()
