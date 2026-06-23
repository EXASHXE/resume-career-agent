import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
spec = importlib.util.spec_from_file_location("score", ROOT / "scripts/score_project_match.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
PROJECTS = ROOT / "resources/profiles/example/projects"


def scores(data):
    return {x["project"]: x["score"] for x in mod.score_projects(data, PROJECTS)}


def test_ai_infra_projects_rank_high():
    s = scores({
        "role_title": "AI Infra Engineer",
        "hard_skills": ["distributed training", "Megatron", "profiling", "memory optimization"],
        "domain_keywords": ["distributed training"],
    })
    assert s["example_distributed_system"] > s["example_agent_platform"]
    assert s["example_distributed_system"] > s["example_backend_platform"]


def test_agent_platform_ranks_high():
    s = scores({
        "role_title": "Agent Platform Engineer",
        "hard_skills": ["RAG", "Tool-Use", "OpenAPI", "SSE", "IAM", "Agent"],
        "domain_keywords": ["Agent", "CloudOps"],
    })
    assert s["example_agent_platform"] > s["example_distributed_system"]
    assert s["example_agent_platform"] > s["example_backend_platform"]


def test_backend_platform_ranks_high():
    s = scores({
        "role_title": "Backend Platform Engineer",
        "hard_skills": ["Kubernetes", "Docker", "Redis", "Kafka", "OpenTelemetry", "Terraform"],
        "domain_keywords": ["backend", "platform engineering"],
    })
    assert s["example_backend_platform"] > s["example_distributed_system"]
    assert s["example_backend_platform"] > s["example_agent_platform"]


def test_output_includes_missing_keywords():
    results = mod.score_projects({
        "role_title": "AI Infra Engineer",
        "hard_skills": ["distributed training", "Megatron", "unobtainium"],
        "domain_keywords": [],
    }, PROJECTS)
    for r in results:
        assert "missing_keywords" in r
        assert isinstance(r["missing_keywords"], list)


def test_output_includes_reasons():
    results = mod.score_projects({
        "role_title": "AI Infra Engineer",
        "hard_skills": ["distributed training"],
        "domain_keywords": [],
    }, PROJECTS)
    for r in results:
        assert "reasons" in r
        assert isinstance(r["reasons"], list)
