# Backend / Platform Engineer Resume Rubric

Additional rubric items for backend, platform, and developer productivity engineering roles.

## Scoring Dimensions (additive to tech-resume-rubric)

### Service / API Design (weight: 15%)
- 0: No API or service design mentioned
- 1: "Designed REST APIs" without specifics
- 2: States API surface, protocol, or schema
- 3: Describes design rationale, versioning, backward compatibility
- 4: Evidence of API governance, SDK generation, consumer feedback loops

### Data Modeling & Persistence (weight: 10%)
- 0: No data layer mentioned
- 1: Lists database names
- 2: States data model entities/relationships
- 3: Describes schema evolution, migration, indexing strategy
- 4: Evidence of performance optimization, sharding, multi-tenancy isolation

### Platform / Infrastructure (weight: 15%)
- 0: No infra context
- 1: "Used Kubernetes/Docker"
- 2: Describes deployment topology
- 3: Describes scaling, resource management, CI/CD pipeline design
- 4: Evidence of platform building (not just using), internal tool adoption, developer productivity impact

### Reliability & Observability (weight: 15%)
- 0: No reliability context
- 1: "Added monitoring"
- 2: Mentions specific metrics, dashboards, or alert rules
- 3: Describes SLO definition, incident response process, postmortem culture
- 4: Evidence of reliability improvement (MTTR reduction, error budget management)

### System Design & Trade-offs (weight: 15%)
- 0: No system design context
- 1: "Built a service"
- 2: Mentions architecture choices
- 3: Describes alternatives considered and trade-off rationale
- 4: Evidence of cross-team design review, RFC process, migration from legacy

## Role-Specific Red Flags

- Too many "used X tool" bullets without "built/changed/improved" context
- Presenting platform usage as platform building
- No mention of failure modes, debugging, or production incidents
- SRE/DevOps role without on-call or incident response mention
- Backend role without data consistency or transaction boundary discussion
- Developer productivity role without before/after workflow improvement evidence
- "Improved performance X%" without methodology, baseline, or measurement window
- "Migrated from A to B" without migration strategy, downtime, or rollback plan

## Resume Emphasis Priority

1. System ownership and architectural decisions (highest weight)
2. Production reliability and observability
3. API/service design and evolution
4. Performance optimization with methodology
5. Developer tooling or platform impact with adoption metrics
6. Collaboration and cross-team design review
7. Technology stack listing (lowest weight, supporting only)
