## Metadata

- **Project**: Example Backend Platform
- **Role**: Backend Platform Engineer
- **Period**: 2022-03 — 2023-12
- **Team size**: 8 engineers
- **Personal ownership**: API gateway, observability platform

## One-line Summary

Built a high-throughput API gateway and observability platform for microservices architecture serving 100K+ RPS.

## Problem / Context

The monolithic backend could not handle growing traffic and deployment complexity. The team needed to migrate to microservices with a unified API gateway, service mesh, and observability stack while maintaining 99.9% availability.

## Technical Challenges

- Designing an API gateway handling 100K+ RPS with sub-10ms P99 latency
- Implementing distributed tracing across 50+ microservices
- Building auto-scaling infrastructure with cost optimization
- Migrating from monolith to microservices without downtime

## Architecture

- API gateway (Envoy-based) with rate limiting, authentication, and routing
- Service mesh with mutual TLS and traffic management
- Observability stack: OpenTelemetry collection, Prometheus metrics, Grafana dashboards
- CI/CD pipeline with ArgoCD for GitOps-based deployments

## Core Modules

- **Gateway**: Envoy-based API gateway with custom filters
- **Observability**: OpenTelemetry collector pipeline with trace aggregation
- **Auto-scaler**: Custom HPA controller with predictive scaling
- **Deployer**: ArgoCD-based GitOps pipeline with canary deployments

## Key Decisions / Trade-offs

- Chose Envoy over Nginx for better dynamic configuration and gRPC support
- Used OpenTelemetry over custom tracing for vendor neutrality
- Implemented canary deployments over blue-green for faster rollback
- Chose Kafka for event streaming over RabbitMQ for higher throughput

## Personal Contribution Candidates

- Designed the Envoy-based API gateway architecture
- Implemented the OpenTelemetry observability pipeline
- Built the custom auto-scaling controller
- Led the monolith-to-microservices migration for 3 core services

## Technologies

Go, Python, Kubernetes, Docker, Envoy, Kafka, Redis, PostgreSQL, OpenTelemetry, Prometheus, Grafana, Terraform, ArgoCD

## Keywords

backend, platform engineering, Kubernetes, Docker, Envoy, Kafka, Redis, OpenTelemetry, Terraform, ArgoCD, observability, Prometheus, Grafana, CI/CD

## Resume Bullets - zh-CN

- 设计并实现基于 Envoy 的 API 网关，支撑 100K+ RPS，P99 延迟 [TODO / 待补：毫秒数]
- 构建 OpenTelemetry 可观测管线，实现 50+ 微服务的分布式追踪和指标聚合
- 开发自定义 HPA 控制器，结合预测性扩缩容，资源利用率提升 [TODO / 待补：百分比]
- 主导 3 个核心服务从单体到微服务的迁移，零停机完成

## Resume Bullets - en-US

- Designed Envoy-based API gateway handling 100K+ RPS with [TODO / 待补：ms] P99 latency
- Built OpenTelemetry observability pipeline enabling distributed tracing and metrics aggregation across 50+ microservices
- Developed custom HPA controller with predictive scaling, improving resource utilization by [TODO / 待补：percentage]
- Led monolith-to-microservices migration for 3 core services with zero downtime

## Interview Pitch - zh-CN

### 60 秒版

我负责设计和实现后端平台的核心基础设施，包括 API 网关、可观测平台和自动扩缩容系统。平台支撑了 50+ 微服务、100K+ RPS 的流量，同时通过 GitOps 实现了可靠的持续部署。

### 3 分钟版

[在 60 秒版基础上展开] 网关选型方面，我们对比了 Nginx 和 Envoy，最终选择 Envoy 是因为它的动态配置能力和原生 gRPC 支持。可观测方面，我们用 OpenTelemetry 统一了追踪、指标和日志，避免了厂商锁定。扩缩容方面，标准 HPA 只能基于当前指标反应，我们加入了基于历史数据的预测性扩缩容，在流量高峰前提前扩容。

## Interview Pitch - en-US

### 60-second version

I designed and built core backend platform infrastructure including an API gateway, observability platform, and auto-scaling system. The platform supports 50+ microservices handling 100K+ RPS, with reliable continuous deployment through GitOps.

### 3-minute version

[Expanding on the 60-second version] For the gateway, we compared Nginx vs Envoy and chose Envoy for its dynamic configuration and native gRPC support. For observability, we unified tracing, metrics, and logs with OpenTelemetry to avoid vendor lock-in. For auto-scaling, standard HPA only reacts to current metrics; we added predictive scaling based on historical data to pre-scale before traffic peaks.

## Likely Interview Questions

1. How did you handle gateway configuration updates without dropping connections?
2. What was your trace sampling strategy at 100K RPS?
3. How did you ensure zero downtime during the monolith migration?
4. What was your canary deployment rollback criteria?
5. How did you manage Kafka consumer group rebalancing?

## Metrics To Confirm

- [ ] P99 latency of API gateway
- [ ] Resource utilization improvement percentage
- [ ] Number of microservices migrated
- [ ] Deployment frequency before/after
- [ ] Cost savings from predictive scaling

## Missing Information

- Exact P99 latency numbers
- Specific services migrated and their complexity
- Cost comparison before/after migration
- Team composition and personal contribution boundaries

## Red Flags / Risks

- "100K+ RPS" needs clarification on request size and complexity
- "Zero downtime" claim needs evidence of migration strategy
- Predictive scaling accuracy needs validation

## Evidence Source

- Internal architecture documents (confidential)
- Load test results (confidential)
- Incident reports and post-mortems (confidential)
