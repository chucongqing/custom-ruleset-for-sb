#!/usr/bin/env python3
"""Generate rules.json with absolute paths from rules.json.template."""

import json
import os
import sys
from pathlib import Path


def resolve_path(base_dir: Path, rel_path: str) -> str:
    """Resolve a relative path to an absolute Windows-style path."""
    # Handle both / and \ in template
    parts = rel_path.replace("/", os.sep).replace("\\", os.sep).split(os.sep)
    resolved = base_dir.joinpath(*parts).resolve()
    # Return Windows-style backslash path
    return str(resolved).replace("/", "\\")


def generate_rules_json(template_path: Path, output_path: Path) -> None:
    with open(template_path, "r", encoding="utf-8") as f:
        rules = json.load(f)

    repo_root = template_path.parent.resolve()

    for rule in rules:
        if rule.get("type") == "local" and "path" in rule:
            rule["path"] = resolve_path(repo_root, rule["path"])

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(rules, f, indent=2)
        f.write("\n")

    print(f"Generated {output_path}")


if __name__ == "__main__":
    script_dir = Path(__file__).parent.resolve()
    template = script_dir / "rules.json.template"
    output = script_dir / "rules.json"

    if not template.exists():
        print(f"Template not found: {template}", file=sys.stderr)
        sys.exit(1)

    generate_rules_json(template, output)
