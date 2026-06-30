# Data Model: DataTrace Core Implementation

**Date**: 2026-06-30 | **Feature**: DataTrace Core Implementation | **Version**: 1.0.0

## Overview

The DataTrace data model represents the domain of data assets, their metadata, lineage relationships, and transformations. The model is designed to support the constitution principles of metadata-first approach, end-to-end lineage, and dbt-centric transformations.

## Entity Relationship Diagram (Conceptual)

```
┌─────────────────────────────────────────────────────────────────────┐
│                          DataTrace Data Model                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────┐       ┌──────────────┐       ┌──────────────┐    │
│  │ Data Asset   │       │  Metadata    │       │   Lineage    │    │
│  │              │       │              │       │   Edge       │    │
│  ├──────────────┤       ├──────────────┤       ├──────────────┤    │
│  │ id           │───┐   │ id           │       │ id           │    │
│  │ name         │   │   │ asset_id     │◄──────│ source_id    │    │
│  │ type         │   │   │ key          │   │   │ target_id    │    │
│  │ description  │   │   │ value        │   │   │ relationship │    │
│  │ source_type  │   │   │ classification│   │   │ metadata     │    │
│  │ connection   │   │   │ last_updated │       └──────────────┘    │
│  └──────────────┘   │   └──────────────┘                              │
│         │            │                                                  │
│         │ has        │                                                  │
│         ▼            │                                                  │
│  ┌──────────────┐   │                                                  │
│  │  dbt Model   │   │                                                  │
│  │              │   │                                                  │
│  ├──────────────┤   │                                                  │
│  │ id           │   │                                                  │
│  │ asset_id     │───────────────────────────── is a               │
│  │ model_name   │   │                                     │
│  │ sql          │   │                                     │
│  │ schema       │   │      ┌──────────────┐       ┌──────────────┐    │
│  │ dependencies │   │      │ PBI Semantic │       │ Classification│    │
│  │ config       │   │      │    Model      │       │    Tag        │    │
│  │ docs         │   │      │              │       │              │    │
│  │ tests        │   │      ├──────────────┤       ├──────────────┤    │
│  └──────────────┘   │      │ id           │       │ id           │    │
│         │            │      │ asset_id     │       │ column_id    │    │
│         │            │      │ dataset_name │       │ tag          │    │
│         │ is a       │      │ workspace    │       │ sensitivity  │    │
│         ▼            │      │ tables[]     │       │ mask_pattern │    │
│  ┌──────────────┐   │      │ relationships │       └──────────────┘    │
│  │ BigQuery     │   │      │ measures[]   │                              │
│  │   Table      │   │      └──────────────┘                              │
│  ├──────────────┤   │              ▲                                    │
│  │ id           │   │              │ has                                 │
│  │ asset_id     │   │              │                                    │
│  │ dataset      │   │      ┌──────────────┐                              │
│  │ table_name   │   │──────│   Column     │                              │
│  │ schema       │       │              │                              │
│  │ partitions   │       ├──────────────┤                              │
│  │ clusters     │       │ id           │                              │
│  │ storage_used │       │ asset_id     │                              │
│  │ row_count    │       │ column_name │                              │
│  │ last_modified│       │ data_type   │                              │
│  └──────────────┘       │ is_nullable │                              │
│                           └──────────────┘                              │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

## Entities

### 1. DataAsset

**Description**: A generic entity representing any data source, transformation, or destination. This is the base entity from which all other data entities inherit.

**Attributes**:

| Attribute | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `id` | UUID | Yes | Unique identifier for the data asset | `550e8400-e29b-41d4-a716-446655440000` |
| `name` | String(255) | Yes | Human-readable name | `customers` |
| `type` | Enum | Yes | Type of data asset | `bigquery_table`, `dbt_model`, `powerbi_semantic_model`, `external` |
| `description` | Text | No | Detailed description | `Contains customer master data` |
| `source_type` | Enum | Yes | The source system type | `bigquery`, `dbt`, `powerbi`, `other` |
| `connection_id` | UUID | No | Reference to connection configuration | `conn-123` |
| `created_at` | Timestamp | Yes | When the asset was first cataloged | `2026-06-30T10:00:00Z` |
| `updated_at` | Timestamp | Yes | When the asset was last updated | `2026-06-30T10:00:00Z` |
| `is_active` | Boolean | Yes | Whether the asset is actively tracked | `true` |
| `external_id` | String(512) | No | External identifier (e.g., BigQuery table ID) | `project.dataset.table` |

**Validation Rules**:
- `name` must be unique within a source_type
- `type` must be one of: `bigquery_table`, `bigquery_view`, `dbt_model`, `dbt_source`, `dbt_seed`, `dbt_snapshot`, `powerbi_semantic_model`, `powerbi_report`, `external_database`, `api`, `file`
- `source_type` must be one of: `bigquery`, `dbt`, `powerbi`, `other`

---

### 2. Metadata

**Description**: Stores metadata about data assets including owner, description, schema, data type, freshness expectations, and classification level. Every data asset must have metadata.

**Attributes**:

| Attribute | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `id` | UUID | Yes | Unique identifier for the metadata entry | `660e8400-e29b-41d4-a716-446655440001` |
| `asset_id` | UUID | Yes | Reference to the DataAsset | `550e8400-e29b-41d4-a716-446655440000` |
| `key` | String(100) | Yes | Metadata key | `owner`, `freshness_expectation`, `classification_level` |
| `value` | Text | No | Metadata value (stored as JSON string for structured data) | `{"email": "john@example.com", "team": "data"}` |
| `data_type` | Enum | Yes | Type of the value | `string`, `number`, `boolean`, `json`, `date`, `timestamp` |
| `source` | Enum | Yes | Source of this metadata | `auto_discovered`, `manual`, `dbt`, `powerbi`, `user_provided` |
| `classification` | String(50) | No | Classification category | `PII`, `PDS`, `confidential`, `internal`, `public` |
| `sensitivity_level` | Enum | No | Sensitivity level | `high`, `medium`, `low` |
| `created_at` | Timestamp | Yes | When the metadata was created | `2026-06-30T10:00:00Z` |
| `updated_at` | Timestamp | Yes | When the metadata was last updated | `2026-06-30T10:00:00Z` |

**Validation Rules**:
- `key` must be unique per asset_id
- `data_type` must be one of: `string`, `number`, `boolean`, `json`, `date`, `timestamp`
- `source` must be one of: `auto_discovered`, `manual`, `dbt`, `powerbi`, `user_provided`
- `classification` must be from a predefined taxonomy
- `sensitivity_level` must be one of: `high`, `medium`, `low`

**Predefined Metadata Keys**:
- `owner` (json): `{email, name, team}`
- `description` (string): Long description
- `schema` (json): Column definitions
- `data_type` (string): Type of data
- `freshness_expectation` (json): `{frequency, threshold, cron}`
- `classification_level` (string): `PII`, `PDS`, `confidential`, etc.
- `retention_policy` (json): `{days, archive_after}`
- `access_control` (json): `{read: [...], write: [...]}`

---

### 3. LineageEdge

**Description**: Represents a relationship/edge in the lineage graph, connecting source and target data assets with a relationship type.

**Attributes**:

| Attribute | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `id` | UUID | Yes | Unique identifier for the lineage edge | `770e8400-e29b-41d4-a716-446655440002` |
| `source_id` | UUID | Yes | Reference to source DataAsset | `550e8400-e29b-41d4-a716-446655440000` |
| `target_id` | UUID | Yes | Reference to target DataAsset | `880e8400-e29b-41d4-a716-446655440003` |
| `relationship_type` | Enum | Yes | Type of relationship | `transforms`, `depends_on`, `feeds_into`, `references`, `materializes` |
| `transformation_type` | String(50) | No | Specific transformation type | `dbt_model`, `dbt_seed`, `sql_view`, `etl_job` |
| `column_mapping` | JSON | No | Column-level lineage mapping | `{"col1": "col1", "col2": "col2_transformed"}` |
| `sql_logic` | Text | No | SQL logic if applicable | `SELECT * FROM source` |
| `metadata` | JSON | No | Additional edge metadata | `{"priority": "high", "frequency": "daily"}` |
| `discovered_at` | Timestamp | Yes | When the lineage was discovered | `2026-06-30T10:00:00Z` |
| `verified_at` | Timestamp | No | When the lineage was manually verified | `2026-06-30T11:00:00Z` |
| `verification_status` | Enum | Yes | Verification status | `auto_discovered`, `verified`, `needs_review`, `rejected` |
| `is_production` | Boolean | Yes | Whether this lineage is production-ready | `true` |

**Validation Rules**:
- `source_id` and `target_id` must reference existing DataAsset records
- `relationship_type` must be one of: `transforms`, `depends_on`, `feeds_into`, `references`, `materializes`, `copies`, `aggregates`
- `verification_status` must be one of: `auto_discovered`, `verified`, `needs_review`, `rejected`
- Circular references are allowed but will be flagged in validation

---

### 4. BigQueryTable (Specialization of DataAsset)

**Description**: Represents a BigQuery table or view with BigQuery-specific attributes.

**Attributes** (in addition to DataAsset):

| Attribute | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `project_id` | String(255) | Yes | Google Cloud project ID | `my-project-123` |
| `dataset_id` | String(255) | Yes | BigQuery dataset ID | `analytics` |
| `table_type` | Enum | Yes | Type of BigQuery object | `TABLE`, `VIEW`, `MATERIALIZED_VIEW`, `EXTERNAL` |
| `partitioning` | JSON | No | Partitioning configuration | `{"type": "DATE", "field": "created_at"}` |
| `clustering` | JSON | No | Clustering configuration | `{"fields": ["user_id", "region"]}` |
| `storage_bytes` | Integer | No | Storage used in bytes | `1048576` |
| `row_count` | Integer | No | Number of rows | `1000000` |
| `last_modified` | Timestamp | No | Last modification timestamp | `2026-06-30T10:00:00Z` |
| `created` | Timestamp | No | Creation timestamp | `2026-01-01T00:00:00Z` |
| `expires` | Timestamp | No | Expiration timestamp | `2027-06-30T00:00:00Z` |

**Validation Rules**:
- `table_type` must be one of: `TABLE`, `VIEW`, `MATERIALIZED_VIEW`, `EXTERNAL`
- `project_id` must be a valid GCP project ID
- `dataset_id` must match BigQuery dataset naming rules

---

### 5. BigQueryColumn (Specialization for columns)

**Description**: Represents a column within a BigQuery table.

**Attributes**:

| Attribute | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `id` | UUID | Yes | Unique identifier | `990e8400-e29b-41d4-a716-446655440004` |
| `asset_id` | UUID | Yes | Reference to parent DataAsset (BigQueryTable) | `550e8400-e29b-41d4-a716-446655440000` |
| `column_name` | String(300) | Yes | Column name | `customer_id` |
| `column_index` | Integer | Yes | Position in table (0-indexed) | `0` |
| `data_type` | String(50) | Yes | BigQuery data type | `STRING`, `INT64`, `FLOAT64`, `TIMESTAMP`, `RECORD`, `ARRAY` |
| `is_nullable` | Boolean | Yes | Whether column allows NULL | `false` |
| `description` | Text | No | Column description | `Unique identifier for customer` |
| `is_partitioning_column` | Boolean | No | Whether this is a partitioning column | `false` |
| `is_clustering_column` | Boolean | No | Whether this is a clustering column | `true` |
| `precision` | Integer | No | Precision for numeric types | `10` |
| `scale` | Integer | No | Scale for numeric types | `2` |
| `max_length` | Integer | No | Maximum length for string types | `255` |
| `is_pii` | Boolean | No | Whether this column contains PII | `true` |
| `pii_category` | String(50) | No | PII category | `email`, `phone`, `ssn` |

**Validation Rules**:
- `column_name` must be unique per table
- `data_type` must be a valid BigQuery data type
- `is_nullable` default is `true`

---

### 6. dbtModel (Specialization of DataAsset)

**Description**: Represents a dbt model with dbt-specific attributes.

**Attributes** (in addition to DataAsset):

| Attribute | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `model_name` | String(255) | Yes | dbt model name | `stg_customers` |
| `resource_type` | Enum | Yes | dbt resource type | `model`, `source`, `seed`, `snapshot`, `analysis` |
| `package_name` | String(255) | No | dbt package name | `my_project` |
| `path` | String(512) | No | File path in dbt project | `models/staging/stg_customers.sql` |
| `raw_sql` | Text | No | Raw SQL from model file | `SELECT * FROM {{ source(...) }}` |
| `compiled_sql` | Text | No | Compiled SQL (after Jinja rendering) | `SELECT * FROM project.dataset.raw_customers` |
| `database` | String(255) | No | Target database | `analytics` |
| `schema` | String(255) | No | Target schema | `staging` |
| `alias` | String(255) | No | Model alias | `stg_cust` |
| `materialized` | Enum | Yes | Materialization strategy | `table`, `view`, `incremental`, `ephemeral` |
| `config` | JSON | No | dbt model config | `{"materialized": "incremental", "incremental_strategy": "merge"}` |
| `docs` | JSON | No | dbt documentation | `{"description": "Staging model for customers"}` |
| `meta` | JSON | No | dbt meta | `{"owner": "@john"}` |
| `tests` | JSON | No | dbt tests | `[{"test_name": "not_null", "column_name": "customer_id"}]` |
| `dependencies` | JSON | No | List of dependencies | `["model.my_project.stg_orders"]` |
| `build_path` | String(512) | No | Build path in dbt artifacts | `target/run/my_project/models/staging/stg_customers.sql` |
| `unique_id` | String(512) | No | dbt unique ID | `model.my_project.stg_customers` |
| `patch_path` | String(512) | No | Patch path if applicable | `models/staging/stg_customers.yml` |
| `buildable` | Boolean | No | Whether the model is buildable | `true` |
| `checksum` | JSON | No | Checksum information | `{"name": "sha256", "checksum": "abc123..."}` |

**Validation Rules**:
- `resource_type` must be one of: `model`, `source`, `seed`, `snapshot`, `analysis`, `operation`, `singular`, `hook`
- `materialized` must be one of: `table`, `view`, `incremental`, `ephemeral`, `materialized_table`

---

### 7. dbtSource (Specialization of DataAsset)

**Description**: Represents a dbt source definition.

**Attributes** (in addition to DataAsset):

| Attribute | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `source_name` | String(255) | Yes | dbt source name | `raw` |
| `table_name` | String(255) | Yes | Source table name | `customers` |
| `database` | String(255) | No | Source database | `raw_data` |
| `schema` | String(255) | No | Source schema | `ecommerce` |
| `identifier` | String(512) | No | Source identifier | `raw_customers` |
| `quoting` | JSON | No | Quoting configuration | `{"database": false, "schema": false, "identifier": false}` |
| `loaded_at_field` | String(255) | No | Field used for incremental loading | `loaded_at` |
| `freshness` | JSON | No | Freshness configuration | `{"warn_after": "12h", "error_after": "24h"}` |
| `external` | JSON | No | External configuration | `{"location": "BigQuery", "table": "project.dataset.table"}` |
| `description` | Text | No | Source description | `Raw customer data from ecommerce platform` |
| `columns` | JSON | No | Column definitions | `[{"name": "id", "type": "INT64"}]` |
| `meta` | JSON | No | Source meta | `{"type": "raw"}` |
| `source_definition_path` | String(512) | No | Path to source definition | `models/sources.yml` |
| `unrendered_config` | JSON | No | Unrendered source config | `...` |

---

### 8. PowerBISemanticModel (Specialization of DataAsset)

**Description**: Represents a Power BI semantic model (formerly dataset) with Power BI-specific attributes.

**Attributes** (in addition to DataAsset):

| Attribute | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `workspace_id` | UUID | Yes | Power BI workspace ID | `a1b2c3d4-e5f6-7890-1234-567890abcdef` |
| `workspace_name` | String(255) | No | Power BI workspace name | `Analytics` |
| `dataset_id` | UUID | Yes | Power BI dataset ID | `b2c3d4e5-f6g7-8901-2345-67890abcdef1` |
| `dataset_name` | String(255) | Yes | Power BI dataset name | `Sales_Mart` |
| `configured_by` | String(255) | No | Who configured the semantic model | `john@example.com` |
| `default_mode` | Enum | No | Default mode | `Push`, `Pull`, `LiveConnect` |
| `storage_mode` | Enum | No | Storage mode | `Import`, `DirectQuery`, `Dual`, `Push` |
| `refresh_schedule` | JSON | No | Refresh schedule | `{"frequency": "daily", "time": "02:00"}` |
| `last_refresh` | Timestamp | No | Last refresh timestamp | `2026-06-30T02:00:00Z` |
| `tables` | JSON | No | List of tables in semantic model | `[{"name": "Sales", "rows": 1000000}]` |
| `relationships` | JSON | No | Relationships between tables | `[{"from": "Sales", "to": "Date", "type": "ManyToOne"}]` |
| `measures` | JSON | No | Measures defined in semantic model | `[{"name": "Total Sales", "expression": "SUM(Sales[Amount])"}]` |
| `columns` | JSON | No | Columns with their properties | `[{"name": "SalesAmount", "type": "Decimal", "isHidden": false}]` |
| `culture` | String(10) | No | Locale/culture | `en-US` |
| `collation` | String(20) | No | Collation setting | `Latin1_General_CI_AS` |

**Validation Rules**:
- `default_mode` must be one of: `Push`, `Pull`, `LiveConnect`
- `storage_mode` must be one of: `Import`, `DirectQuery`, `Dual`, `Push`

---

### 9. PowerBITable (Specialization for Power BI tables)

**Description**: Represents a table within a Power BI semantic model.

**Attributes**:

| Attribute | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `id` | UUID | Yes | Unique identifier | `a1b2c3d4-e5f6-7890-1234-567890abcdef` |
| `semantic_model_id` | UUID | Yes | Reference to PowerBISemanticModel | `b2c3d4e5-f6g7-8901-2345-67890abcdef1` |
| `name` | String(255) | Yes | Table name | `Sales` |
| `display_name` | String(255) | No | Display name | `Sales Data` |
| `description` | Text | No | Table description | `Contains all sales transactions` |
| `is_hidden` | Boolean | Yes | Whether table is hidden | `false` |
| `row_count` | Integer | No | Number of rows | `1000000` |
| `columns` | JSON | No | List of columns | `[{"name": "Date", "type": "date"}]` |
| `measures` | JSON | No | List of measures | `[{"name": "Total Sales", "expression": "SUM(Sales[Amount])"}]` |
| `hierarchies` | JSON | No | Hierarchies defined | `[{"name": "Date Hierarchy", "levels": ["Year", "Quarter", "Month"]}]` |

---

### 10. PowerBIRelationship

**Description**: Represents a relationship between tables in a Power BI semantic model.

**Attributes**:

| Attribute | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `id` | UUID | Yes | Unique identifier | `c1d2e3f4-a5b6-7890-1234-567890abcdef` |
| `semantic_model_id` | UUID | Yes | Reference to PowerBISemanticModel | `b2c3d4e5-f6g7-8901-2345-67890abcdef1` |
| `name` | String(255) | Yes | Relationship name | `Sales_to_Date` |
| `from_table` | String(255) | Yes | Source table name | `Sales` |
| `from_column` | String(255) | Yes | Source column name | `OrderDate` |
| `to_table` | String(255) | Yes | Target table name | `Date` |
| `to_column` | String(255) | Yes | Target column name | `Date` |
| `cardinality` | Enum | Yes | Relationship cardinality | `OneToMany`, `ManyToOne`, `OneToOne`, `ManyToMany` |
| `cross_filter_direction` | Enum | Yes | Cross-filter direction | `OneWay`, `Both`, `Automatic` |
| `is_active` | Boolean | Yes | Whether relationship is active | `true` |

**Validation Rules**:
- `cardinality` must be one of: `OneToMany`, `ManyToOne`, `OneToOne`, `ManyToMany`
- `cross_filter_direction` must be one of: `OneWay`, `Both`, `Automatic`

---

### 11. ClassificationTag

**Description**: Represents a classification tag for data assets or columns, used for PII/PDS identification and masking.

**Attributes**:

| Attribute | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `id` | UUID | Yes | Unique identifier | `d1e2f3g4-b5h6-7890-1234-567890abcdef` |
| `asset_id` | UUID | No | Reference to DataAsset (nullable for global tags) | `550e8400-e29b-41d4-a716-446655440000` |
| `column_id` | UUID | No | Reference to BigQueryColumn (nullable) | `990e8400-e29b-41d4-a716-446655440004` |
| `tag` | String(50) | Yes | Classification tag | `PII`, `email`, `phone`, `credit_card`, `ssn` |
| `category` | Enum | Yes | Tag category | `personal`, `financial`, `health`, `other` |
| `sensitivity` | Enum | Yes | Sensitivity level | `high`, `medium`, `low` |
| `mask_pattern` | String(100) | No | Pattern for masking | `***MASKED***`, `****-****-****-****` |
| `is_regex` | Boolean | No | Whether mask_pattern is a regex | `false` |
| `applies_to_dev` | Boolean | Yes | Whether to mask in development | `true` |
| `applies_to_prod` | Boolean | Yes | Whether to mask in production | `false` |
| `created_at` | Timestamp | Yes | When the tag was created | `2026-06-30T10:00:00Z` |

**Validation Rules**:
- Either `asset_id` or `column_id` must be provided
- `category` must be one of: `personal`, `financial`, `health`, `government`, `other`
- `sensitivity` must be one of: `high`, `medium`, `low`

---

### 12. LineageGraphMaterialized (Pre-computed lineage paths)

**Description**: Pre-computed lineage paths for faster querying. This is an optimization table.

**Attributes**:

| Attribute | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `id` | UUID | Yes | Unique identifier | `e1f2g3h4-c5i6-7890-1234-567890abcdef` |
| `source_id` | UUID | Yes | Source DataAsset ID | `550e8400-e29b-41d4-a716-446655440000` |
| `target_id` | UUID | Yes | Target DataAsset ID | `880e8400-e29b-41d4-a716-446655440003` |
| `path` | JSON | Yes | Array of asset IDs in the path | `[id1, id2, id3, ...]` |
| `depth` | Integer | Yes | Number of hops in the path | `3` |
| `path_type` | Enum | Yes | Type of path | `shortest`, `all`, `direct` |
| `updated_at` | Timestamp | Yes | When the path was last computed | `2026-06-30T10:00:00Z` |

**Validation Rules**:
- `path_type` must be one of: `shortest`, `all`, `direct`
- `depth` must be >= 1

---

## Relationships

### Entity Relationships

1. **DataAsset to Metadata**: One-to-Many (1:N)
   - One DataAsset can have many Metadata entries
   - Metadata.asset_id → DataAsset.id

2. **DataAsset to LineageEdge**: One-to-Many (1:N) as source and target
   - One DataAsset can be the source of many LineageEdge records
   - One DataAsset can be the target of many LineageEdge records
   - LineageEdge.source_id → DataAsset.id
   - LineageEdge.target_id → DataAsset.id

3. **BigQueryTable to BigQueryColumn**: One-to-Many (1:N)
   - One BigQueryTable can have many BigQueryColumn records
   - BigQueryColumn.asset_id → BigQueryTable.id (via DataAsset)

4. **PowerBISemanticModel to PowerBITable**: One-to-Many (1:N)
   - One PowerBISemanticModel can have many PowerBITable records
   - PowerBITable.semantic_model_id → PowerBISemanticModel.id (via DataAsset)

5. **PowerBISemanticModel to PowerBIRelationship**: One-to-Many (1:N)
   - One PowerBISemanticModel can have many PowerBIRelationship records
   - PowerBIRelationship.semantic_model_id → PowerBISemanticModel.id (via DataAsset)

6. **DataAsset to ClassificationTag**: One-to-Many (1:N)
   - One DataAsset can have many ClassificationTag records
   - ClassificationTag.asset_id → DataAsset.id

7. **BigQueryColumn to ClassificationTag**: One-to-Many (1:N)
   - One BigQueryColumn can have many ClassificationTag records
   - ClassificationTag.column_id → BigQueryColumn.id

8. **DataAsset to LineageGraphMaterialized**: One-to-Many (1:N) as source and target
   - LineageGraphMaterialized.source_id → DataAsset.id
   - LineageGraphMaterialized.target_id → DataAsset.id

### Inheritance Relationships

- **BigQueryTable** inherits from **DataAsset** (type = `bigquery_table` or `bigquery_view`)
- **dbtModel** inherits from **DataAsset** (type = `dbt_model`, `dbt_source`, `dbt_seed`, etc.)
- **PowerBISemanticModel** inherits from **DataAsset** (type = `powerbi_semantic_model`)

---

## State Transitions

### DataAsset Lifecycle

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│    Discovered    │────▶│   Cataloged     │────▶│     Active      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Ignored/      │     │   Deprecated    │     │   Verification   │
│   Excluded       │     │                 │     │   Needed         │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

**States**:
1. **Discovered**: Asset was found but not yet cataloged
2. **Cataloged**: Asset metadata has been extracted and stored
3. **Active**: Asset is actively tracked and lineage is being maintained
4. **Deprecated**: Asset is no longer in use but kept for historical lineage
5. **Ignored/Excluded**: Asset was explicitly excluded from tracking

**Transitions**:
- Discovered → Cataloged: When metadata extraction completes
- Cataloged → Active: When lineage relationships are established
- Active → Deprecated: When asset is marked as no longer in use
- Cataloged/Active → Ignored: When asset is explicitly excluded

### LineageEdge Verification Lifecycle

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Auto-Discovered  │────▶│ Needs Review     │────▶│    Verified      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
       │                   │                   │
       ▼                   ▼                   ▼
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   (end state)    │     │    Rejected      │     │ Production Ready │
│   for simple     │     │                 │     │                 │
│   lineage         │     └─────────────────┘     └─────────────────┘
└─────────────────┘
```

**States**:
1. **Auto-Discovered**: Lineage was discovered automatically (from dbt manifest, etc.)
2. **Needs Review**: Lineage requires manual verification
3. **Verified**: Lineage has been manually verified
4. **Rejected**: Lineage was rejected (false positive, incorrect)
5. **Production Ready**: Lineage is verified and ready for production use

**Transitions**:
- Auto-Discovered → Needs Review: When lineage is flagged for verification
- Needs Review → Verified: When manual verification passes
- Needs Review → Rejected: When manual verification fails
- Verified → Production Ready: When all checks pass
- Verified/Production Ready → Needs Review: When source or target changes

---

## Validation Rules

### Cross-Entity Validation

1. **LineageEdge.source_id and LineageEdge.target_id** must reference existing DataAsset.id
2. **Metadata.asset_id** must reference existing DataAsset.id
3. **BigQueryColumn.asset_id** must reference existing BigQueryTable.id (which is a DataAsset)
4. **ClassificationTag.asset_id** must reference existing DataAsset.id OR ClassificationTag.column_id must reference existing BigQueryColumn.id
5. **PowerBITable.semantic_model_id** must reference existing PowerBISemanticModel.id
6. **PowerBIRelationship.semantic_model_id** must reference existing PowerBISemanticModel.id

### Business Rules

1. **No orphaned assets**: Every DataAsset should be referenced by at least one LineageEdge (except for root sources)
2. **No circular dependencies**: Lineage graph should be a Directed Acyclic Graph (DAG) for most use cases. Circular dependencies should be flagged but allowed for certain scenarios (e.g., recursive models)
3. **Metadata completeness**: All DataAssets should have at minimum: owner, description, classification_level
4. **Lineage verification**: All production lineage (is_production = true) must have verification_status = 'verified'
5. **PII masking**: All columns with is_pii = true must have corresponding ClassificationTag records

---

## Indexing Strategy

### BigQuery Tables (Physical Storage)

Since metadata is stored in BigQuery, we use BigQuery's partitioning and clustering features:

1. **Metadata Table**
   - Partitioned by: `created_at` (daily)
   - Clustered by: `asset_id`, `key`

2. **LineageEdge Table**
   - Partitioned by: `discovered_at` (daily)
   - Clustered by: `source_id`, `target_id`, `relationship_type`

3. **DataAsset Table**
   - Partitioned by: `created_at` (daily)
   - Clustered by: `type`, `source_type`, `is_active`

4. **BigQueryTable Table**
   - Partitioned by: `last_modified` (daily)
   - Clustered by: `project_id`, `dataset_id`

5. **BigQueryColumn Table**
   - Partitioned by: (none - small enough)
   - Clustered by: `asset_id`, `is_pii`

6. **LineageGraphMaterialized Table**
   - Partitioned by: `updated_at` (daily)
   - Clustered by: `source_id`, `target_id`

---

## Query Patterns

### Common Queries

1. **Get all lineage for an asset**
   ```sql
   -- Direct relationships
   SELECT * FROM lineage_edges 
   WHERE source_id = :asset_id OR target_id = :asset_id
   
   -- Full lineage graph (recursive)
   WITH RECURSIVE lineage_graph AS (
     SELECT source_id, target_id, 1 as depth, [source_id, target_id] as path
     FROM lineage_edges
     WHERE source_id = :asset_id
     
     UNION ALL
     
     SELECT le.source_id, le.target_id, lg.depth + 1, 
            ARRAY_CONCAT(lg.path, [le.target_id])
     FROM lineage_edges le
     JOIN lineage_graph lg ON le.source_id = lg.target_id
     WHERE lg.depth < 10  -- Prevent infinite recursion
   )
   SELECT * FROM lineage_graph
   ```

2. **Find all assets owned by a person**
   ```sql
   SELECT da.*
   FROM data_assets da
   JOIN metadata m ON da.id = m.asset_id
   WHERE m.key = 'owner'
     AND JSON_EXTRACT_SCALAR(m.value, '$.email') = :email
   ```

3. **Find all PII columns**
   ```sql
   SELECT bc.*
   FROM bigquery_columns bc
   JOIN classification_tags ct ON bc.id = ct.column_id
   WHERE ct.tag = 'PII'
   ```

4. **Get impact analysis for a source table**
   ```sql
   -- Find all downstream assets
   WITH RECURSIVE downstream AS (
     SELECT target_id, 1 as depth
     FROM lineage_edges
     WHERE source_id = :source_asset_id
     
     UNION ALL
     
     SELECT le.target_id, d.depth + 1
     FROM lineage_edges le
     JOIN downstream d ON le.source_id = d.target_id
     WHERE d.depth < 10
   )
   SELECT da.*
   FROM data_assets da
   JOIN downstream d ON da.id = d.target_id
   ```

5. **Get lineage from dbt model to Power BI semantic model**
   ```sql
   SELECT 
     bqt.table_name as bigquery_source,
     dm.model_name as dbt_model,
     pbsm.dataset_name as powerbi_semantic_model
   FROM lineage_edges le1
   JOIN data_assets da1 ON le1.source_id = da1.id
   JOIN bigquery_tables bqt ON da1.id = bqt.asset_id
   JOIN data_assets da2 ON le1.target_id = da2.id
   JOIN dbt_models dm ON da2.id = dm.asset_id
   JOIN lineage_edges le2 ON le1.target_id = le2.source_id
   JOIN data_assets da3 ON le2.target_id = da3.id
   JOIN powerbi_semantic_models pbsm ON da3.id = pbsm.asset_id
   WHERE le1.relationship_type = 'transforms'
     AND le2.relationship_type = 'feeds_into'
   ```

---

## Schema Evolution

### Versioning

- Schema changes will use migration scripts
- Each migration will be versioned and applied in order
- Backward compatibility will be maintained where possible
- Breaking changes will require a major version bump

### Migration Strategy

1. **Additive changes** (new columns, new tables): Applied automatically
2. **Structural changes** (column type changes): Require validation
3. **Breaking changes** (column removal, table removal): Require migration script

---

## Storage Estimates

### Per-Asset Storage

| Entity | Approx. Size per Record | Estimated Records | Total Storage |
|--------|-------------------------|-------------------|---------------|
| DataAsset | 500 bytes | 10,000 | ~5 MB |
| Metadata | 1 KB | 50,000 | ~50 MB |
| LineageEdge | 500 bytes | 20,000 | ~10 MB |
| BigQueryTable | 1 KB | 10,000 | ~10 MB |
| BigQueryColumn | 500 bytes | 100,000 | ~50 MB |
| dbtModel | 5 KB | 5,000 | ~25 MB |
| dbtSource | 1 KB | 2,000 | ~2 MB |
| PowerBISemanticModel | 5 KB | 500 | ~2.5 MB |
| PowerBITable | 2 KB | 5,000 | ~10 MB |
| PowerBIRelationship | 1 KB | 2,000 | ~2 MB |
| ClassificationTag | 500 bytes | 10,000 | ~5 MB |
| LineageGraphMaterialized | 1 KB | 100,000 | ~100 MB |
| **Total** | | | **~271.5 MB** |

### Growth Projections

- **Year 1**: 10k tables, 50k columns, 20k lineage edges → ~300 MB
- **Year 2**: 50k tables, 250k columns, 100k lineage edges → ~1.5 GB
- **Year 3**: 100k tables, 500k columns, 200k lineage edges → ~3 GB

These are manageable sizes for BigQuery and will not significantly impact query costs.

---

## Glossary

| Term | Definition |
|------|------------|
| **Data Asset** | Any data source, transformation, or destination that is tracked by DataTrace |
| **Lineage** | The flow of data from source to consumption, including all transformations |
| **Metadata** | Descriptive information about data assets |
| **dbt** | Data Build Tool, a transformation tool that uses SQL and Jinja templates |
| **BigQuery** | Google Cloud's serverless data warehouse |
| **Power BI** | Microsoft's business intelligence and visualization platform |
| **PII** | Personally Identifiable Information |
| **PDS** | Personal Data Subject (similar to PII) |
| **DAG** | Directed Acyclic Graph, a graph with no circular dependencies |
