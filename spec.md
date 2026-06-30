# Feature Specification: DataTrace Core Implementation

**Feature Branch**: `main`

**Created**: 2026-06-30

**Status**: Draft

**Input**: User description: "Implement DataTrace core system"

## User Scenarios & Testing *(mandatory)*

### Clarifications

#### Session 2026-06-30

- Q: how are we going to connect to Power BI api ? → A: Power BI REST API with Service Principal authentication

### User Story 1 - Metadata Discovery (Priority: P1)

As a data engineer, I want to automatically discover and catalog all metadata for BigQuery tables so that I can understand what data assets exist and their characteristics.

**Why this priority**: Metadata is the foundation for all other DataTrace functionality. Without it, lineage and discovery are impossible.

**Independent Test**: Can be tested by running metadata discovery on a sample BigQuery dataset and verifying that all tables have complete metadata including owner, description, schema, data type, freshness expectations, and classification level.

**Acceptance Scenarios**:

1. **Given** a BigQuery dataset, **When** metadata discovery runs, **Then** all tables are cataloged with complete metadata
2. **Given** a table with missing metadata, **When** discovery runs, **Then** the system flags it as incomplete
3. **Given** a new table added to BigQuery, **When** discovery runs again, **Then** the new table is automatically cataloged

---

### User Story 2 - Lineage Tracking (Priority: P1)

As a data analyst, I want to trace the lineage of any table from BigQuery source through dbt transformations to Power BI semantic model so that I can understand where data comes from and how it's transformed.

**Why this priority**: Lineage is critical for understanding data provenance, impact analysis, and debugging.

**Independent Test**: Can be tested by creating a sample dbt project with transformations and verifying that lineage can be traced from source to final output.

**Acceptance Scenarios**:

1. **Given** a dbt model, **When** I view its lineage, **Then** I see all source tables, SQL logic, dbt model dependencies, and output schema
2. **Given** a Power BI semantic model, **When** I view its lineage, **Then** I see the dbt mart tables it depends on
3. **Given** a source table, **When** I view its downstream impact, **Then** I see all models and semantic models that depend on it

---

### User Story 3 - dbt Integration (Priority: P1)

As a data engineer, I want all transformations to be managed through dbt so that I can leverage dbt's dependency graph, documentation, and testing framework.

**Why this priority**: dbt is the required transformation tool per the constitution.

**Independent Test**: Can be tested by creating dbt models and verifying they are automatically discovered and integrated into the lineage graph.

**Acceptance Scenarios**:

1. **Given** a dbt project, **When** it's connected to DataTrace, **Then** all models are discovered and their dependencies are mapped
2. **Given** a new dbt model, **When** it's added, **Then** it automatically appears in the lineage graph
3. **Given** a dbt model with documentation, **When** it's discovered, **Then** the documentation is stored as metadata

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST automatically discover metadata for all BigQuery tables including owner, description, schema, data type, freshness expectations, and classification level
- **FR-002**: System MUST track lineage from BigQuery source through dbt transformation layers to Power BI semantic model
- **FR-003**: System MUST integrate with dbt to extract model dependencies, SQL logic, and output schemas
- **FR-004**: System MUST integrate with Power BI metadata APIs to extract semantic model information
- **FR-005**: System MUST provide automated discovery from dbt manifests, BigQuery INFORMATION_SCHEMA, and Power BI metadata APIs
- **FR-006**: System MUST support manual verification and approval workflow for discovered lineage
- **FR-007**: System MUST validate that all PII/PDS fields are classified and masked in development environments
- **FR-008**: System MUST enforce data retention policies at the dataset level
- **FR-009**: System MUST implement access controls following principle of least privilege
- **FR-010**: System MUST capture audit logging for all schema changes and data access

### Key Entities *(include if feature involves data)*

- **Metadata**: Stores information about data assets including owner, description, schema, data type, freshness expectations, and classification level
- **Lineage**: Tracks the flow of data from source to consumption, including transformations and dependencies
- **dbt Model**: Represents a dbt model with its SQL, dependencies, and output schema
- **Power BI Semantic Model**: Represents a Power BI semantic model with its relationships, cardinality, measures, and lineage
- **Data Asset**: A generic entity representing any data source, transformation, or destination

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of BigQuery tables have complete metadata cataloged
- **SC-002**: 100% of dbt models have lineage tracked from source to output
- **SC-003**: 100% of Power BI semantic models have lineage back to source tables
- **SC-004**: Manual verification completed for 100% of production lineage
- **SC-005**: All PII/PDS fields are classified and masked in development
- **SC-006**: Zero unauthorized access to data assets
- **SC-007**: All schema changes and data access events are logged

## Assumptions

- BigQuery is the primary data warehouse
- dbt Cloud or dbt Core is used for all production transformations
- Power BI with Premium capacity is used for visualization
- Power BI connection uses REST API with Service Principal authentication via MSAL
- Metadata is stored in BigQuery tables with dbt docs integration
- Airflow, Dagster, or Cloud Composer is used for orchestration
- All production models are implemented in dbt
- All direct SQL in BigQuery outside dbt is for non-production use only
