"""Tests for scripts/_utils.py shared utilities."""
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Ensure scripts/ directory is in sys.path for _utils import
import sys
sys.path.insert(0, str(ROOT / "scripts"))

from _utils import get_root, read_file, write_file, require_dependency, load_config, output_json


def test_get_root():
    root = get_root()
    assert root.is_dir()
    assert (root / "SKILL.md").exists()
    assert (root / "scripts").is_dir()


def test_read_file():
    content = read_file(ROOT / "SKILL.md")
    assert "Resume Career Agent" in content


def test_read_file_not_found():
    try:
        read_file(ROOT / "nonexistent_file.txt")
        assert False, "Should have raised FileNotFoundError"
    except FileNotFoundError as e:
        assert "not found" in str(e).lower()


def test_write_file():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "subdir" / "test.txt"
        write_file(out, "hello world")
        assert out.exists()
        assert out.read_text(encoding="utf-8") == "hello world"


def test_require_dependency_success():
    mod = require_dependency("json", "should not happen")
    assert mod is not None


def test_require_dependency_failure():
    try:
        require_dependency("nonexistent_module_xyz", "install xyz")
        assert False, "Should have raised SystemExit"
    except SystemExit as e:
        assert "install xyz" in str(e)


def test_load_config():
    cfg = load_config("jd_keywords.json")
    assert "aliases" in cfg
    assert "soft" in cfg
    assert "seniority" in cfg
    assert isinstance(cfg["aliases"], dict)
    assert "distributed training" in cfg["aliases"]


def test_load_config_lint_rules():
    cfg = load_config("lint_rules.json")
    assert "weak_zh" in cfg
    assert "weak_en" in cfg
    assert "fabrication_risk" in cfg
    assert isinstance(cfg["weak_zh"], list)


def test_load_config_privacy_rules():
    cfg = load_config("privacy_rules.json")
    assert "skip_dirs" in cfg
    assert "forbidden_paths" in cfg
    assert "generic_patterns" in cfg


def test_load_config_profile_schema():
    cfg = load_config("profile_schema.json")
    assert "required_sections" in cfg
    assert isinstance(cfg["required_sections"], list)
    assert len(cfg["required_sections"]) > 10


def test_output_json_stdout(capsys):
    data = {"key": "value", "num": 42}
    output_json(data)
    captured = capsys.readouterr()
    parsed = json.loads(captured.out)
    assert parsed["key"] == "value"
    assert parsed["num"] == 42


def test_output_json_to_file():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "output.json"
        output_json({"test": True}, json_out=str(out))
        content = json.loads(out.read_text(encoding="utf-8"))
        assert content["test"] is True
