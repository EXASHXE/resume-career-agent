#!/usr/bin/env python3
"""Package skill into a reproducible zip.

Runs privacy_guard and basic checks before packaging.
Excludes: .git, caches, dist, build, venvs, private profile data.
"""
from __future__ import annotations

import argparse
import importlib.util
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

EXCLUDE_DIRS = {
    "__pycache__", ".pytest_cache", ".git", "dist", "build",
    ".venv", "venv", ".mypy_cache", ".tox", "node_modules",
    ".private", ".local", "private", "local", "personal",
    "resume", "resumes", "jd", "jds", "materials", "career-assets",
}


def _run_guard() -> bool:
    try:
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/privacy_guard.py"), "--json"],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0:
            print("Privacy guard failed. Fix violations before packaging.")
            print(result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)
            return False
        return True
    except subprocess.TimeoutExpired:
        print("Privacy guard timed out.")
        return False


def create_zip(output_path: Path) -> Path:
    DIST.mkdir(exist_ok=True)
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(ROOT.rglob("*")):
            rel = path.relative_to(ROOT)
            parts = rel.parts
            if any(p in EXCLUDE_DIRS for p in parts):
                continue
            if path.suffix in {".zip", ".pdf", ".docx"}:
                continue
            if path.is_file():
                zf.write(path, str(rel))
    return output_path


def main() -> None:
    p = argparse.ArgumentParser(description="Package skill into zip.")
    p.add_argument(
        "--out",
        default=str(DIST / "resume-career-agent.zip"),
        help="Output zip path (default: dist/resume-career-agent.zip)",
    )
    p.add_argument(
        "--skip-guard",
        action="store_true",
        help="Skip privacy guard check (not recommended)",
    )
    args = p.parse_args()

    if not args.skip_guard:
        print("Running privacy guard...")
        if not _run_guard():
            sys.exit(1)

    print("Packaging skill...")
    out = create_zip(Path(args.out))
    size_mb = out.stat().st_size / (1024 * 1024)
    print(f"Packaged: {out} ({size_mb:.2f} MB)")


if __name__ == "__main__":
    main()
