import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location("validate", ROOT / "scripts/validate_profile.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_example_profile_valid():
    result = mod.validate(ROOT / "resources/profiles/example")
    assert result["valid"], f"Issues: {result['issues']}"


def test_missing_profile_dir():
    result = mod.validate(ROOT / "resources/profiles/nonexistent")
    assert not result["valid"]


def test_includes_files_list():
    result = mod.validate(ROOT / "resources/profiles/example")
    assert len(result["files"]) >= 3  # self_profile, resume_base, 3 project assets
    assert any("self_profile" in f for f in result["files"])
    assert any("resume_base" in f for f in result["files"])


def test_example_profile_has_no_issues():
    result = mod.validate(ROOT / "resources/profiles/example")
    assert len(result["issues"]) == 0, f"Unexpected issues: {result['issues']}"
