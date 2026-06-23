"""Tests for scripts/init_private_profile.py."""
import importlib.util
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Ensure scripts/ directory is in sys.path for _utils import
sys.path.insert(0, str(ROOT / "scripts"))

spec = importlib.util.spec_from_file_location("init", ROOT / "scripts/init_private_profile.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

EXAMPLE_SRC = ROOT / "resources/profiles/example"


def _make_init_func(tmp: str):
    """Create an init_profile function that uses a temp directory."""
    profiles_dir = Path(tmp) / "profiles"
    profiles_dir.mkdir(parents=True, exist_ok=True)

    def init(name: str, force: bool = False) -> Path:
        target = profiles_dir / name
        if target.exists():
            if not force:
                raise SystemExit(f"'{target}' already exists. Use --force to overwrite.")
            shutil.rmtree(target)
        shutil.copytree(EXAMPLE_SRC, target)
        for f in target.rglob("*.example.md"):
            new_name = f.name.replace(".example", "")
            f.rename(f.with_name(new_name))
        return target

    return init


def test_init_creates_profile():
    with tempfile.TemporaryDirectory() as tmp:
        init = _make_init_func(tmp)
        result = init("test-profile")
        assert result.exists()
        # Files should have .example suffix removed
        assert (result / "self_profile.md").exists()
        assert (result / "resume_base.md").exists()
        assert (result / "projects").is_dir()


def test_init_refuses_without_force():
    with tempfile.TemporaryDirectory() as tmp:
        init = _make_init_func(tmp)
        init("test-profile")
        try:
            init("test-profile", force=False)
            assert False, "Should have raised SystemExit"
        except SystemExit:
            pass


def test_init_with_force_overwrites():
    with tempfile.TemporaryDirectory() as tmp:
        init = _make_init_func(tmp)
        init("test-profile")
        result = init("test-profile", force=True)
        assert result.exists()
        assert (result / "self_profile.md").exists()
