<!--
Sync Impact Report
==================
Version change: template -> 1.0.0 (MAJOR: Initial constitution creation)
Added sections: Core Principles (7), Additional Constraints, Development Workflow, Governance
Removed sections: None (template placeholders replaced)
Templates requiring updates: 
  - plan-template.md: Constitution Check section aligns with new principles
  - spec-template.md: Mandatory sections align with governance requirements
  - tasks-template.md: Task categorization reflects principle-driven types (metadata, lineage, testing)
Follow-up TODOs: None
-->

# DataTrace Constitution

## Core Principles

### I. Metadata-First (NON-NEGOTIABLE)
Every data asset MUST have complete, accurate metadata including: owner, description, schema, data type, freshness expectations, and classification level. Metadata MUST be machine-readable and stored alongside the asset. Rationale: Without metadata, lineage is meaningless and discovery is impossible.

### II. End-to-End Lineage
DataTrace MUST track every table from BigQuery source through dbt transformation layers to Power BI semantic model. Each transformation MUST document: source tables, SQL logic, dbt model dependencies, and output schema. Gaps in lineage are considered critical bugs.

### III. dbt-Centric Transformations
All data transformations MUST be implemented and managed through dbt. Direct SQL in BigQuery outside dbt models is prohibited for production pipelines. Rationale: dbt provides the dependency graph, documentation, and testing framework required for reliable lineage.

### IV. BigQuery-Native Optimization
All models and queries MUST follow BigQuery best practices: partitioning on date/timestamp columns, clustering on high-cardinality filter columns, and materialization strategies appropriate to query patterns. Cost optimization MUST be a first-class concern in all data design decisions.

### V. Power BI Semantic Layer Integration
Every dbt mart table exposed to Power BI MUST have a corresponding semantic model with: clearly defined relationships, proper cardinality, documented measures, and lineage back to source. Semantic model changes MUST be versioned and communicated to consumers.

### VI. Automated Discovery with Manual Verification
Lineage MUST be auto-discovered from dbt manifests, BigQuery INFORMATION_SCHEMA, and Power BI metadata APIs. Auto-discovered lineage MUST be validated through manual review before being marked as production-ready. Rationale: Automation scales, but human verification ensures accuracy.

### VII. Test-Driven Data Quality
Every data model MUST have associated tests: schema validation, null checks, uniqueness constraints, referential integrity, and freshness monitoring. Tests MUST run in CI/CD pipeline and block merges on failure. Rationale: Untested data is unreliable data.

## Additional Constraints

**Technology Stack Requirements**
- Data Warehouse: BigQuery (primary, non-negotiable)
- Transformation: dbt Cloud or dbt Core (required for all production models)
- Visualization: Power BI with Premium capacity recommended
- Metadata Storage: BigQuery tables with dbt docs integration
- Orchestration: Airflow, Dagster, or Cloud Composer for production pipelines

**Compliance Standards**
- All PII/PDS fields MUST be classified and masked in development environments
- Data retention policies MUST be enforced at the dataset level
- Access controls MUST follow principle of least privilege
- Audit logging MUST capture all schema changes and data access

## Development Workflow

**Code Review Requirements**
- Every PR MUST include: updated dbt documentation, lineage impact assessment, cost analysis for new queries
- Two approvals required: one data engineer, one data analyst/consumer
- Lineage diagrams MUST be updated and linked in PR description for any model changes

**Testing Gates**
- Unit tests: dbt tests for all models (required)
- Integration tests: Cross-model validations in staging environment (required for production)
- End-to-end tests: Full pipeline runs with sample data (required before merge to main)
- Performance tests: Query cost and execution time benchmarks (required for large models)

**Deployment Approval Process**
- Staging deployment: Automatic on PR merge
- Production deployment: Requires tagged release and change approval board sign-off
- Breaking changes: Require migration plan and consumer notification 14 days in advance
- Rollback procedure: MUST be documented for every production change

## Governance

Constitution supersedes all other practices and documentation. All development MUST comply with these principles.

**Amendment Procedure**
- Proposals: Submit as GitHub Issues with "constitution-amendment" label
- Review: Minimum 7-day discussion period with core team
- Approval: Requires 2/3 majority vote of maintainers
- Documentation: All amendments MUST include rationale, impact assessment, and migration plan

**Versioning Policy**
- MAJOR: Backward incompatible governance/principle removals or redefinitions
- MINOR: New principle/section added or materially expanded guidance
- PATCH: Clarifications, wording improvements, non-semantic refinements
- All changes MUST be documented in constitution file header with Sync Impact Report

**Compliance Review Expectations**
- All PRs/reviews MUST verify compliance with constitution principles
- Complexity MUST be justified with reference to specific principles it serves
- Use constitution.md as the source of truth for all governance decisions

**Version**: 1.0.0 | **Ratified**: 2026-06-30 | **Last Amended**: 2026-06-30
