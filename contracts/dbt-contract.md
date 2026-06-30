# DataTrace dbt Integration Contract

**Version**: v1.0.0 | **Status**: Draft | **Last Updated**: 2026-06-30

## Overview

This contract defines how DataTrace integrates with dbt projects to extract metadata, lineage, and other information. The integration supports both dbt Core and dbt Cloud.

## Integration Methods

### 1. Local dbt Project (dbt Core)

DataTrace reads dbt artifacts directly from the local filesystem.

**Required Files**:
- `manifest.json` - Main manifest file
- `run_results.json` - Run results (optional, for test status)
- `catalog.json` - Documentation catalog (optional)
- `dbt_schema.yml` - Schema information (optional)

**Location**: Typically in `target/` directory of the dbt project.

### 2. dbt Cloud API

DataTrace connects to dbt Cloud via the Artifacts API.

**API Endpoint**: `https://cloud.getdbt.com/api/v2/`

## Connection Configuration

### dbt Core Configuration

```yaml
# In DataTrace config file
connections:
  - name: my-dbt-project
    type: dbt
    path: /path/to/dbt/project
    profiles_yml: /path/to/profiles.yml
    target_path: /path/to/dbt/project/target
    
# Optional: Specific connection settings
    database: analytics
    schema: staging
    threads: 4
```

### dbt Cloud Configuration

```yaml
# In DataTrace config file
connections:
  - name: my-dbt-cloud-project
    type: dbt_cloud
    account_id: 12345
    project_id: 67890
    api_key: dbtc_abc123...  # Or use environment variable
    environment: production
```

## Extracted Information

### From manifest.json

DataTrace extracts the following from the dbt manifest:

1. **Models**
   - Model name, database, schema
   - Materialization type (table, view, incremental, ephemeral)
   - Raw SQL and compiled SQL
   - Dependencies (parents and children)
   - Configuration (materialized, incremental_strategy, etc.)
   - Documentation (description, meta)
   - Tags
   - Tests

2. **Sources**
   - Source name, database, schema
   - Table name
   - Column definitions
   - Freshness configuration
   - Documentation
   - External configuration

3. **Seeds**
   - Seed name, database, schema
   - File path
   - Column definitions

4. **Snapshots**
   - Snapshot name, database, schema
   - Target database and schema
   - Configuration

5. **Macros**
   - Macro name
   - File path
   - Arguments

6. **Dependencies**
   - Full dependency graph
   - Child map and parent map

### From catalog.json

DataTrace extracts documentation information:
- Model documentation
- Column documentation
- Source documentation

### From run_results.json

DataTrace extracts test results:
- Test names
- Test status (pass/fail/error)
- Execution time
- Test results per model

## Lineage Extraction

### Model Lineage

DataTrace creates lineage edges based on dbt model dependencies:

```
Source Table -> dbt Source -> dbt Model (staging) -> dbt Model (mart) -> Target Table
                \_______-> dbt Model (other) ->/
```

**Relationship Types**:
- `depends_on`: Model depends on source or another model
- `transforms`: Model transforms source data
- `materializes`: Model materializes as a table or view

### Column-Level Lineage

If available, DataTrace extracts column-level lineage from:
- dbt column metadata
- SQL parsing (experimental)

## Discovery Process

### Step 1: Locate dbt Project

```bash
# For local projects
dbt ls --project-dir /path/to/project

# DataTrace uses:
# 1. Explicit path in configuration
# 2. dbt_project.yml search
# 3. Environment variable DBT_PROJECT_DIR
```

### Step 2: Run dbt Compile

```bash
# DataTrace can trigger dbt compile
dbt compile --project-dir /path/to/project
```

### Step 3: Parse Artifacts

DataTrace parses:
1. `manifest.json` - Primary source of truth
2. `catalog.json` - Documentation
3. `run_results.json` - Test results (if available)

### Step 4: Extract Metadata

For each model:
- Extract model metadata
- Extract dependencies
- Create lineage edges
- Store in DataTrace database

## API Interface

### dbt Core Integration

**Python Interface**:

```python
from datatrace.integrations.dbt import DbtProject

# Initialize project
project = DbtProject(
    path="/path/to/dbt/project",
    profiles_yml="/path/to/profiles.yml"
)

# Discover
assets = project.discover()

# Get lineage
lineage = project.get_lineage()
```

### dbt Cloud Integration

**API Interface**:

```python
from datatrace.integrations.dbt_cloud import DbtCloudProject

# Initialize project
project = DbtCloudProject(
    account_id=12345,
    project_id=67890,
    api_key="dbtc_abc123..."
)

# Get latest artifacts
artifacts = project.get_latest_artifacts()

# Discover
assets = project.discover()
```

## Configuration Schema

### dbtConfig Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "type": {
      "type": "string",
      "enum": ["dbt", "dbt_cloud"]
    },
    "name": {
      "type": "string"
    },
    "path": {
      "type": "string",
      "description": "Path to dbt project (for dbt Core)"
    },
    "profiles_yml": {
      "type": "string",
      "description": "Path to profiles.yml"
    },
    "target_path": {
      "type": "string",
      "description": "Path to target directory"
    },
    "account_id": {
      "type": "integer",
      "description": "dbt Cloud account ID"
    },
    "project_id": {
      "type": "integer",
      "description": "dbt Cloud project ID"
    },
    "api_key": {
      "type": "string",
      "description": "dbt Cloud API key"
    },
    "environment": {
      "type": "string",
      "description": "dbt Cloud environment"
    }
  },
  "required": ["type", "name"]
}
```

## Manifest Schema (Subset)

### Model Schema

```json
{
  "database": "string",
  "schema": "string",
  "name": "string",
  "resource_type": "model",
  "package_name": "string",
  "path": "string",
  "original_file_path": "string",
  "unique_id": "string",
  "alias": "string",
  "checksum": {
    "name": "string",
    "checksum": "string"
  },
  "config": {
    "materialized": "string",
    "incremental_strategy": "string",
    "persist_docs": {
      "relation": true,
      "columns": true
    }
  },
  "tags": ["string"],
  "meta": {},
  "docs": {
    "show": true
  },
  "columns": {
    "column_name": {
      "type": "string",
      "index": 0,
      "name": "string"
    }
  },
  "tests": [
    {
      "test_metadata": {
        "name": "string",
        "kwargs": {}
      },
      "column_name": "string"
    }
  ],
  "dependencies": ["string"],
  "children": ["string"],
  "parents": ["string"],
  "raw_sql": "string",
  "compiled_sql": "string",
  "build_path": "string",
  "deferred": false,
  "unrendered_config": {},
  "relation_name": "string",
  "created_at": 0
}
```

## Error Handling

### dbt Integration Errors

| Error Code | Description | Recovery |
|------------|-------------|----------|
| `DBT_PROJECT_NOT_FOUND` | dbt project not found at specified path | Verify path |
| `DBT_COMPILE_FAILED` | dbt compile failed | Check dbt project |
| `MANIFEST_NOT_FOUND` | manifest.json not found | Run dbt compile |
| `MANIFEST_INVALID` | manifest.json is invalid | Check dbt version |
| `AUTHENTICATION_FAILED` | dbt Cloud authentication failed | Check API key |
| `API_RATE_LIMITED` | dbt Cloud API rate limited | Wait and retry |

## Security

### Credentials Management

- **dbt Core**: Uses profiles.yml which may contain credentials
- **dbt Cloud**: API key should be stored securely

**Recommended**:
- Use environment variables for sensitive data
- Use credential stores (Keyring, Vault, etc.)
- Never commit credentials to version control

### Environment Variables

```bash
# dbt Cloud
export DBT_CLOUD_ACCOUNT_ID=12345
export DBT_CLOUD_PROJECT_ID=67890
export DBT_CLOUD_API_KEY=dbtc_abc123...

# dbt Core
export DBT_PROJECT_DIR=/path/to/dbt/project
export DBT_PROFILES_YML=/path/to/profiles.yml
```

## Testing

### Contract Tests

DataTrace provides contract tests to verify dbt integration:

```bash
# Test dbt integration
datatrace test dbt --project /path/to/dbt/project

# Validate manifest parsing
datatrace test dbt-parse --manifest /path/to/manifest.json
```

### Test Cases

1. **Valid dbt project**
   - Given: Valid dbt project with manifest.json
   - When: DataTrace discovers the project
   - Then: All models, sources, and lineage are extracted

2. **Missing manifest**
   - Given: dbt project without manifest.json
   - When: DataTrace attempts discovery
   - Then: Error is returned with suggestion to run dbt compile

3. **Invalid manifest**
   - Given: Corrupted manifest.json
   - When: DataTrace parses the manifest
   - Then: Error is returned with parsing details

4. **dbt Cloud authentication failure**
   - Given: Invalid dbt Cloud API key
   - When: DataTrace connects to dbt Cloud
   - Then: Authentication error is returned

## Performance

### Performance Characteristics

| Operation | Complexity | Typical Duration |
|-----------|------------|------------------|
| Parse manifest | O(n) where n = number of models | < 1 second for 1000 models |
| Extract lineage | O(n + e) where e = number of edges | < 5 seconds for 1000 models |
| Full discovery | O(n) | < 10 seconds for 1000 models |
| Incremental discovery | O(changed) | < 1 second for small changes |

### Caching

DataTrace caches dbt artifacts to improve performance:
- Manifest is cached and only re-read when changed
- Lineage graph is cached and updated incrementally
- Model metadata is cached for fast access

## Best Practices

1. **Run dbt compile before DataTrace discovery**
   - Ensures manifest.json is up to date
   - DataTrace can trigger this automatically with permission

2. **Use incremental discovery**
   - Only process changed models
   - Significantly faster for large projects

3. **Include documentation in dbt models**
   - Description, meta, and column docs are extracted
   - Improves DataTrace metadata quality

4. **Use dbt tags effectively**
   - Tags are extracted and can be used for filtering
   - Helps organize and categorize models

5. **Configure freshness in sources**
   - Freshness configuration is extracted
   - Enables DataTrace to monitor data freshness

## Limitations

1. **Column-level lineage**
   - Limited to what dbt provides
   - SQL parsing for column lineage is experimental

2. **Macros and packages**
   - Macros are cataloged but not executed
   - Package dependencies are not fully traversed

3. **Custom materializations**
   - Custom materializations may not be fully supported
   - Standard materializations (table, view, incremental) are supported

4. **dbt Cloud limitations**
   - Only latest artifacts are available via API
   - Historical artifacts require custom solutions

## Future Enhancements

1. **Real-time integration**
   - Webhook from dbt Cloud on run completion
   - Automatic discovery trigger

2. **Enhanced column lineage**
   - Improved SQL parsing
   - Integration with dbt lineage features

3. **dbt docs integration**
   - Generate DataTrace-compatible documentation
   - Bidirectional sync with dbt docs
