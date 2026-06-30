# Implementation Plan: DataTrace Core Implementation

**Branch**: `main` | **Date**: 2026-06-30 | **Spec**: [spec.md](spec.md)

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

Implement the DataTrace core system for automated metadata discovery, end-to-end lineage tracking, and dbt integration. The system will automatically discover and catalog metadata for all BigQuery tables, track lineage from source through dbt transformations to Power BI semantic models, and enforce the constitution principles of metadata-first approach, dbt-centric transformations, and test-driven data quality.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.11+, dbt Core/Cloud, SQL (BigQuery)

**Primary Dependencies**: Google Cloud SDK (BigQuery), dbt Core/Cloud, Power BI REST API, Airflow/Dagster/Cloud Composer (orchestration)

**Storage**: BigQuery (primary data warehouse and metadata storage)

**Testing**: dbt tests (data model validation), pytest (application testing)

**Target Platform**: Google Cloud Platform (GCP)

**Project Type**: Data pipeline/lineage tracking system (CLI + web service)

**Performance Goals**: Cost optimization for BigQuery queries (<10TB/month), scalable to 10k+ tables, sub-second lineage query response times

**Constraints**: All production transformations MUST use dbt, all data assets MUST have complete metadata, PII/PDS fields MUST be classified and masked in development

**Scale/Scope**: Enterprise data warehouse with potentially thousands of tables, hundreds of dbt models, multiple Power BI semantic models

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Gates from DataTrace Constitution (v1.0.0)

- **GATE-001 Metadata-First (NON-NEGOTIABLE)**: PASS - All data assets will have complete metadata stored alongside the asset. The DataTrace system itself enforces this principle.

- **GATE-002 End-to-End Lineage**: PASS - The system will track every table from BigQuery source through dbt transformation layers to Power BI semantic model, documenting source tables, SQL logic, dbt model dependencies, and output schema.

- **GATE-003 dbt-Centric Transformations (NON-NEGOTIABLE)**: PASS - The system will only track dbt-based transformations. Direct SQL in BigQuery outside dbt models will be flagged as non-production.

- **GATE-004 BigQuery-Native Optimization**: PASS - The system will validate and enforce partitioning on date/timestamp columns, clustering on high-cardinality filter columns, and cost-optimized materialization strategies.

- **GATE-005 Power BI Semantic Layer Integration**: PASS - Every dbt mart table exposed to Power BI will have corresponding semantic model tracking with relationships, cardinality, and documented measures.

- **GATE-006 Automated Discovery with Manual Verification**: PASS - Lineage will be auto-discovered from dbt manifests, BigQuery INFORMATION_SCHEMA, and Power BI metadata APIs, with manual review workflow before production-readiness.

- **GATE-007 Test-Driven Data Quality**: PASS - All data models will have associated tests (schema validation, null checks, uniqueness constraints, referential integrity, freshness monitoring) that run in CI/CD.

- **GATE-008 Technology Stack Compliance**: PASS - Uses BigQuery (primary data warehouse), dbt Core/Cloud (transformations), Power BI (visualization), Airflow/Dagster/Cloud Composer (orchestration).

- **GATE-009 Compliance Standards**: PASS - Will implement PII/PDS classification and masking, data retention policies at dataset level, principle of least privilege access controls, and audit logging for all schema changes and data access.

**Result**: ALL GATES PASS - No violations detected. Proceeding to Phase 0 research.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
src/
├── core/                   # Core DataTrace functionality
│   ├── metadata/           # Metadata discovery and cataloging
│   ├── lineage/            # Lineage tracking and graph building
│   ├── dbt_integration/    # dbt manifest parsing and integration
│   ├── powerbi_integration/# Power BI metadata API integration
│   └── bigquery/           # BigQuery INFORMATION_SCHEMA integration
├── models/                 # Data models for DataTrace metadata
│   ├── metadata_models.py  # Metadata data models
│   ├── lineage_models.py   # Lineage data models
│   └── ...
├── services/               # Business logic services
│   ├── discovery_service.py
│   ├── lineage_service.py
│   └── ...
├── api/                    # Web service API (FastAPI/Flask)
│   ├── endpoints/
│   └── schemas/
├── cli/                    # Command-line interface
│   └── commands/
├── lib/                    # Shared utilities and helpers
│   ├── bigquery_client.py
│   ├── dbt_client.py
│   └── ...
└── config/                 # Configuration management

tests/
├── unit/                   # Unit tests
│   ├── test_metadata.py
│   ├── test_lineage.py
│   └── ...
├── integration/            # Integration tests
│   ├── test_dbt_integration.py
│   ├── test_bigquery_integration.py
│   └── ...
└── contract/               # Contract tests for API endpoints

metadata/                   # DataTrace metadata storage (BigQuery)
├── catalog/                # Metadata catalog tables
└── lineage/                # Lineage graph tables
```

**Structure Decision**: Single project structure with clear separation of concerns. The `src/` directory contains all core functionality organized by domain (metadata, lineage, integrations). The `tests/` directory mirrors the source structure with unit, integration, and contract tests. Metadata is stored in BigQuery tables under a dedicated schema.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| None | N/A | N/A |

**Result**: No complexity violations detected. All design decisions align with constitution principles.

---

## Post-Design Constitution Check

*GATE: Re-evaluate after Phase 1 design completion.*

### Post-Design Validation

All constitution gates have been re-validated against the completed design artifacts (data-model.md, contracts/, quickstart.md):

- **GATE-001 Metadata-First**: **STILL PASS** - Data model confirms all data assets have metadata. The `Metadata` entity enforces this with required fields for owner, classification, and sensitivity.

- **GATE-002 End-to-End Lineage**: **STILL PASS** - Data model includes `LineageEdge` entity with source/target relationships. Contracts define lineage query endpoints.

- **GATE-003 dbt-Centric Transformations**: **STILL PASS** - Data model includes specialized `dbtModel` and `dbtSource` entities. dbt contract defines integration approach.

- **GATE-004 BigQuery-Native Optimization**: **STILL PASS** - Data model captures partitioning/clustering in `BigQueryTable`. BigQuery contract defines optimization patterns.

- **GATE-005 Power BI Semantic Layer Integration**: **STILL PASS** - Data model includes `PowerBISemanticModel`, `PowerBITable`, `PowerBIRelationship`. Power BI contract defines integration.

- **GATE-006 Automated Discovery with Manual Verification**: **STILL PASS** - Data model includes `verification_status` field on `LineageEdge`. Quickstart defines verification workflow.

- **GATE-007 Test-Driven Data Quality**: **STILL PASS** - Data model includes `tests` field on `dbtModel`. Quickstart includes test scenarios.

- **GATE-008 Technology Stack Compliance**: **STILL PASS** - All contracts specify compliant technologies (BigQuery, dbt, Power BI).

- **GATE-009 Compliance Standards**: **STILL PASS** - Data model includes `ClassificationTag` entity for PII/PDS. Metadata includes security fields.

**Result**: ALL GATES STILL PASS - No violations detected after design. Ready for Phase 2 (implementation).
