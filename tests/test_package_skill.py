import importlib.util
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("package", ROOT / "scripts/package_skill.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_create_zip():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "test.zip"
        result = mod.create_zip(out)
        assert result.exists()
        assert result.stat().st_size > 0


def test_zip_includes_skill_md():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "test.zip"
        result = mod.create_zip(out)
        with zipfile.ZipFile(result, "r") as zf:
            names = zf.namelist()
        assert "SKILL.md" in names


def test_zip_includes_references():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "test.zip"
        result = mod.create_zip(out)
        with zipfile.ZipFile(result, "r") as zf:
            names = zf.namelist()
        ref_files = [n for n in names if n.startswith("references/")]
        assert len(ref_files) >= 10


def test_zip_includes_scripts():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "test.zip"
        result = mod.create_zip(out)
        with zipfile.ZipFile(result, "r") as zf:
            names = zf.namelist()
        script_files = [n for n in names if n.startswith("scripts/") and n.endswith(".py")]
        assert len(script_files) >= 8


def test_zip_excludes_git():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "test.zip"
        result = mod.create_zip(out)
        with zipfile.ZipFile(result, "r") as zf:
            names = zf.namelist()
        assert not any(n.startswith(".git/") for n in names)


def test_zip_includes_example_profile():
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "test.zip"
        result = mod.create_zip(out)
        with zipfile.ZipFile(result, "r") as zf:
            names = zf.namelist()
        example_files = [n for n in names if "resources/profiles/example/" in n]
        assert len(example_files) >= 4
