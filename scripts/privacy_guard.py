#!/usr/bin/env python3
"""Privacy guard — scan repo for forbidden personal asset patterns.

Loads:
- Forbidden path patterns and generic secret patterns from configs/privacy_rules.json.
- User-specific phrases from a local denylist file (via --denylist).

Exit 0 if clean, exit 1 if violations found.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

# Ensure script directory is in sys.path for _utils import
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _utils import get_root, add_json_arg, load_config

# Load configuration from external JSON
_cfg = load_config("privacy_rules.json")
SKIP_DIRS = set(_cfg["skip_dirs"])
FORBIDDEN_PATHS = _cfg["forbidden_paths"]
GENERIC_PATTERNS = [(p, label) for p, label in _cfg["generic_patterns"]]
EXEMPT_PATH = _cfg["exempt_path"]
DENYLIST_EXAMPLE = _cfg["denylist_example"]
DENYLIST_LOCAL = _cfg["denylist_local"]


def _is_text_file(path: Path) -> bool:
    try:
        with open(path, "rb") as f:
            chunk = f.read(1024)
        return b"\x00" not in chunk
    except OSError:
        return False


def _should_skip(path: Path, root: Path) -> bool:
    parts = path.relative_to(root).parts
    return any(p in SKIP_DIRS for p in parts)


def _load_denylist(path: Path) -> list[str]:
    phrases: list[str] = []
    try:
        content = path.read_text(encoding="utf-8").strip()
    except (OSError, FileNotFoundError):
        return phrases
    for line in content.splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            phrases.append(stripped)
    return phrases


def _get_tracked_files(root: Path) -> set[str]:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), "ls-files", "--cached"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return set(line.strip() for line in result.stdout.splitlines() if line.strip())
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        pass
    return set()


def scan(
    root: Path,
    denylist_phrases: list[str] | None = None,
    check_git_tracked: bool = True,
    run_generic_checks: bool = True,
) -> list[dict]:
    findings: list[dict] = []
    tracked = _get_tracked_files(root) if check_git_tracked else set()
    phrases = denylist_phrases or []

    for path in sorted(root.rglob("*")):
        if _should_skip(path, root):
            continue
        if not path.is_file():
            continue

        rel = str(path.relative_to(root)).replace("\\", "/")

        for fp in FORBIDDEN_PATHS:
            if rel.startswith(fp) or ("/" + fp) in ("/" + rel):
                if tracked and rel in tracked:
                    reason = "forbidden path pattern (tracked)"
                else:
                    reason = "forbidden path pattern"
                findings.append({
                    "path": rel,
                    "line": 0,
                    "matched": fp,
                    "reason": reason,
                })

        if EXEMPT_PATH in ("/" + rel):
            continue

        if not _is_text_file(path):
            continue

        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue

        for phrase in phrases:
            if phrase in content:
                lineno = 0
                for i, line in enumerate(content.splitlines(), 1):
                    if phrase in line:
                        lineno = i
                        break
                findings.append({
                    "path": rel,
                    "line": lineno,
                    "matched": phrase,
                    "reason": "forbidden phrase from denylist",
                })

        if run_generic_checks:
            for pattern, label in GENERIC_PATTERNS:
                for m in re.finditer(pattern, content):
                    lineno = content[:m.start()].count("\n") + 1
                    findings.append({
                        "path": rel,
                        "line": lineno,
                        "matched": m.group(),
                        "reason": f"generic: {label}",
                    })

    return findings


def _format_text(findings: list[dict]) -> str:
    if not findings:
        return "Privacy guard passed.\n"
    lines = ["PRIVACY GUARD FAILED", ""]
    for v in findings:
        loc = f"{v['path']}:{v['line']}" if v.get("line") else v["path"]
        lines.append(f"{loc}")
        lines.append(f"  matched: {v.get('matched', '')}")
        lines.append(f"  reason: {v['reason']}")
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Privacy guard scanner")
    parser.add_argument(
        "root",
        nargs="?",
        default=str(get_root()),
        help="root directory to scan (default: repo root)",
    )
    add_json_arg(parser)
    parser.add_argument(
        "--denylist",
        default=None,
        help=f"Path to denylist file (default: auto-detect {DENYLIST_LOCAL})",
    )
    parser.add_argument(
        "--no-git-check",
        action="store_true",
        help="Skip git-tracked file check",
    )
    parser.add_argument(
        "--no-generic",
        action="store_true",
        help="Skip generic secrets/keys/phone/email checks",
    )
    args = parser.parse_args()
    root = Path(args.root).resolve()

    denylist_path = None
    if args.denylist:
        denylist_path = Path(args.denylist)
    else:
        local = root / DENYLIST_LOCAL
        if local.is_file():
            denylist_path = local

    phrases = _load_denylist(denylist_path) if denylist_path else []
    findings = scan(
        root,
        denylist_phrases=phrases,
        check_git_tracked=not args.no_git_check,
        run_generic_checks=not args.no_generic,
    )

    if args.json:
        payload = {
            "ok": len(findings) == 0,
            "findings": findings,
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(_format_text(findings))

    sys.exit(1 if findings else 0)


if __name__ == "__main__":
    main()
