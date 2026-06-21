#!/usr/bin/env python3
"""Create a local gitignored private profile from the example template.

The created directory is automatically ignored by .gitignore.
Do not commit it.
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "resources/profiles/example"
PROFILES = ROOT / "resources/profiles"


def init_profile(name: str, force: bool = False) -> Path:
    target = PROFILES / name
    if target.exists():
        if not force:
            print(f"Error: '{target}' already exists. Use --force to overwrite.")
            sys.exit(1)
        shutil.rmtree(target)

    shutil.copytree(EXAMPLE, target)

    for f in target.rglob("*.example.md"):
        new_name = f.name.replace(".example", "")
        new_path = f.with_name(new_name)
        f.rename(new_path)

    for d in list(target.rglob("*")):
        if d.is_dir() and d.name == "projects":
            for pf in d.rglob("*.example.md"):
                new_name = pf.name.replace(".example", "")
                pf.rename(pf.with_name(new_name))

    print(f"Private profile created: {target}")
    print()
    print("Next steps:")
    print(f"  1. Edit files under {target}/")
    print(f"  2. Validate: python scripts/validate_profile.py {target}")
    print(f"  3. This directory is gitignored — do NOT commit it.")
    return target


def main() -> None:
    p = argparse.ArgumentParser(description="Create a local private profile.")
    p.add_argument("--name", required=True, help="Profile directory name (e.g., my-profile)")
    p.add_argument("--force", action="store_true", help="Overwrite if profile already exists")
    args = p.parse_args()
    init_profile(args.name, force=args.force)


if __name__ == "__main__":
    main()
