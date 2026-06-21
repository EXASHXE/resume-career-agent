import importlib.util
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_smoke_check_runs():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/smoke_check.py")],
        capture_output=True, text=True, timeout=30,
    )
    assert "Smoke Check" in result.stdout
    assert result.returncode == 0, f"Smoke check failed:\n{result.stdout}\n{result.stderr}"


def test_smoke_check_mentions_checks():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/smoke_check.py")],
        capture_output=True, text=True, timeout=30,
    )
    assert "Privacy Guard" in result.stdout
    assert "Validate Example Profile" in result.stdout
    assert "Package Skill" in result.stdout
