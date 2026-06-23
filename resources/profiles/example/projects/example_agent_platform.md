## Metadata

- **Project**: Example Agent Platform
- **Role**: Agent Platform Engineer
- **Period**: 2023-06 — 2024-12
- **Team size**: 5 engineers
- **Personal ownership**: Agent orchestration framework, RAG pipeline

## One-line Summary

Built an LLM agent orchestration platform with RAG, tool-use, and multi-step reasoning for enterprise workflow automation.

## Problem / Context

Enterprise customers needed AI agents that could execute multi-step workflows using internal tools and knowledge bases. Existing solutions lacked reliable tool-calling, context management, and observability for production deployments.

## Technical Challenges

- Designing a reliable tool-calling protocol with error recovery and retry logic
- Building a RAG pipeline with hybrid search (dense + sparse) and reranking
- Implementing streaming response with SSE for real-time agent status updates
- Ensuring agent actions are auditable and reversible for compliance

## Architecture

- Agent runtime with pluggable tool registry and execution sandbox
- RAG service with dual-encoder retrieval and cross-encoder reranking
- Orchestrator managing multi-step reasoning with plan-execute-reflect loop
- API gateway with IAM integration and audit logging

## Core Modules

- **Tool Registry**: Dynamic tool registration with OpenAPI schema validation
- **RAG Pipeline**: Hybrid retrieval with HyDE query expansion and cross-encoder reranking
- **Orchestrator**: Plan-execute-reflect loop with context window management
- **Audit Service**: Immutable action log with compliance reporting

## Key Decisions / Trade-offs

- Chose plan-execute-reflect over ReAct for better control over long workflows
- Used cross-encoder reranking despite latency cost (50ms) for higher precision
- Implemented tool execution in sandboxed containers for security isolation
- Chose SSE over WebSocket for streaming due to simpler infrastructure requirements

## Personal Contribution Candidates

- Designed the agent orchestration framework architecture
- Implemented the RAG pipeline with hybrid search and reranking
- Built the tool registry with OpenAPI schema validation
- Developed the streaming response system with SSE

## Technologies

Python, LangChain, FAISS, OpenAPI, SSE, IAM, Kubernetes, Redis, PostgreSQL

## Keywords

Agent, RAG, Tool-Use, OpenAPI, SSE, IAM, LangChain, FAISS, orchestration, reranker, HyDE

## Resume Bullets - zh-CN

- 设计并实现 LLM Agent 编排平台，支持 RAG 检索增强和工具调用，服务 [TODO / 待补：用户数] 企业客户
- 构建混合检索 RAG 管线（稠密+稀疏），引入交叉编码器重排序，检索准确率提升 [TODO / 待补：百分比]
- 实现基于 OpenAPI 的动态工具注册与沙箱执行，支持 [TODO / 待补：工具数] 企业内部工具
- 开发 SSE 流式响应系统，实现 Agent 执行状态的实时可观测

## Resume Bullets - en-US

- Designed LLM agent orchestration platform with RAG and tool-calling, serving [TODO / 待补：user count] enterprise customers
- Built hybrid retrieval RAG pipeline (dense + sparse) with cross-encoder reranking, improving retrieval accuracy by [TODO / 待补：percentage]
- Implemented OpenAPI-based dynamic tool registry with sandboxed execution, supporting [TODO / 待补：tool count] internal enterprise tools
- Developed SSE streaming response system enabling real-time agent execution observability

## Interview Pitch - zh-CN

### 60 秒版

我负责设计和实现企业级 LLM Agent 编排平台。核心能力包括 RAG 检索增强、OpenAPI 工具调用和多步推理。平台采用了 plan-execute-reflect 编排模式，配合混合检索 RAG 管线，服务了多个企业客户的工作流自动化需求。

### 3 分钟版

[在 60 秒版基础上展开] 技术选型方面，我们对比了 ReAct 和 plan-execute-reflect 两种模式。ReAct 更灵活但在长流程中容易偏离目标，plan-execute-reflect 通过显式规划步骤提供了更好的可控性。RAG 管线方面，我们用 HyDE 做查询扩展，双编码器做初筛，交叉编码器做精排，虽然精排增加了 50ms 延迟，但准确率提升显著。工具执行方面，我们在容器沙箱中运行，确保安全性。

## Interview Pitch - en-US

### 60-second version

I designed and built an enterprise LLM agent orchestration platform. Core capabilities include RAG-augmented retrieval, OpenAPI tool-calling, and multi-step reasoning. The platform uses a plan-execute-reflect orchestration pattern with a hybrid retrieval RAG pipeline, serving multiple enterprise customers for workflow automation.

### 3-minute version

[Expanding on the 60-second version] For orchestration, we compared ReAct vs plan-execute-reflect. ReAct is more flexible but tends to drift in long workflows; plan-execute-reflect provides better control through explicit step planning. For the RAG pipeline, we use HyDE for query expansion, dual-encoder for initial retrieval, and cross-encoder for reranking. The reranking adds 50ms latency but significantly improves accuracy. Tool execution runs in container sandboxes for security isolation.

## Likely Interview Questions

1. How did you handle tool execution failures and retries?
2. What was your context window management strategy for long workflows?
3. How did you evaluate RAG retrieval quality?
4. What observability and debugging tools did you build for agents?
5. How did you handle IAM and permission scoping for tool access?

## Metrics To Confirm

- [ ] Number of enterprise customers served
- [ ] RAG retrieval accuracy improvement percentage
- [ ] Number of supported tools
- [ ] End-to-end latency for typical workflows
- [ ] Agent task completion rate

## Missing Information

- Specific enterprise customer names (confidential)
- Production deployment scale and traffic numbers
- Comparison baseline for retrieval accuracy
- Cost analysis of cross-encoder reranking

## Red Flags / Risks

- "Enterprise customers" is vague — need at least count and industry
- RAG accuracy claims need methodology documentation
- Tool count claim needs context (internal vs external tools)

## Evidence Source

- Internal architecture design documents (confidential)
- RAG evaluation benchmark results (confidential)
- Customer feedback reports (confidential)
