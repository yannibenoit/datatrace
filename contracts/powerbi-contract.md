# DataTrace Power BI Integration Contract

**Version**: v1.0.0 | **Status**: Draft | **Last Updated**: 2026-06-30

## Overview

This contract defines how DataTrace integrates with Microsoft Power BI to extract metadata about semantic models (datasets), tables, relationships, and measures. This enables end-to-end lineage tracking from BigQuery sources through dbt transformations to Power BI consumption.

## Integration Methods

### Power BI REST API

DataTrace uses the Power BI REST API to extract metadata from Power BI workspaces.

**API Endpoint**: `https://api.powerbi.com/v1.0/myorg/`

**API Documentation**: https://learn.microsoft.com/en-us/rest/api/power-bi/

### Power BI XMLA Endpoint (Optional)

For more detailed metadata, DataTrace can use the XMLA endpoint.

**XMLA Endpoint**: `powerbi://api.powerbi.com/v1.0/myorg/{workspace}`

## Connection Configuration

```yaml
# In DataTrace config file
connections:
  - name: my-powerbi
    type: powerbi
    workspace: my-workspace-id  # Workspace UUID
    
    # Authentication
    authentication:
      type: service_principal
      client_id: my-client-id
      tenant_id: my-tenant-id
      # client_secret: stored securely
      
    # OR
    authentication:
      type: user
      username: user@example.com
      password: secure-password  # Or use interactive auth
```

## Extracted Information

### From REST API

#### Workspace Information

```json
{
  "id": "workspace-uuid",
  "name": "Analytics Workspace",
  "type": "Workspace",
  "isReadOnly": false,
  "isOnDedicatedCapacity": true
}
```

#### Semantic Model (Dataset) Information

```json
{
  "id": "dataset-uuid",
  "name": "Sales_Mart",
  "addRowsPermissionsEnabled": true,
  "configuredBy": "john@example.com",
  "defaultMode": "Push",
  "isEffectiveIdentityRequired": false,
  "isOnPremGatewayRequired": false,
  "isQpuEnabled": false,
  "targetStorageMode": "Import",
  "usesDataflow": false
}
```

#### Table Information

```json
{
  "name": "Sales",
  "isHidden": false,
  "isPrivate": false,
  "source": {
    "expression": "= SharePoint.Contents(\"https://...\")"
  },
  "measures": [
    {
      "name": "Total Sales",
      "expression": "SUM(Sales[Amount])"
    }
  ],
  "columns": [
    {
      "name": "OrderDate",
      "dataType": "DateTime",
      "isHidden": false,
      "isKey": false,
      "sortDirection": "None"
    }
  ]
}
```

#### Relationship Information

```json
{
  "name": "Sales_to_Date",
  "active": true,
  "cardinality": "ManyToOne",
  "crossFilterDirection": "Both",
  "fromTable": "Sales",
  "fromColumn": "OrderDate",
  "toTable": "Date",
  "toColumn": "Date"
}
```

#### Refresh Schedule

```json
{
  "frequency": "Daily",
  "time": "02:00",
  "enabled": true,
  "notifyOption": "MailOnFailure"
}
```

## API Interface

### Python Interface

```python
from datatrace.integrations.powerbi import PowerBIConnection

# Initialize connection
conn = PowerBIConnection(
    workspace_id="workspace-uuid",
    client_id="my-client-id",
    tenant_id="my-tenant-id"
)

# Get all semantic models (datasets)
datasets = conn.get_datasets()

# Get dataset metadata
dataset = conn.get_dataset(dataset_id="dataset-uuid")

# Get tables in dataset
tables = conn.get_tables(dataset_id="dataset-uuid")

# Get relationships in dataset
relationships = conn.get_relationships(dataset_id="dataset-uuid")

# Get measures in table
measures = conn.get_measures(dataset_id="dataset-uuid", table_name="Sales")

# Get refresh history
refresh_history = conn.get_refresh_history(dataset_id="dataset-uuid")
```

## Authentication

### Service Principal Authentication (Recommended)

```python
from msal import ConfidentialClientApplication

# Create confidential client
app = ConfidentialClientApplication(
    client_id="my-client-id",
    client_credential="my-client-secret",
    authority=f"https://login.microsoftonline.com/{tenant_id}"
)

# Get token
result = app.acquire_token_for_client(scopes=["https://analysis.windows.net/powerbi/api/.default"])
access_token = result["access_token"]
```

### User Authentication

```python
from msal import PublicClientApplication

# Create public client
app = PublicClientApplication(
    client_id="my-client-id",
    authority=f"https://login.microsoftonline.com/{tenant_id}"
)

# Get token interactively
result = app.acquire_token_interactive(scopes=["https://analysis.windows.net/powerbi/api/.default"])
access_token = result["access_token"]
```

## Metadata Schema

### PowerBISemanticModel Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "workspace_id": {"type": "string", "format": "uuid"},
    "workspace_name": {"type": "string"},
    "dataset_id": {"type": "string", "format": "uuid"},
    "dataset_name": {"type": "string"},
    "configured_by": {"type": "string"},
    "default_mode": {"type": "string", "enum": ["Push", "Pull", "LiveConnect"]},
    "storage_mode": {"type": "string", "enum": ["Import", "DirectQuery", "Dual", "Push"]},
    "is_on_premium_capacity": {"type": "boolean"},
    "created_date": {"type": "string", "format": "date-time"},
    "last_refresh_date": {"type": "string", "format": "date-time"},
    "refresh_schedule": {"type": "object"},
    "tables": {
      "type": "array",
      "items": {"$ref": "#/definitions/table"}
    },
    "relationships": {
      "type": "array",
      "items": {"$ref": "#/definitions/relationship"}
    },
    "measures": {
      "type": "array",
      "items": {"$ref": "#/definitions/measure"}
    }
  },
  "definitions": {
    "table": {
      "type": "object",
      "properties": {
        "name": {"type": "string"},
        "display_name": {"type": "string"},
        "description": {"type": "string"},
        "is_hidden": {"type": "boolean"},
        "row_count": {"type": "integer"},
        "columns": {
          "type": "array",
          "items": {"type": "object"}
        },
        "measures": {
          "type": "array",
          "items": {"type": "object"}
        }
      }
    },
    "relationship": {
      "type": "object",
      "properties": {
        "name": {"type": "string"},
        "from_table": {"type": "string"},
        "from_column": {"type": "string"},
        "to_table": {"type": "string"},
        "to_column": {"type": "string"},
        "cardinality": {"type": "string", "enum": ["OneToMany", "ManyToOne", "OneToOne", "ManyToMany"]},
        "cross_filter_direction": {"type": "string", "enum": ["OneWay", "Both", "Automatic"]},
        "is_active": {"type": "boolean"}
      }
    },
    "measure": {
      "type": "object",
      "properties": {
        "name": {"type": "string"},
        "display_name": {"type": "string"},
        "expression": {"type": "string"},
        "description": {"type": "string"},
        "is_hidden": {"type": "boolean"}
      }
    }
  },
  "required": ["workspace_id", "dataset_id", "dataset_name"]
}
```

## Lineage Integration

### Connecting Power BI to dbt

DataTrace creates lineage between dbt models and Power BI semantic models:

```
BigQuery Table -> dbt Source -> dbt Model -> Power BI Semantic Model -> Power BI Table
```

**Discovery Methods**:

1. **Connection-based**: Power BI semantic model uses BigQuery as data source
   - Extract connection string
   - Parse BigQuery table references
   - Match to dbt models

2. **Naming convention**: Power BI table names match dbt model names
   - Direct name matching
   - Pattern-based matching

3. **Manual mapping**: User-defined mappings
   - Explicit mappings in configuration
   - Override automatic discovery

### Lineage Relationship Types

| Relationship | Description | Example |
|--------------|-------------|---------|
| `feeds_into` | dbt model feeds into Power BI semantic model | dbt dim_customer -> PBI Sales_Mart |
| `consumes` | Power BI semantic model consumes dbt model | PBI Sales_Mart -> dbt fct_sales |

## Error Handling

### Power BI Integration Errors

| Error Code | Description | Recovery |
|------------|-------------|----------|
| `WORKSPACE_NOT_FOUND` | Power BI workspace not found | Verify workspace ID |
| `DATASET_NOT_FOUND` | Semantic model not found | Verify dataset ID |
| `AUTHENTICATION_FAILED` | Authentication failed | Check credentials |
| `PERMISSION_DENIED` | Permission denied | Check Power BI permissions |
| `API_RATE_LIMITED` | API rate limit exceeded | Wait and retry |
| `THROTTLED` | Request throttled | Implement backoff |

## Security

### Azure AD Permissions Required

DataTrace requires the following Azure AD permissions:

- `https://analysis.windows.net/powerbi/api/.default` - Full API access
- `https://analysis.windows.net/powerbi/api/Workspace.Read.All` - Read all workspaces
- `https://analysis.windows.net/powerbi/api/Dataset.Read.All` - Read all datasets
- `https://analysis.windows.net/powerbi/api/Dataflow.Read.All` - Read all dataflows

### Service Principal Setup

```bash
# Register Azure AD application
az ad app create --display-name "DataTrace App"

# Create service principal
az ad sp create --id <application-id>

# Assign permissions (in Azure Portal)
# 1. Go to Azure Portal -> Azure Active Directory -> App registrations
# 2. Select your app
# 3. Go to API permissions
# 4. Add Power BI permissions
# 5. Grant admin consent

# Store credentials securely
export POWERBI_CLIENT_ID=my-client-id
export POWERBI_TENANT_ID=my-tenant-id
# Store client secret in secure vault
```

## Performance

### Performance Characteristics

| Operation | Typical Duration | Notes |
|-----------|------------------|-------|
| List workspaces | < 1 second | |
| List datasets in workspace | < 1 second | |
| Get dataset metadata | < 1 second | |
| Get tables in dataset | < 1 second | |
| Get relationships | < 1 second | |
| Get refresh history | < 1 second | |
| Full workspace scan | < 10 seconds | For typical workspace |

### API Rate Limits

- **Per user**: 60 requests per minute
- **Per application**: Higher limits available
- **Burst**: 10 requests per second

### Optimization Techniques

1. **Parallel requests**: Multiple datasets can be queried in parallel
2. **Caching**: Metadata is cached to avoid repeated API calls
3. **Incremental updates**: Only query for changed datasets
4. **Batch requests**: Combine multiple requests when possible

## Best Practices

1. **Use service principal with least privilege**
   - Only grant necessary permissions
   - Use workspace-level permissions where possible

2. **Enable Power BI Premium**
   - Better performance for large datasets
   - More frequent refreshes

3. **Use consistent naming conventions**
   - Helps with automatic lineage discovery
   - Makes manual mapping easier

4. **Document data sources**
   - Include connection information in Power BI
   - Helps DataTrace trace lineage back to source

5. **Monitor refresh schedules**
   - Track refresh history
   - Alert on failed refreshes

## Testing

### Contract Tests

```bash
# Test Power BI connection
datatrace test powerbi --workspace workspace-uuid

# Validate dataset extraction
datatrace test powerbi-dataset --workspace workspace-uuid --dataset dataset-uuid

# Test lineage discovery
datatrace test powerbi-lineage --workspace workspace-uuid
```

### Test Cases

1. **Valid workspace access**
   - Given: Valid Power BI workspace with DataTrace permissions
   - When: DataTrace connects to Power BI
   - Then: All datasets are listed successfully

2. **Dataset with tables**
   - Given: Dataset with multiple tables and relationships
   - When: DataTrace discovers dataset
   - Then: All tables, relationships, and measures are extracted

3. **BigQuery-connected dataset**
   - Given: Dataset connected to BigQuery
   - When: DataTrace extracts connection information
   - Then: BigQuery connection string is parsed

4. **Missing permissions**
   - Given: Workspace without DataTrace permissions
   - When: DataTrace attempts to list datasets
   - Then: Permission denied error is returned

## Limitations

1. **DirectQuery datasets**
   - Metadata extraction may be limited
   - Lineage may be incomplete

2. **Shared datasets**
   - May not have access to underlying connections
   - Lineage may be partial

3. **Power BI Report Server**
   - On-premises deployment not supported
   - Cloud-only currently

4. **Embedded analytics**
   - May require additional permissions
   - Limited metadata access

5. **Personal workspaces**
   - May not be accessible via service principal
   - Requires user authentication

## Future Enhancements

1. **Power BI Dataflows**
   - Extract metadata from Dataflows
   - Track lineage through Dataflow entities

2. **Report metadata**
   - Extract report structure
   - Track which datasets are used in reports

3. **Usage analytics**
   - Track report usage
   - Monitor popular datasets

4. **Impact analysis**
   - Analyze impact of schema changes on reports
   - Predict which reports will break
