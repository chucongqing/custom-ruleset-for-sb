# AGENTS.md — Project Guide for AI Coding Agents

This file documents the architecture, conventions, and workflows for working on this repository. Read this first if you are going to modify code, add rules, or change the build process.

## Project Overview

This repository is a curated collection of [sing-box](https://github.com/SagerNet/sing-box) rule-sets for major Chinese Internet services, intended to be routed directly (bypassing proxies). It does not store the actual compiled rule-set data; instead, it references rule-sets from a bundled `sing-geosite` Git submodule and generates a `rules.json` file containing absolute paths to those local `.srs` files.

The repository has no runtime server or service. The deliverable is the generated `rules.json`, which users reference from their sing-box configuration.

## Technology Stack

- **Languages:** Python 3 (build scripts only), JSON (data/template/generated output), Make (task runner)
- **Dependencies:** None outside the Python standard library and a working `git` CLI
- **External Data Source:** `sing-geosite` Git submodule, pinned to the `rule-set` branch (`https://github.com/SagerNet/sing-geosite.git`)
- **Target Platform:** Cross-platform — Windows, Linux, and macOS

There is no `pyproject.toml`, `requirements.txt`, `setup.py`, `package.json`, `Cargo.toml`, or similar package manifest because the Python scripts rely solely on the standard library.

## Project Structure

```text
.
├── sing-geosite/           # Git submodule: compiled sing-geosite rule-sets (*.srs)
├── .gitignore              # Ignores generated rules.json, Python cache, OS files
├── .gitmodules             # Declares the sing-geosite submodule and rule-set branch
├── Makefile                # Task runner for generate/update/clean/help
├── README.md               # User-facing documentation and usage examples
├── generate-rules.py       # Build script: rules.json.template -> rules.json
├── update-ruleset.py       # Maintenance script: update sing-geosite submodule
├── rules.example.json      # Small example showing alternate remote/local rule entries
├── rules.json.template     # Source of truth for the rule list (relative paths)
└── rules.json              # Generated output (absolute paths, not committed)
```

### Key Files

- **`rules.json.template`** — The hand-edited source of truth. Each rule entry uses a relative path under `sing-geosite/`. The `geoip-cn` entry is a remote rule referencing GitHub.
- **`rules.json`** — Generated from the template with absolute, OS-native paths. This file is ignored by Git and should not be edited by hand; it will be overwritten by `make generate` or `python generate-rules.py`.
- **`generate-rules.py`** — Reads `rules.json.template`, resolves every `local` rule's relative path to an absolute path using the repository root, and writes `rules.json`.
- **`update-ruleset.py`** — Initializes/updates the `sing-geosite` submodule to the latest `rule-set` branch.
- **`rules.example.json`** — A standalone example file for users who want a minimal ads/CN/geoip setup. It is not processed by any script.

## Build and Generation Commands

Use either `make` or the Python scripts directly.

```bash
# Generate rules.json from rules.json.template
make generate
# or
python generate-rules.py

# Update the sing-geosite submodule to the latest rule-set branch
make update
# or
python update-ruleset.py

# Remove the generated rules.json
make clean

# Default target: same as make generate
make all

# Show available Makefile targets
make help
```

### After Checking Out the Repository

If you cloned without submodules, initialize it first:

```bash
git submodule update --init --recursive
```

Then generate `rules.json`:

```bash
python generate-rules.py
```

## Runtime Architecture

There is no long-running process. The project produces a static `rules.json` artifact that is consumed by sing-box as a `route.rule_set` entry. A generated local rule looks like this:

```json
{
  "tag": "geosite-bilibili",
  "type": "local",
  "format": "binary",
  "path": "/absolute/path/to/sing-geosite/geosite-bilibili.srs"
}
```

On Windows the path is written with backslashes and escaped for JSON (`\\`). On Linux/macOS the path is POSIX-style.

The only remote rule in the default template is `geoip-cn`, which downloads from `https://raw.githubusercontent.com/SagerNet/sing-geoip/rule-set/geoip-cn.srs` via the `proxy` outbound.

## Code Style and Conventions

- **Python:** Follow PEP 8. The existing scripts use type hints, docstrings, and `pathlib.Path` for path manipulation.
- **Paths in templates:** Always use forward slashes (`sing-geosite/geosite-example.srs`) in `rules.json.template`; the generator normalizes them to the host OS separator.
- **Rule tags:** Use the sing-box convention `geosite-<name>` or `geoip-<name>`.
- **Template edits are the source of truth.** Never edit `rules.json` directly; it is generated and Git-ignored.
- **Generated output formatting:** `generate-rules.py` writes JSON with `indent=2` and a trailing newline. Preserve this if you change the generator.
- **Shebang:** Python scripts use `#!/usr/bin/env python3`.

### Adding a New Rule

1. Confirm the `.srs` file exists in `sing-geosite/` (or add/update the submodule first).
2. Add a new entry to `rules.json.template` with a relative path.
3. Run `python generate-rules.py` to update `rules.json`.
4. Update `README.md` if the service is documented in the included-services table or v2rayN geosite list.

## Testing Instructions

There is currently no automated test suite. Manual verification steps:

1. Run `python generate-rules.py` and confirm `rules.json` is produced without errors.
2. Validate that `rules.json` is valid JSON and that every `local` rule points to an existing `.srs` file under `sing-geosite/`.
3. Optionally load `rules.json` into a sing-box configuration and check that sing-box starts without rule-set path errors.

A quick shell check for missing files:

```bash
python -c "import json; rs=json.load(open('rules.json')); miss=[r for r in rs if r.get('type')=='local' and not __import__('os').path.exists(r['path'])]; print('Missing:', miss or 'none')"
```

## Deployment / Distribution

This repository is not deployed as an application. Distribution is via Git:

1. Commit changes to `rules.json.template`, scripts, documentation, and `.gitmodules`.
2. Do **not** commit `rules.json`; users generate it locally after cloning.
3. Ensure the `sing-geosite` submodule pointer reflects the desired `rule-set` commit.
4. Users clone with `--recurse-submodules` (or run `git submodule update --init --recursive`), then run `python generate-rules.py`.

## Security Considerations

- `rules.json` contains absolute local file system paths. If you distribute a pre-generated copy, be aware it exposes your local directory layout.
- The `geoip-cn` rule downloads a binary rule-set from a remote GitHub URL. In a strict threat model, verify the file or host it yourself.
- The `sing-geosite` submodule is fetched over HTTPS from `https://github.com/SagerNet/sing-geosite.git`. Ensure the submodule URL is trustworthy before running `make update`.
- Do not add credentials, private paths, or API keys to any file in this repository.

## Common Tasks for Agents

- **Add a new service:** edit `rules.json.template`, run `python generate-rules.py`, update `README.md`.
- **Refresh rule-set data:** run `make update` (pulls latest `rule-set` branch for `sing-geosite`).
- **Regenerate after template changes:** run `make generate` or `make all`.
- **Clean generated artifact:** run `make clean`.

## Notes

- The project intentionally stays dependency-free. Do not introduce third-party Python packages unless there is a strong reason, because there is no requirements file or lockfile to manage them.
- The `Makefile` uses POSIX-style commands (`rm -f`) and works under Git Bash on Windows. Native Windows shells may not run `make` targets unless a compatible Make environment is installed.
- `rules.example.json` is not used by the generator; it is only documentation.
