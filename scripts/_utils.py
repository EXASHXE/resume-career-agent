#!/usr/bin/env python3
"""Shared utilities for resume-career-agent scripts.

Provides common path helpers, file I/O, dependency checking,
CLI argument helpers, JSON output, and config loading.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def get_root() -> Path:
    """Return the project root directory (parent of scripts/)."""
    return Path(__file__).resolve().parents[1]


def read_file(path: Path | str, encoding: str = "utf-8") -> str:
    """Read a text file, raising FileNotFoundError with a clear message if not found."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {p}")
    return p.read_text(encoding=encoding)


def write_file(path: Path | str, content: str, encoding: str = "utf-8") -> None:
    """Write content to a text file, creating parent directories as needed."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding=encoding)


def require_dependency(module_name: str, install_hint: str):
    """Import a required module or exit with a clear install hint.

    Returns the imported module.
    """
    try:
        return __import__(module_name)
    except ImportError as exc:
        raise SystemExit(f"Missing dependency: {install_hint}") from exc


def add_json_arg(parser: argparse.ArgumentParser) -> None:
    """Add a standardized --json flag to an argument parser."""
    parser.add_argument("--json", action="store_true", help="Output as JSON")


def add_json_out_arg(parser: argparse.ArgumentParser) -> None:
    """Add a standardized -o/--json-out flag to an argument parser."""
    parser.add_argument("-o", "--json-out", help="Write JSON output to file")


def output_json(data: object, json_out: str | None = None) -> None:
    """Output data as JSON. Write to file if json_out is given, else print to stdout."""
    payload = json.dumps(data, ensure_ascii=False, indent=2)
    if json_out:
        write_file(json_out, payload + "\n")
    else:
        print(payload)


def load_config(filename: str) -> object:
    """Load a JSON config file from the configs/ directory."""
    config_path = get_root() / "configs" / filename
    return json.loads(read_file(config_path))
