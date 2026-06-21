#!/usr/bin/env python3
"""Privacy guard — scan repo for forbidden personal asset patterns.

Loads:
- Built-in forbidden path patterns (hardcoded, generic).
- User-specific phrases from a local denylist file (via --denylist).
- Generic secrets/passwords/keys patterns (hardcoded, generic).

Exit 0 if clean, exit 1 if violations found.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

SKIP_DIRS = {
    ".git", "__pycache__", ".pytest_cache", "dist", "build",
    "node_modules", ".mypy_cache", ".tox", ".venv", "venv",
}

FORBIDDEN_PATHS = [
    "resources/profiles/default/",
    "resources/profiles/default/projects/",
    ".private/",
    ".local/",
    "private/",
    "local/",
    "personal/",
    "resume/",
    "resumes/",
    "jd/",
    "jds/",
    "materials/",
    "career-assets/",
]

GENERIC_PATTERNS = [
    (r"(?i)(?:private[_-]?key|secret[_-]?key|api[_-]?key|access[_-]?token)\s*[:=]\s*\S{8,}", "secret/key/token pattern"),
    (r"(?i)password\s*[:=]\s*\S{4,}", "password assignment"),
    (r"-----BEGIN (?:\w+ )?PRIVATE KEY-----", "PEM private key"),
    (r"(?<!\d)(?:86)?1[3-9]\d{9}(?!\d)", "phone number pattern"),
    (r"\b\d{17}[\dXx]\b", "ID number pattern"),
    (r"\b\d{6}\s*\d{4}\s*\d{2}\s*\d{2}\s*[\dXx]\b", "ID number pattern"),
]

EXEMPT_PATH = "resources/profiles/example/projects/"
DENYLIST_EXAMPLE = ".privacy-denylist.example"
DENYLIST_LOCAL = ".privacy-denylist.local"


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
                    reason = f"forbidden path pattern (tracked)"
                else:
                    reason = f"forbidden path pattern"
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
        default=str(Path(__file__).resolve().parents[1]),
        help="root directory to scan (default: repo root)",
    )
    parser.add_argument("--json", action="store_true", help="Output as JSON")
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
