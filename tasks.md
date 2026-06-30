---

description: "Task list for DataTrace Core Implementation feature"
---

# Tasks: DataTrace Core Implementation

**Input**: Design documents from `/specs/DataTrace Core Implementation/`

**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL - only include them if explicitly requested in the feature specification. This feature does not explicitly request TDD, so tests are minimal.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

**Format**: `[ID] [P?] [Story] Description with file path`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

Single project structure at repository root:
- `src/` - Core application code
- `tests/` - Test code
- `contracts/` - Interface contracts
- `metadata/` - DataTrace metadata storage (BigQuery)

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for DataTrace Core Implementation

- [X] T001 Create Python project structure per implementation plan in plan.md
- [X] T002 Initialize Python 3.11+ project with Poetry dependency management
- [X] T003 Add core dependencies: google-cloud-bigquery, dbt-core, msal, fastapi, pydantic, pytest
- [X] T004 [P] Configure linting with ruff and formatting with black
- [X] T005 [P] Setup pre-commit hooks for code quality
- [X] T006 Create src/ directory with __init__.py files
- [X] T007 Create tests/ directory with __init__.py files
- [X] T008 Create configuration directory structure at src/config/

**Checkpoint**: Project structure ready for code implementation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T009 Create base DataAsset model in src/models/data_asset.py (from data-model.md)
- [X] T010 Create Metadata model in src/models/metadata.py (from data-model.md)
- [X] T011 Create LineageEdge model in src/models/lineage.py (from data-model.md)
- [X] T012 [P] Create BigQuery-specific models in src/models/bigquery.py (BigQueryTable, BigQueryColumn)
- [X] T013 [P] Create dbt-specific models in src/models/dbt.py (dbtModel, dbtSource)
- [X] T014 [P] Create PowerBI-specific models in src/models/powerbi.py (PowerBISemanticModel, PowerBITable, PowerBIRelationship)
- [X] T015 [P] Create ClassificationTag model in src/models/classification.py
- [X] T016 Setup SQLAlchemy or Pydantic base models for all data entities
- [X] T017 [P] Create database/BigQuery connection utilities in src/lib/bigquery_client.py
- [X] T018 [P] Create configuration management in src/config/settings.py
- [X] T019 Create error handling framework and custom exceptions in src/lib/exceptions.py
- [X] T020 Create logging configuration in src/config/logging.py
- [X] T021 Setup environment variable management for all integrations
- [X] T022 [P] Create utility functions in src/lib/utils.py (JSON parsing, UUID generation, etc.)
- [X] T023 Create base repository/DAO pattern in src/core/repository.py for data access

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Metadata Discovery (Priority: P1) 🎯 MVP

**Goal**: As a data engineer, I want to automatically discover and catalog all metadata for BigQuery tables so that I can understand what data assets exist and their characteristics.

**Independent Test**: Can be tested by running metadata discovery on a sample BigQuery dataset and verifying that all tables have complete metadata including owner, description, schema, data type, freshness expectations, and classification level.

### Implementation for User Story 1

- [ ] T024 [P] [US1] Create BigQueryMetadataService in src/services/bigquery_metadata.py
- [ ] T025 [P] [US1] Create MetadataDiscoveryService in src/core/metadata/discovery.py
- [ ] T026 [P] [US1] Create INFORMATION_SCHEMA query builder in src/core/metadata/queries.py
- [ ] T027 [US1] Implement table discovery from BigQuery INFORMATION_SCHEMA.TABLES in src/core/metadata/discovery.py
- [ ] T028 [US1] Implement column discovery from BigQuery INFORMATION_SCHEMA.COLUMNS in src/core/metadata/discovery.py
- [ ] T029 [US1] Implement storage info discovery from BigQuery INFORMATION_SCHEMA.TABLE_STORAGE in src/core/metadata/discovery.py
- [ ] T030 [US1] Implement metadata cataloging service in src/core/metadata/catalog.py
- [ ] T031 [US1] Create metadata storage adapter for BigQuery in src/core/metadata/storage.py
- [ ] T032 [US1] Implement DataTrace metadata tables creation in metadata/catalog/ (BigQuery DDL)
- [ ] T033 [US1] Add validation for metadata completeness in src/core/metadata/validation.py
- [ ] T034 [US1] Implement metadata refresh/sync mechanism in src/core/metadata/sync.py
- [ ] T035 [US1] Create CLI command for metadata discovery in src/cli/commands/metadata.py
- [ ] T036 [US1] Add metadata discovery API endpoint GET /assets in src/api/endpoints/assets.py (from api-contract.md)
- [ ] T037 [US1] Add metadata retrieval API endpoint GET /assets/{asset_id}/metadata in src/api/endpoints/metadata.py (from api-contract.md)
- [ ] T038 [US1] Add metadata update API endpoint PUT /assets/{asset_id}/metadata/{key} in src/api/endpoints/metadata.py (from api-contract.md)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Metadata can be discovered from BigQuery and cataloged in DataTrace.

---

## Phase 4: User Story 2 - Lineage Tracking (Priority: P1)

**Goal**: As a data analyst, I want to trace the lineage of any table from BigQuery source through dbt transformations to Power BI semantic model so that I can understand where data comes from and how it's transformed.

**Independent Test**: Can be tested by creating a sample dbt project with transformations and verifying that lineage can be traced from source to final output.

### Implementation for User Story 2

- [ ] T039 [P] [US2] Create LineageService in src/core/lineage/service.py
- [ ] T040 [P] [US2] Create LineageGraphBuilder in src/core/lineage/graph.py
- [ ] T041 [P] [US2] Create LineageStorage in src/core/lineage/storage.py
- [ ] T042 [US2] Implement lineage edge creation and management in src/core/lineage/service.py
- [ ] T043 [US2] Implement graph traversal algorithms (BFS, DFS) in src/core/lineage/graph.py
- [ ] T044 [US2] Implement recursive CTE query support for lineage in src/core/lineage/queries.py
- [ ] T045 [US2] Create lineage materialized path pre-computation in src/core/lineage/materialized.py
- [ ] T046 [US2] Implement lineage verification workflow in src/core/lineage/verification.py
- [ ] T047 [US2] Add verification status tracking to LineageEdge model
- [ ] T048 [US2] Create lineage visualization service in src/core/lineage/visualization.py
- [ ] T049 [US2] Create CLI command for lineage graph in src/cli/commands/lineage.py
- [ ] T050 [US2] Add lineage graph API endpoint GET /lineage/graph in src/api/endpoints/lineage.py (from api-contract.md)
- [ ] T051 [US2] Add lineage impact analysis endpoint GET /lineage/impact in src/api/endpoints/lineage.py (from api-contract.md)
- [ ] T052 [US2] Add lineage path finding endpoint GET /lineage/path in src/api/endpoints/lineage.py (from api-contract.md)
- [ ] T053 [US2] Add lineage verification API endpoints in src/api/endpoints/verification.py (from api-contract.md)

**Checkpoint**: At this point, User Story 2 should be fully functional and testable independently. Lineage can be traced from BigQuery through dbt to Power BI.

---

## Phase 5: User Story 3 - dbt Integration (Priority: P1)

**Goal**: As a data engineer, I want all transformations to be managed through dbt so that I can leverage dbt's dependency graph, documentation, and testing framework.

**Independent Test**: Can be tested by creating dbt models and verifying they are automatically discovered and integrated into the lineage graph.

### Implementation for User Story 3

- [ ] T054 [P] [US3] Create dbtProjectService in src/core/dbt/project.py
- [ ] T055 [P] [US3] Create dbtManifestParser in src/core/dbt/manifest.py
- [ ] T056 [P] [US3] Create dbtModelService in src/core/dbt/models.py
- [ ] T057 [US3] Implement manifest.json parsing in src/core/dbt/manifest.py
- [ ] T058 [US3] Implement dbt model extraction from manifest in src/core/dbt/models.py
- [ ] T059 [US3] Implement dbt source extraction from manifest in src/core/dbt/sources.py
- [ ] T060 [US3] Implement dbt dependency graph extraction in src/core/dbt/dependencies.py
- [ ] T061 [US3] Create dbt artifact caching mechanism in src/core/dbt/cache.py
- [ ] T062 [US3] Implement dbt model to DataAsset mapping in src/core/dbt/mapping.py
- [ ] T063 [US3] Implement dbt lineage integration with LineageService in src/core/dbt/lineage_integration.py
- [ ] T064 [US3] Create CLI command for dbt discovery in src/cli/commands/dbt.py
- [ ] T065 [US3] Implement dbt Cloud API integration in src/core/dbt/cloud.py
- [ ] T066 [US3] Add dbt integration test endpoint POST /discovery/run in src/api/endpoints/discovery.py (from api-contract.md)
- [ ] T067 [US3] Add dbt discovery status endpoint GET /discovery/{discovery_id}/status in src/api/endpoints/discovery.py (from api-contract.md)

**Checkpoint**: At this point, User Story 3 should be fully functional and testable independently. dbt models are automatically discovered and integrated into the lineage graph.

---

## Phase 6: BigQuery Integration Deep Dive

**Goal**: Complete BigQuery integration with all features from bigquery-contract.md

**Independent Test**: Can be tested by running full BigQuery metadata discovery and verifying all tables, columns, and storage info is extracted.

### Implementation for BigQuery Integration

- [ ] T068 [P] [US1] Implement partition configuration parsing in src/core/bigquery/partitioning.py
- [ ] T069 [P] [US1] Implement clustering configuration parsing in src/core/bigquery/clustering.py
- [ ] T070 [US1] Add BigQuery routine (stored procedure/function) discovery in src/core/bigquery/routines.py
- [ ] T071 [US1] Add BigQuery job history discovery in src/core/bigquery/jobs.py
- [ ] T072 [US1] Implement BigQuery view definition parsing in src/core/bigquery/views.py
- [ ] T073 [US1] Add cost tracking for metadata queries in src/core/bigquery/cost.py
- [ ] T074 [US1] Implement rate limiting and backoff for BigQuery API in src/lib/bigquery_client.py
- [ ] T075 [US1] Add BigQuery IAM permission validation in src/core/bigquery/permissions.py

**Checkpoint**: BigQuery integration is complete with all metadata types supported.

---

## Phase 7: Power BI Integration

**Goal**: Complete Power BI integration for end-to-end lineage tracking

**Independent Test**: Can be tested by connecting to a Power BI workspace and verifying semantic models, tables, and relationships are extracted.

### Implementation for Power BI Integration

- [ ] T076 [P] [US2] Create PowerBIService in src/core/powerbi/service.py
- [ ] T077 [P] [US2] Create PowerBIConnection in src/core/powerbi/connection.py
- [ ] T078 [P] [US2] Implement Power BI REST API client in src/lib/powerbi_client.py
- [ ] T079 [US2] Implement workspace discovery in src/core/powerbi/workspaces.py
- [ ] T080 [US2] Implement semantic model (dataset) discovery in src/core/powerbi/datasets.py
- [ ] T081 [US2] Implement table discovery from semantic models in src/core/powerbi/tables.py
- [ ] T082 [US2] Implement relationship discovery from semantic models in src/core/powerbi/relationships.py
- [ ] T083 [US2] Implement measure discovery from semantic models in src/core/powerbi/measures.py
- [ ] T084 [US2] Implement column discovery from Power BI tables in src/core/powerbi/columns.py
- [ ] T085 [US2] Create Power BI to dbt lineage connector in src/core/powerbi/lineage.py
- [ ] T086 [US2] Implement Power BI refresh history tracking in src/core/powerbi/refresh.py
- [ ] T087 [US2] Add Power BI authentication with MSAL in src/lib/auth/powerbi.py
- [ ] T088 [US2] Implement Service Principal authentication flow in src/lib/auth/powerbi.py

**Checkpoint**: Power BI integration is complete. Lineage can be traced from BigQuery -> dbt -> Power BI.

---

## Phase 8: PII/PDS Classification and Masking

**Goal**: Implement PII/PDS classification and dynamic data masking as per constitution

**Independent Test**: Can be tested by running classification on sample datasets and verifying PII columns are identified and masked appropriately.

### Implementation for Classification

- [ ] T089 [P] [US1] Create ClassificationService in src/core/classification/service.py
- [ ] T090 [P] [US1] Implement BigQuery DLP API integration in src/lib/classification/dlp.py
- [ ] T091 [US1] Create PII detection patterns in src/core/classification/patterns.py
- [ ] T092 [US1] Implement column-level classification in src/core/classification/columns.py
- [ ] T093 [US1] Implement asset-level classification in src/core/classification/assets.py
- [ ] T094 [US1] Create masking pattern generator in src/core/classification/masking.py
- [ ] T095 [US1] Implement dynamic view generation for masked data in src/core/classification/views.py
- [ ] T096 [US1] Add classification to metadata extraction in src/core/metadata/discovery.py
- [ ] T097 [US1] Create classification tag management in src/core/classification/tags.py
- [ ] T098 [US1] Implement sensitivity level enforcement in src/core/classification/enforcement.py

**Checkpoint**: PII/PDS classification system is complete and integrated with metadata discovery.

---

## Phase 9: Discovery Orchestration

**Goal**: Implement automated discovery workflows that orchestrate BigQuery, dbt, and Power BI discovery

**Independent Test**: Can be tested by running full discovery and verifying all sources are processed correctly.

### Implementation for Discovery

- [ ] T099 [P] Create DiscoveryOrchestrator in src/core/discovery/orchestrator.py
- [ ] T100 [P] Create DiscoveryJob model in src/models/discovery.py
- [ ] T101 [P] Create DiscoveryResult model in src/models/discovery.py
- [ ] T102 [US1] Implement full discovery workflow in src/core/discovery/workflow.py
- [ ] T103 [US1] Implement incremental discovery in src/core/discovery/incremental.py
- [ ] T104 [US1] Create discovery job queue in src/core/discovery/queue.py
- [ ] T105 [US1] Implement discovery progress tracking in src/core/discovery/progress.py
- [ ] T106 [US1] Create discovery error handling in src/core/discovery/errors.py
- [ ] T107 [US1] Implement discovery scheduling in src/core/discovery/scheduler.py
- [ ] T108 [US1] Add discovery status API endpoints in src/api/endpoints/discovery.py (from api-contract.md)
- [ ] T109 [US1] Create CLI command for full discovery in src/cli/commands/discover.py

**Checkpoint**: Automated discovery workflow is complete and can process all source types.

---

## Phase 10: API Service Layer

**Goal**: Complete REST API implementation as per api-contract.md

**Independent Test**: Can be tested by starting the API server and validating all endpoints work correctly.

### Implementation for API

- [ ] T110 [P] Create FastAPI application factory in src/api/app.py
- [ ] T111 [P] Setup API middleware in src/api/middleware.py
- [ ] T112 [P] Implement authentication middleware in src/api/middleware/auth.py
- [ ] T113 [P] Create rate limiting in src/api/middleware/rate_limit.py
- [ ] T114 [P] Implement error handlers in src/api/handlers.py
- [ ] T115 [P] Create API schemas in src/api/schemas/assets.py
- [ ] T116 [P] Create API schemas in src/api/schemas/lineage.py
- [ ] T117 [P] Create API schemas in src/api/schemas/metadata.py
- [ ] T118 [P] Create API schemas in src/api/schemas/discovery.py
- [ ] T119 Complete assets API endpoints in src/api/endpoints/assets.py (from api-contract.md)
- [ ] T120 Complete lineage API endpoints in src/api/endpoints/lineage.py (from api-contract.md)
- [ ] T121 Complete verification API endpoints in src/api/endpoints/verification.py (from api-contract.md)
- [ ] T122 Implement health check endpoint in src/api/endpoints/health.py
- [ ] T123 Add OpenAPI/Swagger documentation to all endpoints
- [ ] T124 Implement API versioning support in src/api/versioning.py
- [ ] T125 Create API configuration in src/config/api.py

**Checkpoint**: REST API is complete with all endpoints from api-contract.md implemented and tested.

---

## Phase 11: CLI Interface

**Goal**: Complete CLI implementation as per cli-contract.md

**Independent Test**: Can be tested by running CLI commands and verifying they work as documented.

### Implementation for CLI

- [ ] T126 Create CLI main entry point in src/cli/main.py
- [ ] T127 Create CLI argument parser in src/cli/parser.py
- [ ] T128 [P] Implement configure command group in src/cli/commands/configure.py
- [ ] T129 [P] Implement discover command group in src/cli/commands/discover.py
- [ ] T130 [P] Implement lineage command group in src/cli/commands/lineage.py
- [ ] T131 [P] Implement metadata command group in src/cli/commands/metadata.py
- [ ] T132 [P] Implement assets command group in src/cli/commands/assets.py
- [ ] T133 [P] Implement verify command group in src/cli/commands/verify.py
- [ ] T134 [P] Implement server command in src/cli/commands/server.py
- [ ] T135 Create CLI output formatters in src/cli/formatters.py
- [ ] T136 Implement JSON, YAML, and table output formats in src/cli/formatters/
- [ ] T137 Add Graphviz output for lineage in src/cli/formatters/graphviz.py
- [ ] T138 Create CLI configuration management in src/cli/config.py
- [ ] T139 Implement CLI error handling and exit codes in src/cli/errors.py
- [ ] T140 Add CLI help and documentation generation in src/cli/help.py

**Checkpoint**: CLI is complete with all commands from cli-contract.md implemented.

---

## Phase 12: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T141 [P] Add comprehensive documentation in docs/
- [ ] T142 [P] Create README.md with setup and usage instructions
- [ ] T143 [P] Add contribution guidelines in CONTRIBUTING.md
- [ ] T144 Code cleanup and refactoring for consistency
- [ ] T145 [P] Add additional unit tests in tests/unit/ for core functionality
- [ ] T146 [P] Add integration tests in tests/integration/ for key workflows
- [ ] T147 Implement performance optimization for lineage queries
- [ ] T148 Add query caching for BigQuery metadata in src/lib/cache.py
- [ ] T149 [P] Implement security hardening across all components
- [ ] T150 Run quickstart.md validation scenarios and verify all pass
- [ ] T151 [P] Add Docker container support with Dockerfile
- [ ] T152 [P] Create docker-compose.yml for local development
- [ ] T153 [P] Add Kubernetes manifests for deployment in k8s/
- [ ] T154 Implement comprehensive logging across all modules
- [ ] T155 Add metrics and monitoring endpoints in src/api/endpoints/metrics.py

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (Phase 4)**: Depends on Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (Phase 5)**: Depends on Foundational (Phase 2) - No dependencies on other stories
- **BigQuery Integration (Phase 6)**: Depends on User Story 1 (Phase 3)
- **Power BI Integration (Phase 7)**: Depends on User Story 2 (Phase 4)
- **Classification (Phase 8)**: Depends on User Story 1 (Phase 3)
- **Discovery Orchestration (Phase 9)**: Depends on Phases 3, 4, 5, 6, 7, 8
- **API Service Layer (Phase 10)**: Depends on Phases 3, 4, 5, 6, 7, 8, 9
- **CLI Interface (Phase 11)**: Depends on Phases 3, 4, 5, 6, 7, 8, 9, 10
- **Polish (Phase 12)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (Metadata Discovery)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (Lineage Tracking)**: Can start after Foundational (Phase 2) - Integrates with US1 but should be independently testable
- **User Story 3 (dbt Integration)**: Can start after Foundational (Phase 2) - Integrates with US1/US2 but should be independently testable

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, User Stories 1, 2, and 3 can all start in parallel (if team capacity allows)
- All parallel tasks within a story can run concurrently
- Different user stories can be worked on in parallel by different team members
- BigQuery, Power BI, and Classification phases can run in parallel once their respective dependencies are met
- API Service Layer and CLI Interface phases can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all models for User Story 1 together:
Task: "T024 Create BigQueryMetadataService in src/services/bigquery_metadata.py"
Task: "T025 Create MetadataDiscoveryService in src/core/metadata/discovery.py"
Task: "T026 Create INFORMATION_SCHEMA query builder in src/core/metadata/queries.py"
Task: "T027 Implement table discovery from BigQuery INFORMATION_SCHEMA.TABLES"

# Launch all API endpoints for User Story 1 together:
Task: "T036 Add metadata discovery API endpoint GET /assets"
Task: "T037 Add metadata retrieval API endpoint GET /assets/{asset_id}/metadata"
Task: "T038 Add metadata update API endpoint PUT /assets/{asset_id}/metadata/{key}"
```

## Parallel Example: All User Stories (After Foundational Phase)

```bash
# Team with 3 developers can work on all user stories in parallel:

# Developer 1 - User Story 1 (Metadata Discovery):
Task: "T024 Create BigQueryMetadataService in src/services/bigquery_metadata.py"
Task: "T025 Create MetadataDiscoveryService in src/core/metadata/discovery.py"
Task: "T026 Create INFORMATION_SCHEMA query builder in src/core/metadata/queries.py"
...

# Developer 2 - User Story 2 (Lineage Tracking):
Task: "T039 Create LineageService in src/core/lineage/service.py"
Task: "T040 Create LineageGraphBuilder in src/core/lineage/graph.py"
Task: "T041 Create LineageStorage in src/core/lineage/storage.py"
...

# Developer 3 - User Story 3 (dbt Integration):
Task: "T054 Create dbtProjectService in src/core/dbt/project.py"
Task: "T055 Create dbtManifestParser in src/core/dbt/manifest.py"
Task: "T056 Create dbtModelService in src/core/dbt/models.py"
...
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Metadata Discovery)
4. **STOP and VALIDATE**: Test User Story 1 independently with quickstart.md scenarios
5. Deploy/demo if ready

**MVP Scope**: Setup + Foundational + User Story 1 = Basic metadata discovery from BigQuery

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add BigQuery deep dive → Deploy/Demo
6. Add Power BI integration → Deploy/Demo
7. Add Classification → Deploy/Demo
8. Add Discovery Orchestration → Deploy/Demo
9. Add API Service Layer → Deploy/Demo
10. Add CLI Interface → Deploy/Demo
11. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. **Week 1**: Team completes Setup + Foundational together
2. **Week 2+**: Once Foundational is done:
   - Developer A: User Story 1 + BigQuery deep dive
   - Developer B: User Story 2 + Power BI integration
   - Developer C: User Story 3 + Classification
3. **Week 3+**: API Service Layer and CLI Interface can start
4. **Final Week**: Polish and cross-cutting concerns

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability (US1, US2, US3)
- Each user story should be independently completable and testable
- Verify tests fail before implementing (if tests included)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
- All tasks follow strict checklist format with ID, [P] marker, [Story] label, and file path

---

## Task Summary

**Total Tasks**: 155

**Tasks per Phase**:
- Phase 1 (Setup): 8 tasks
- Phase 2 (Foundational): 16 tasks
- Phase 3 (User Story 1 - Metadata Discovery): 14 tasks
- Phase 4 (User Story 2 - Lineage Tracking): 14 tasks
- Phase 5 (User Story 3 - dbt Integration): 14 tasks
- Phase 6 (BigQuery Integration Deep Dive): 8 tasks
- Phase 7 (Power BI Integration): 14 tasks
- Phase 8 (PII/PDS Classification): 10 tasks
- Phase 9 (Discovery Orchestration): 10 tasks
- Phase 10 (API Service Layer): 16 tasks
- Phase 11 (CLI Interface): 15 tasks
- Phase 12 (Polish): 15 tasks

**Parallel Opportunities**: 68 tasks marked [P] (44% of total)

**MVP Scope**: 46 tasks (Phases 1-3)

**Full Implementation**: 155 tasks

**Suggested First Delivery**: Complete Phases 1-3 (MVP) = 46 tasks

---

## File Path Summary

**Core Directories**:
- `src/` - 120+ tasks
  - `src/core/` - Metadata, Lineage, dbt, BigQuery, Power BI, Classification, Discovery
  - `src/models/` - Data models for all entities
  - `src/services/` - Business logic services
  - `src/api/` - REST API implementation
  - `src/cli/` - Command-line interface
  - `src/lib/` - Utility libraries
  - `src/config/` - Configuration management
- `tests/` - Test code (optional, minimal in this implementation)
- `contracts/` - Interface contracts (already created)
- `metadata/` - BigQuery metadata storage (DDL scripts)
- `docs/` - Documentation
- `k8s/` - Kubernetes manifests

**All tasks specify exact file paths for implementation.**
