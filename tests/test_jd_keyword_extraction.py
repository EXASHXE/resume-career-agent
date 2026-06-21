import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("extract", ROOT / "scripts/extract_jd_keywords.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def test_ai_infra_keywords():
    out = mod.extract(
        "Role: AI Infra Engineer\n"
        "Required: distributed training, Megatron, profiling, memory optimization"
    )
    assert {"distributed training", "Megatron", "profiling", "memory optimization"} <= set(out["hard_skills"])


def test_agent_engineer_keywords():
    out = mod.extract(
        "Role: Agent Platform Engineer\n"
        "Must have Agent, RAG, Tool-Use, OpenAPI, SSE and IAM."
    )
    assert {"RAG", "Tool-Use", "OpenAPI", "SSE", "IAM", "Agent"} <= set(out["hard_skills"])


def test_cloudops_keywords():
    out = mod.extract(
        "Role: CloudOps Engineer\n"
        "Required: CloudOps, Kubernetes, Docker, CI/CD, observability"
    )
    assert "CloudOps" in out["hard_skills"]
    assert "Kubernetes" in out["hard_skills"]


def test_backend_platform_keywords():
    out = mod.extract(
        "Role: Backend Platform Engineer\n"
        "Must have: Python, Go, Kubernetes, Docker, Terraform, Redis, Kafka"
    )
    assert "Python" in out["hard_skills"]
    assert "Go" in out["hard_skills"]
    assert "Kubernetes" in out["hard_skills"]


def test_seniority_signals():
    out = mod.extract("Role: Senior Engineer\n5+ years experience")
    assert "senior" in out["seniority_signals"]


def test_risk_signals():
    out = mod.extract("We want a ninja rockstar who wears many hats!")
    assert len(out.get("risk_signals", [])) > 0


def test_chinese_jd():
    out = mod.extract("岗位：AI 基础设施工程师\n任职要求：分布式训练、Megatron、性能分析")
    assert "distributed training" in out["hard_skills"]
    assert "profiling" in out["hard_skills"]


def test_role_title_extraction():
    out = mod.extract("# Senior Backend Engineer\n\nRequirements: Python, Go, Kubernetes")
    assert "Senior Backend Engineer" in out["role_title"]
