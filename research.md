# Research: DataTrace Core Implementation

**Date**: 2026-06-30 | **Feature**: DataTrace Core Implementation | **Status**: Complete

## Research Areas

### 1. BigQuery Metadata Discovery

**Decision**: Use BigQuery INFORMATION_SCHEMA views combined with custom metadata tables

**Rationale**: 
- INFORMATION_SCHEMA provides comprehensive metadata about tables, columns, routines, and jobs
- INFORMATION_SCHEMA.TABLES, INFORMATION_SCHEMA.COLUMNS, and INFORMATION_SCHEMA.TABLE_STORAGE provide the foundation
- Custom metadata tables in BigQuery will store DataTrace-specific metadata (owner, freshness expectations, classification level)
- This approach is cost-effective as it uses existing BigQuery infrastructure

**Alternatives considered**:
- Google Cloud Data Catalog: More comprehensive but adds complexity and cost
- Third-party metadata tools (Collibra, Alation): Too expensive and heavy for initial implementation
- Custom database for metadata: Adds infrastructure complexity

**Key findings**:
- INFORMATION_SCHEMA views are read-only and automatically updated
- TABLE_STORAGE view provides storage usage which is critical for cost optimization
- Custom metadata can be stored in a dedicated dataset (e.g., `datatrace_metadata`)

---

### 2. dbt Integration and Manifest Parsing

**Decision**: Use dbt Artifacts API and local manifest parsing

**Rationale**:
- dbt manifest.json contains complete dependency graph and model metadata
- dbt Artifacts API (dbt Cloud) or local manifest files (dbt Core) provide access to this data
- Parsing the manifest.json gives us: model names, dependencies, SQL, schema, tests, documentation
- This is the most reliable way to get dbt model lineage

**Alternatives considered**:
- dbt docs JSON: Similar information but less structured for programmatic access
- dbt metadata database: Requires additional dbt configuration
- Custom dbt macros: Would require modifying dbt projects

**Key findings**:
- manifest.json is generated after `dbt compile` or `dbt run`
- The `child_map` and `parent_map` in manifest.json provide the dependency graph
- Model `meta` section can store custom metadata that DataTrace can leverage
- dbt Cloud Artifacts API endpoint: `https://cloud.getdbt.com/api/v2/accounts/{account_id}/projects/{project_id}/artifacts/`

---

### 3. Power BI Metadata API

**Decision**: Use Power BI REST API for semantic model metadata extraction

**Rationale**:
- Power BI provides REST APIs to extract workspace, dataset, and semantic model information
- Semantic models (formerly datasets) expose tables, columns, relationships, and measures
- The API provides lineage information for Power BI-to-dbt connections
- OAuth 2.0 authentication with service principal recommended for automation

**Alternatives considered**:
- Power BI XMLA endpoint: More detailed but complex to parse
- Power BI Premium capacity APIs: Only available for Premium workspaces
- Manual export from Power BI Desktop: Not scalable

**Key findings**:
- Key API endpoints:
  - `https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets` - List datasets
  - `https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/tables` - Get tables
  - `https://api.powerbi.com/v1.0/myorg/groups/{group_id}/datasets/{dataset_id}/ExecuteQueries` - Run DAX queries
- Service principal authentication requires Azure AD app registration
- API rate limits: 60 requests per minute per user

---

### 4. Lineage Graph Storage

**Decision**: Use BigQuery tables with adjacency list pattern for lineage graph

**Rationale**:
- BigQuery can efficiently store and query large graph structures using adjacency lists
- Each edge in the graph is a row: {source, target, relationship_type, metadata}
- Graph queries can use recursive CTEs (WITH RECURSIVE) in BigQuery SQL
- This approach leverages existing BigQuery infrastructure and cost model

**Alternatives considered**:
- Neo4j: Purpose-built for graphs but adds infrastructure complexity
- NetworkX (in-memory Python): Doesn't scale to 10k+ nodes
- Property Graph in BigQuery: Newer feature, less mature
- Apache TinkerPop: Overkill for this use case

**Key findings**:
- Adjacency list pattern works well for DAGs (Directed Acyclic Graphs) which is the nature of data lineage
- Recursive queries in BigQuery can traverse the graph efficiently
- Materialized paths can be pre-computed for faster lineage queries
- Graph can be partitioned by source system (BigQuery, dbt, Power BI) for better performance

---

### 5. Cost Optimization for BigQuery

**Decision**: Implement query optimization patterns and cost monitoring

**Rationale**:
- BigQuery costs are based on data scanned, so query efficiency is critical
- Partition pruning and cluster filtering are the most effective cost reducers
- Materialized views can pre-compute expensive lineage traversals

**Key optimization patterns**:
- **Partitioning**: All metadata tables partitioned by date (creation/modification date)
- **Clustering**: Lineage tables clustered by source and target for common query patterns
- **Materialized views**: Pre-compute common lineage paths (source-to-target)
- **Query caching**: Leverage BigQuery's built-in caching for repeated queries
- **Cost estimation**: Use BigQuery dry-run to estimate costs before execution

**Cost monitoring**:
- Track data scanned per query
- Set up alerts for queries exceeding cost thresholds
- Monthly cost reports by feature/user

---

### 6. PII/PDS Classification and Masking

**Decision**: Use BigQuery data classification with custom tagging and dynamic data masking

**Rationale**:
- BigQuery Data Loss Prevention (DLP) API can automatically classify sensitive data
- Custom data classification tags can be applied to columns
- Dynamic data masking can be implemented using BigQuery views and authorized views
- This approach integrates well with existing BigQuery security features

**Alternatives considered**:
- Third-party data masking tools: Expensive and complex
- Application-level masking: Would require proxy layer for all queries
- Column-level security in Power BI: Only masks in Power BI, not in BigQuery

**Key findings**:
- BigQuery DLP API can detect: credit card numbers, email addresses, phone numbers, SSNs, etc.
- Classification can be automated with scheduled jobs
- Masking can be implemented using:
  - Views that replace sensitive values with masking patterns
  - Authorized views that restrict access to masked versions
  - Row-level security (RLS) for development environments

---

### 7. Orchestration (Airflow/Dagster/Cloud Composer)

**Decision**: Support multiple orchestrators with pluggable architecture

**Rationale**:
- Different teams may use different orchestration tools
- Pluggable architecture allows DataTrace to work with any orchestrator
- Initial implementation will focus on Airflow and Cloud Composer (managed Airflow)

**Key integration patterns**:
- **Airflow/Cloud Composer**: Use Airflow operators to trigger DataTrace jobs
- **Dagster**: Use Dagster resources and ops
- **Custom scripts**: CLI-based integration for flexibility

**Recommended approach**:
- Provide Docker container for DataTrace
- Publish Airflow DAGs and Dagster pipelines as examples
- REST API for programmatic triggering

---

## Technology Choices Summary

| Component | Choice | Rationale |
|-----------|--------|-----------|
| **Language** | Python 3.11+ | Rich ecosystem for data engineering, good BigQuery/dbt support |
| **Web Framework** | FastAPI | Modern, async, OpenAPI support, good performance |
| **BigQuery Client** | google-cloud-bigquery | Official Google SDK, well-maintained |
| **dbt Integration** | dbt-core + dbt-adapters | Direct access to dbt internals |
| **Power BI Client** | msal + requests | Standard OAuth2 flow with REST API |
| **Database** | BigQuery | Already required, scalable, cost-effective |
| **Testing** | pytest + dbt tests | Industry standard, good CI/CD integration |
| **Packaging** | Poetry | Modern dependency management, good for libraries |
| **Deployment** | Docker + Kubernetes | Portable, scalable, industry standard |

---

## Architecture Decisions

### ADR-001: Metadata Storage in BigQuery

**Status**: Accepted

**Context**: Need to store metadata about data assets (tables, columns, models, etc.)

**Decision**: Store all DataTrace metadata in a dedicated BigQuery dataset

**Consequences**:
- **Pros**: No additional infrastructure, leverages existing BigQuery scalability and security, cost-effective
- **Cons**: Metadata queries compete with analytics queries for resources, need to manage schema carefully

**Mitigation**: Use separate dataset with appropriate partitioning and clustering

### ADR-002: Lineage Graph Representation

**Status**: Accepted

**Context**: Need to represent and query complex lineage graphs efficiently

**Decision**: Use adjacency list pattern in BigQuery tables

**Consequences**:
- **Pros**: Simple to implement, works at scale, can use recursive queries
- **Cons**: Some graph queries may be slower than graph databases

**Mitigation**: Pre-compute common paths, use materialized views

### ADR-003: dbt-Centric Design

**Status**: Accepted (Constitution Requirement)

**Context**: Constitution mandates all production transformations in dbt

**Decision**: DataTrace will only track and manage dbt-based transformations

**Consequences**:
- **Pros**: Consistent, reliable lineage from dbt manifests
- **Cons**: Cannot track non-dbt transformations (direct SQL, stored procedures)

**Mitigation**: Flag non-dbt transformations as "external" and document limitations

---

## Open Questions

None - All critical design decisions have been resolved through research.

## Next Steps

Proceed to Phase 1: Design & Contracts
- Generate data-model.md from entities in spec
- Define interface contracts in /contracts/
- Create quickstart.md validation guide
- Update agent context
