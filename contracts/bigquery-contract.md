# DataTrace BigQuery Integration Contract

**Version**: v1.0.0 | **Status**: Draft | **Last Updated**: 2026-06-30

## Overview

This contract defines how DataTrace integrates with Google BigQuery to extract metadata about tables, views, routines, and other database objects.

## Integration Methods

### 1. INFORMATION_SCHEMA Queries

DataTrace queries BigQuery's INFORMATION_SCHEMA views to extract metadata.

**Key Views Used**:
- `INFORMATION_SCHEMA.TABLES` - Table and view metadata
- `INFORMATION_SCHEMA.COLUMNS` - Column metadata
- `INFORMATION_SCHEMA.TABLE_STORAGE` - Storage information
- `INFORMATION_SCHEMA.ROUTINES` - Stored procedures and functions
- `INFORMATION_SCHEMA.JOBS` - Job history
- `INFORMATION_SCHEMA.VIEWS` - View definitions

### 2. BigQuery REST API

DataTrace uses the BigQuery REST API for programmatic access.

**API Endpoint**: `https://bigquery.googleapis.com/bigquery/v2/`

## Connection Configuration

```yaml
# In DataTrace config file
connections:
  - name: my-bigquery
    type: bigquery
    project: my-project-123
    dataset: analytics  # Optional: default dataset
    
    # Authentication (choose one)
    credentials:
      type: service_account
      key_file: /path/to/key.json
    # OR
    credentials:
      type: application_default
    # OR
    credentials:
      type: oauth
      token: ya29.a1B2c3...
```

## Extracted Information

### From INFORMATION_SCHEMA.TABLES

| Field | Type | Description |
|-------|------|-------------|
| `table_catalog` | STRING | Project ID |
| `table_schema` | STRING | Dataset ID |
| `table_name` | STRING | Table name |
| `table_type` | STRING | TABLE, VIEW, etc. |
| `creation_time` | TIMESTAMP | Creation timestamp |
| `last_modified_time` | TIMESTAMP | Last modification timestamp |
| `is_partitioned` | BOOLEAN | Whether table is partitioned |
| `partitioning_column` | STRING | Partitioning column |
| `clustering_columns` | ARRAY | Clustering columns |
| `row_count` | INT64 | Number of rows |
| `size_bytes` | INT64 | Size in bytes |

### From INFORMATION_SCHEMA.COLUMNS

| Field | Type | Description |
|-------|------|-------------|
| `table_catalog` | STRING | Project ID |
| `table_schema` | STRING | Dataset ID |
| `table_name` | STRING | Table name |
| `column_name` | STRING | Column name |
| `data_type` | STRING | Data type |
| `is_nullable` | BOOLEAN | Allows NULL |
| `column_default` | STRING | Default value |
| `max_length` | INT64 | Max length |
| `numeric_precision` | INT64 | Precision |
| `numeric_scale` | INT64 | Scale |

### From INFORMATION_SCHEMA.TABLE_STORAGE

| Field | Type | Description |
|-------|------|-------------|
| `table_catalog` | STRING | Project ID |
| `table_schema` | STRING | Dataset ID |
| `table_name` | STRING | Table name |
| `total_rows` | INT64 | Total rows |
| `total_bytes` | INT64 | Total bytes |
| `active_bytes` | INT64 | Active bytes |
| `long_term_bytes` | INT64 | Long-term storage bytes |

## Discovery Queries

### Full Metadata Discovery

```sql
-- Get all tables and views
SELECT 
  table_catalog as project_id,
  table_schema as dataset_id,
  table_name,
  table_type,
  creation_time,
  last_modified_time
FROM `region-us`.INFORMATION_SCHEMA.TABLES
WHERE table_schema NOT IN ('information_schema', 'datatrace_metadata')
```

### Column Metadata Discovery

```sql
-- Get all columns for all tables
SELECT 
  t.table_catalog as project_id,
  t.table_schema as dataset_id,
  t.table_name,
  c.column_name,
  c.data_type,
  c.is_nullable,
  c.column_default,
  c.max_length,
  c.numeric_precision,
  c.numeric_scale
FROM `region-us`.INFORMATION_SCHEMA.TABLES t
JOIN `region-us`.INFORMATION_SCHEMA.COLUMNS c
  ON t.table_catalog = c.table_catalog
  AND t.table_schema = c.table_schema
  AND t.table_name = c.table_name
WHERE t.table_schema NOT IN ('information_schema', 'datatrace_metadata')
```

### Storage Information

```sql
-- Get storage information
SELECT 
  table_catalog as project_id,
  table_schema as dataset_id,
  table_name,
  total_rows,
  total_bytes,
  active_bytes,
  long_term_bytes
FROM `region-us`.INFORMATION_SCHEMA.TABLE_STORAGE
WHERE table_schema NOT IN ('information_schema', 'datatrace_metadata')
```

## API Interface

### Python Interface

```python
from datatrace.integrations.bigquery import BigQueryConnection

# Initialize connection
conn = BigQueryConnection(
    project="my-project-123",
    credentials_path="/path/to/key.json"
)

# Discover all datasets
atasets = conn.get_datasets()

# Discover all tables in a dataset
tables = conn.get_tables(dataset="analytics")

# Get table metadata
metadata = conn.get_table_metadata("analytics", "customers")

# Get column metadata
columns = conn.get_columns("analytics", "customers")
```

## Metadata Schema

### BigQueryTable Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "project_id": {"type": "string"},
    "dataset_id": {"type": "string"},
    "table_id": {"type": "string"},
    "table_type": {"type": "string", "enum": ["TABLE", "VIEW", "MATERIALIZED_VIEW", "EXTERNAL"]},
    "friendly_name": {"type": "string"},
    "description": {"type": "string"},
    "creation_time": {"type": "string", "format": "date-time"},
    "last_modified_time": {"type": "string", "format": "date-time"},
    "partitioning": {
      "type": "object",
      "properties": {
        "type": {"type": "string", "enum": ["DATE", "INTEGER_RANGE", "TIME", "TIMESTAMP"]},
        "field": {"type": "string"},
        "range": {"type": "object"},
        "interval": {"type": "integer"}
      }
    },
    "clustering": {
      "type": "array",
      "items": {"type": "string"}
    },
    "row_count": {"type": "integer"},
    "size_bytes": {"type": "integer"},
    "labels": {
      "type": "object",
      "additionalProperties": {"type": "string"}
    },
    "location": {"type": "string"},
    "expires": {"type": "string", "format": "date-time"}
  },
  "required": ["project_id", "dataset_id", "table_id", "table_type"]
}
```

### BigQueryColumn Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "project_id": {"type": "string"},
    "dataset_id": {"type": "string"},
    "table_id": {"type": "string"},
    "column_name": {"type": "string"},
    "data_type": {"type": "string"},
    "is_nullable": {"type": "boolean"},
    "description": {"type": "string"},
    "column_default": {"type": ["string", "null"]},
    "max_length": {"type": ["integer", "null"]},
    "numeric_precision": {"type": ["integer", "null"]},
    "numeric_scale": {"type": ["integer", "null"]},
    "is_partitioning_column": {"type": "boolean"},
    "is_clustering_column": {"type": "boolean"}
  },
  "required": ["project_id", "dataset_id", "table_id", "column_name", "data_type"]
}
```

## Error Handling

### BigQuery Integration Errors

| Error Code | Description | Recovery |
|------------|-------------|----------|
| `PROJECT_NOT_FOUND` | GCP project not found | Verify project ID |
| `DATASET_NOT_FOUND` | Dataset not found | Verify dataset ID |
| `TABLE_NOT_FOUND` | Table not found | Verify table ID |
| `AUTHENTICATION_FAILED` | Authentication failed | Check credentials |
| `PERMISSION_DENIED` | Permission denied | Check IAM permissions |
| `QUOTA_EXCEEDED` | Quota exceeded | Check BigQuery quotas |
| `RATE_LIMITED` | Rate limited | Wait and retry |

## Security

### IAM Permissions Required

DataTrace requires the following IAM permissions:

- `bigquery.tables.get` - Get table metadata
- `bigquery.tables.list` - List tables in a dataset
- `bigquery.datasets.get` - Get dataset metadata
- `bigquery.datasets.list` - List datasets in a project
- `bigquery.routines.get` - Get routine metadata
- `bigquery.routines.list` - List routines in a dataset
- `bigquery.jobs.get` - Get job metadata
- `bigquery.jobs.list` - List jobs in a project

### Predefined Roles

- `roles/bigquery.dataViewer` - Read-only access to data
- `roles/bigquery.dataEditor` - Read and write access
- `roles/bigquery.metadataViewer` - Read-only access to metadata
- `roles/bigquery.admin` - Full access

### Service Account Setup

```bash
# Create service account
gcloud iam service-accounts create datatrace-sa \
  --display-name="DataTrace Service Account"

# Grant permissions
gcloud projects add-iam-policy-binding my-project-123 \
  --member="serviceAccount:datatrace-sa@my-project-123.iam.gserviceaccount.com" \
  --role="roles/bigquery.metadataViewer"

# Create key
gcloud iam service-accounts keys create /path/to/key.json \
  --iam-account=datatrace-sa@my-project-123.iam.gserviceaccount.com
```

## Performance

### Performance Characteristics

| Operation | Typical Duration | Data Scanned |
|-----------|------------------|--------------|
| List datasets | < 1 second | 0 bytes |
| List tables in dataset | < 1 second | 0 bytes |
| Get table metadata | < 1 second | 0 bytes |
| Get columns for table | < 1 second | 0 bytes |
| Get storage info | < 1 second | 0 bytes |
| Full project scan | < 1 minute | 0 bytes |

### Optimization Techniques

1. **Metadata-only queries**: INFORMATION_SCHEMA queries don't scan data
2. **Parallel discovery**: Multiple datasets can be discovered in parallel
3. **Caching**: Metadata is cached to avoid repeated queries
4. **Incremental updates**: Only query for changed tables

## Best Practices

1. **Use service account with least privilege**
   - Only grant necessary permissions
   - Use custom roles if needed

2. **Enable BigQuery metadata caching**
   - Reduces API calls
   - Improves performance

3. **Exclude system datasets**
   - Don't scan INFORMATION_SCHEMA
   - Exclude DataTrace's own metadata dataset

4. **Use dataset-level permissions**
   - Limit access to specific datasets
   - Use dataset-level IAM policies

5. **Monitor quotas**
   - BigQuery has quotas for metadata operations
   - Implement backoff for rate limiting

## Testing

### Contract Tests

```bash
# Test BigQuery connection
datatrace test bigquery --project my-project-123

# Validate metadata extraction
datatrace test bigquery-metadata --project my-project-123 --dataset analytics

# Test specific table
datatrace test bigquery-table --project my-project-123 --dataset analytics --table customers
```

### Test Cases

1. **Valid project access**
   - Given: Valid GCP project with DataTrace permissions
   - When: DataTrace connects to BigQuery
   - Then: All datasets are listed successfully

2. **Dataset with tables**
   - Given: Dataset with multiple tables
   - When: DataTrace discovers dataset
   - Then: All tables and their metadata are extracted

3. **Partitioned and clustered tables**
   - Given: Tables with partitioning and clustering
   - When: DataTrace extracts table metadata
   - Then: Partitioning and clustering info is captured

4. **Missing permissions**
   - Given: Project without DataTrace permissions
   - When: DataTrace attempts to list datasets
   - Then: Permission denied error is returned

## Limitations

1. **Cross-project queries**
   - Requires permissions in all projects
   - Cross-project lineage may require additional configuration

2. **External tables**
   - External table metadata is limited
   - May not include all schema information

3. **Real-time updates**
   - Metadata may be slightly delayed
   - BigQuery INFORMATION_SCHEMA updates may lag

4. **BigQuery editions**
   - Some features may differ between BigQuery and BigQuery Omni
   - Multi-cloud support may be limited

## Future Enhancements

1. **Change Data Capture (CDC)**
   - Detect schema changes in real-time
   - Track table evolution

2. **Data Quality Monitoring**
   - Integrate with BigQuery Data Quality
   - Monitor data quality metrics

3. **Cost Analysis**
   - Analyze query costs
   - Provide cost optimization recommendations

4. **Multi-cloud Support**
   - Support BigQuery Omni (AWS, Azure)
   - Unified metadata across clouds
