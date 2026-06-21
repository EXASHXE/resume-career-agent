#!/usr/bin/env python3
"""Deterministically extract normalized keywords from a JD (no LLM needed)."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ALIASES = {
    "distributed training": ["distributed training", "分布式训练"],
    "Megatron": ["megatron", "megatron-lm"],
    "profiling": ["profiling", "profiler", "性能分析", "性能剖析"],
    "memory optimization": ["memory optimization", "memory management", "显存优化", "内存优化", "oom"],
    "RAG": ["rag", "retrieval-augmented", "检索增强"],
    "Tool-Use": ["tool-use", "tool use", "tool calling", "工具调用"],
    "OpenAPI": ["openapi", "open api", "oas"],
    "SSE": ["sse", "server-sent events", "流式输出"],
    "IAM": ["iam", "identity and access management", "身份认证"],
    "Agent": ["agent", "智能体"],
    "PyTorch": ["pytorch", "torch"],
    "Python": ["python"],
    "Go": ["golang", "go"],
    "Rust": ["rust"],
    "Kubernetes": ["kubernetes", "k8s"],
    "Docker": ["docker", "container"],
    "TP": ["tensor parallel", "张量并行", "tp"],
    "PP": ["pipeline parallel", "流水线并行", "pp"],
    "DP": ["data parallel", "数据并行", "dp"],
    "HCCL": ["hccl"],
    "NCCL": ["nccl"],
    "FAISS": ["faiss"],
    "Kafka": ["kafka"],
    "Redis": ["redis"],
    "Envoy": ["envoy"],
    "etcd": ["etcd"],
    "OpenTelemetry": ["opentelemetry", "otel"],
    "HyDE": ["hyde"],
    "Reranker": ["reranker", "rerank"],
    "DevOps": ["devops"],
    "SRE": ["site reliability", "sre"],
    "CloudOps": ["cloudops", "cloud operations", "云运维"],
    "CI/CD": ["ci/cd", "continuous integration"],
    "observability": ["observability", "可观测"],
    "backend": ["backend", "后端"],
    "platform engineering": ["platform engineer", "平台工程"],
    "Terraform": ["terraform"],
    "ArgoCD": ["argocd"],
    "Prometheus": ["prometheus"],
    "Grafana": ["grafana"],
    "LangChain": ["langchain"],
    "LlamaIndex": ["llamaindex"],
}

SOFT = {
    "communication": ["communication", "沟通"],
    "collaboration": ["collaboration", "协作", "teamwork"],
    "ownership": ["ownership", "主人翁", "责任心"],
    "problem solving": ["problem solving", "解决问题"],
}

SENIORITY = [
    "senior", "staff", "principal", "lead", "architect",
    "mentoring", "ownership", "年以上", "years", "5\\+", "7\\+", "10\\+",
]

RISK_SIGNALS = [
    "\"fast[- ]paced\"", "wear many hats", "wearing many hats",
    "ninja", "rockstar", "guru", "unicorn", "10x",
]

ROLE_PATTERNS = [
    r"(?:job title|position|role|职位|岗位)\s*[:：]\s*([^\n]{2,80})",
    r"^#?\s*([^\n]{2,80}(?:engineer|工程师|开发|架构师))\s*$",
]


def hits(text: str, mapping: dict[str, list[str]]) -> list[str]:
    low = text.lower()
    return [
        name
        for name, terms in mapping.items()
        if any(
            re.search(r"(?<![\w-])" + re.escape(t.lower()) + r"(?![\w-])", low)
            for t in terms
        )
    ]


def nearby_items(text: str, markers: list[str]) -> list[str]:
    result = []
    for line in text.splitlines():
        low = line.lower()
        if any(m in low for m in markers):
            item = re.sub(r"^[\s*#\-\d.)]+", "", line).strip()
            if item and len(item) <= 240:
                result.append(item)
    return list(dict.fromkeys(result))


def extract(text: str) -> dict:
    role = ""
    for pattern in ROLE_PATTERNS:
        match = re.search(pattern, text, re.I | re.M)
        if match:
            role = match.group(1).strip(" -*#：:")
            break

    hard = hits(text, ALIASES)
    soft = hits(text, SOFT)
    domain = [
        x for x in hard
        if x in {
            "distributed training", "RAG", "Tool-Use", "Agent",
            "CloudOps", "DevOps", "SRE", "backend", "platform engineering",
        }
    ]
    seniority = [s for s in SENIORITY if re.search(s, text, re.I)]
    risk = [r for r in RISK_SIGNALS if re.search(r, text, re.I)]

    return {
        "role_title": role,
        "hard_skills": hard,
        "soft_skills": soft,
        "domain_keywords": domain,
        "seniority_signals": seniority,
        "must_have": nearby_items(text, ["must", "required", "requirement", "必须", "任职要求"]),
        "nice_to_have": nearby_items(text, ["nice to have", "preferred", "plus", "加分", "优先"]),
        "risk_signals": risk,
    }


def main() -> None:
    p = argparse.ArgumentParser(description="Extract normalized keywords from a job description.")
    p.add_argument("jd", help="Path to JD file (text)")
    p.add_argument("-o", "--json-out", help="Write JSON output to file")
    args = p.parse_args()

    text = Path(args.jd).read_text(encoding="utf-8")
    data = extract(text)
    payload = json.dumps(data, ensure_ascii=False, indent=2)

    if args.json_out:
        Path(args.json_out).write_text(payload + "\n", encoding="utf-8")
    else:
        print(payload)


if __name__ == "__main__":
    main()
