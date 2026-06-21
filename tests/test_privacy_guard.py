import importlib.util
import json
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("guard", ROOT / "scripts/privacy_guard.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_detects_forbidden_path():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        forbidden = d / "resources/profiles/default/projects"
        forbidden.mkdir(parents=True)
        (forbidden / "test.md").write_text("hello")
        findings = mod.scan(d)
        assert any("forbidden path pattern" in v["reason"] for v in findings)


def test_allows_example_projects():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        allowed = d / "resources/profiles/example/projects"
        allowed.mkdir(parents=True)
        (allowed / "example.md").write_text("safe content")
        findings = mod.scan(d)
        assert not any("forbidden path pattern" in v["reason"] for v in findings)


def test_allows_generic_tech_terms():
    generic_terms = [
        "Megatron is a framework for distributed training.",
        "NPU support is important for heterogeneous hardware.",
        "We use RAG for retrieval-augmented generation.",
        "OpenAPI is used for service specifications.",
        "CloudOps requires operational automation.",
    ]
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "safe.md").write_text("\n".join(generic_terms))
        findings = mod.scan(d, run_generic_checks=False)
        assert len(findings) == 0, f"Unexpected findings: {findings}"


def test_denylist_detects_phrase():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "config.md").write_text(
            "This document references ExamplePrivateEmployer and ExampleInternalProject."
        )
        phrases = ["ExamplePrivateEmployer", "ExampleInternalProject"]
        findings = mod.scan(d, denylist_phrases=phrases, run_generic_checks=False)
        assert any("ExamplePrivateEmployer" == v["matched"] for v in findings)
        assert any("ExampleInternalProject" == v["matched"] for v in findings)
        assert all("denylist" in v["reason"] for v in findings)


def test_denylist_empty_when_no_phrases():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "safe.md").write_text("normal content")
        findings = mod.scan(d, denylist_phrases=[], run_generic_checks=False)
        assert len(findings) == 0


def test_denylist_skips_comments():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        denylist = d / "deny.txt"
        denylist.write_text("# This is a comment\nActualPhrase\n# Another comment\n")
        phrases = mod._load_denylist(denylist)
        assert phrases == ["ActualPhrase"]


def test_private_dirs_detected():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "private").mkdir()
        (d / "private" / "secret.md").write_text("secret")
        findings = mod.scan(d, run_generic_checks=False)
        assert any("private/" in v["matched"] for v in findings), f"Findings: {findings}"


def test_materials_dir_detected():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "materials").mkdir()
        (d / "materials" / "note.md").write_text("note")
        findings = mod.scan(d, run_generic_checks=False)
        assert any("materials/" in v["matched"] for v in findings)


def test_json_output_format():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        (d / "clean.md").write_text("safe content")
        findings = mod.scan(d, run_generic_checks=False)
        payload = json.dumps(
            {"ok": len(findings) == 0, "findings": findings},
            ensure_ascii=False, indent=2,
        )
        parsed = json.loads(payload)
        assert isinstance(parsed["ok"], bool)
        assert isinstance(parsed["findings"], list)


def test_denylist_from_file():
    with tempfile.TemporaryDirectory() as tmp:
        d = Path(tmp)
        denylist = d / ".privacy-denylist.local"
        denylist.write_text("FictionalProjectAlpha\nFictionalPlatformBeta\n")
        (d / "doc.md").write_text(
            "We built FictionalProjectAlpha for our customers using FictionalPlatformBeta."
        )
        phrases = mod._load_denylist(denylist)
        findings = mod.scan(d, denylist_phrases=phrases, run_generic_checks=False)
        assert any("FictionalProjectAlpha" == v["matched"] for v in findings)
        assert any("FictionalPlatformBeta" == v["matched"] for v in findings)


def test_no_violations_clean_repo():
    findings = mod.scan(ROOT, run_generic_checks=False)
    assert len(findings) == 0, f"Unexpected findings in repo: {findings}"


def test_generic_checks_repo():
    findings = mod.scan(ROOT, run_generic_checks=True)
    # Generic checks may have false positives on example placeholder addresses;
    # the key invariant is that no denylist-path or denylist-phrase violations exist.
    # Accept findings only if they are from .privacy-denylist.example.
    unexpected = [
        f for f in findings
        if ".privacy-denylist.example" not in f["path"]
    ]
    assert len(unexpected) == 0, f"Unexpected generic findings: {unexpected}"
