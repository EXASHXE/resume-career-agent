import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Ensure scripts/ directory is in sys.path for _utils import
sys.path.insert(0, str(ROOT / "scripts"))

spec = importlib.util.spec_from_file_location("lint", ROOT / "scripts/lint_resume.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_weak_bullet_warns():
    warnings = mod.lint("## 项目经历\n- 负责项目，熟悉 Python，优化了系统")
    codes = {w["code"] for w in warnings}
    assert "weak-expression" in codes
    assert "missing-metric" in codes


def test_english_weak_expression():
    warnings = mod.lint("## Experience\n- Responsible for maintaining the CI/CD pipeline")
    codes = {w["code"] for w in warnings}
    assert "weak-expression-en" in codes or any(
        "responsible for" in w.get("message", "").lower() for w in warnings
    )


def test_fabrication_risk():
    warnings = mod.lint("## Projects\n- 优化后性能提升100%，彻底解决了稳定性问题")
    codes = {w["code"] for w in warnings}
    assert "fabrication-risk" in codes


def test_fail_on_warning_flag():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "test_weak_resume.md"
        p.write_text("## 项目经历\n- 负责项目，熟悉 Python", encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(ROOT / "scripts/lint_resume.py"),
             str(p), "--fail-on-warning"],
            capture_output=True, text=True,
        )
        assert result.returncode == 1


def test_empty_input():
    warnings = mod.lint("")
    assert isinstance(warnings, list)


def test_no_weak_expressions():
    warnings = mod.lint("## Experience\n- Built distributed training platform serving 10K+ GPUs")
    codes = {w["code"] for w in warnings}
    assert "weak-expression" not in codes
    assert "weak-expression-en" not in codes
