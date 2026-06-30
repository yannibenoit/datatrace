# DataTrace REST API Contract

**Version**: v1.0.0 | **Status**: Draft | **Last Updated**: 2026-06-30

## Overview

The DataTrace REST API provides programmatic access to DataTrace functionality for metadata discovery, lineage tracking, and data asset management. The API follows RESTful principles with JSON request/response formats.

### Base URL

```
https://api.datatrace.example.com/v1
```

### Content Type

All requests and responses use:
```
Content-Type: application/json
```

## Authentication

### Authentication Methods

| Method | Description | Use Case |
|--------|-------------|----------|
| Bearer Token | JWT token in Authorization header | Machine-to-machine |
| Service Account | Service account key | Server-side applications |
| OAuth 2.0 | OAuth 2.0 flow | User-facing applications |

### Authentication Header

```
Authorization: Bearer {access_token}
```

### Scopes

| Scope | Description |
|-------|-------------|
| `datatrace:read` | Read-only access to all DataTrace data |
| `datatrace:write` | Read and write access to DataTrace data |
| `datatrace:admin` | Administrative access including configuration |

## Rate Limiting

| Endpoint | Rate Limit | Burst Limit |
|----------|------------|--------------|
| All endpoints | 100 requests/minute | 10 requests/second |
| Discovery endpoints | 50 requests/minute | 5 requests/second |
| Lineage endpoints | 200 requests/minute | 20 requests/second |

### Rate Limit Headers

```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 30
```

## Error Handling

### HTTP Status Codes

| Code | Name | Description |
|------|------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 204 | No Content | Resource deleted successfully |
| 400 | Bad Request | Invalid request body or parameters |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 409 | Conflict | Resource already exists |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Unexpected server error |

### Error Response Format

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": {
      "field": "field_name",
      "value": "invalid_value",
      "reason": "validation_failed"
    },
    "timestamp": "2026-06-30T10:00:00Z",
    "request_id": "req-abc123"
  }
}
```

### Common Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `AUTHENTICATION_REQUIRED` | 401 | No authentication provided |
| `INSUFFICIENT_PERMISSIONS` | 403 | User lacks required permissions |
| `INVALID_REQUEST` | 400 | Request body is invalid |
| `RESOURCE_NOT_FOUND` | 404 | Requested resource doesn't exist |
| `RESOURCE_EXISTS` | 409 | Resource already exists |
| `VALIDATION_ERROR` | 400 | Field validation failed |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests |
| `INTERNAL_ERROR` | 500 | Unexpected server error |

---

## Endpoints

### Health

#### Get API Health

**Endpoint**: `GET /health`

**Description**: Check API health and connectivity

**Authentication**: None required

**Response**: 200 OK

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-06-30T10:00:00Z",
  "services": {
    "bigquery": "healthy",
    "database": "healthy",
    "cache": "healthy"
  }
}
```

---

### Data Assets

#### List Data Assets

**Endpoint**: `GET /assets`

**Description**: List all data assets with optional filtering

**Scopes**: `datatrace:read`

**Query Parameters**:

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `type` | string | No | Filter by asset type | `bigquery_table` |
| `source_type` | string | No | Filter by source type | `bigquery` |
| `is_active` | boolean | No | Filter by active status | `true` |
| `search` | string | No | Search in name/description | `customer` |
| `page` | integer | No | Page number (default: 1) | `1` |
| `page_size` | integer | No | Results per page (default: 100, max: 1000) | `100` |
| `order_by` | string | No | Order by field (default: `name`) | `created_at` |
| `order_direction` | string | No | Order direction (default: `asc`) | `desc` |

**Response**: 200 OK

```json
{
  "assets": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "customers",
      "type": "bigquery_table",
      "source_type": "bigquery",
      "description": "Customer master data",
      "is_active": true,
      "external_id": "project.dataset.customers",
      "created_at": "2026-06-30T10:00:00Z",
      "updated_at": "2026-06-30T10:00:00Z"
    }
  ],
  "pagination": {
    "total": 100,
    "page": 1,
    "page_size": 100,
    "total_pages": 1
  }
}
```

#### Get Data Asset

**Endpoint**: `GET /assets/{asset_id}`

**Description**: Get details for a specific data asset

**Scopes**: `datatrace:read`

**Response**: 200 OK

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "customers",
  "type": "bigquery_table",
  "source_type": "bigquery",
  "description": "Customer master data",
  "is_active": true,
  "external_id": "project.dataset.customers",
  "connection_id": "conn-123",
  "created_at": "2026-06-30T10:00:00Z",
  "updated_at": "2026-06-30T10:00:00Z",
  "metadata": {
    "owner": {"email": "john@example.com", "name": "John Doe", "team": "data"},
    "classification_level": "PII",
    "freshness_expectation": {"frequency": "daily", "threshold": "24h"}
  }
}
```

#### Create Data Asset

**Endpoint**: `POST /assets`

**Description**: Create a new data asset

**Scopes**: `datatrace:write`

**Request Body**:

```json
{
  "name": "customers",
  "type": "bigquery_table",
  "source_type": "bigquery",
  "description": "Customer master data",
  "external_id": "project.dataset.customers",
  "metadata": {
    "owner": {"email": "john@example.com", "name": "John Doe", "team": "data"}
  }
}
```

**Response**: 201 Created

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "customers",
  "type": "bigquery_table",
  "source_type": "bigquery",
  "description": "Customer master data",
  "is_active": true,
  "external_id": "project.dataset.customers",
  "created_at": "2026-06-30T10:00:00Z",
  "updated_at": "2026-06-30T10:00:00Z"
}
```

#### Update Data Asset

**Endpoint**: `PUT /assets/{asset_id}`

**Description**: Update an existing data asset

**Scopes**: `datatrace:write`

**Request Body**:

```json
{
  "name": "customers_updated",
  "description": "Updated customer master data",
  "metadata": {
    "owner": {"email": "jane@example.com", "name": "Jane Doe", "team": "data"}
  }
}
```

**Response**: 200 OK

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "customers_updated",
  "type": "bigquery_table",
  "source_type": "bigquery",
  "description": "Updated customer master data",
  "is_active": true,
  "external_id": "project.dataset.customers",
  "created_at": "2026-06-30T10:00:00Z",
  "updated_at": "2026-06-30T11:00:00Z"
}
```

#### Delete Data Asset

**Endpoint**: `DELETE /assets/{asset_id}`

**Description**: Delete a data asset (soft delete - marks as inactive)

**Scopes**: `datatrace:write`

**Query Parameters**:

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `hard_delete` | boolean | No | Perform hard delete (default: false) | `false` |

**Response**: 204 No Content

---

### Metadata

#### Get Metadata for Asset

**Endpoint**: `GET /assets/{asset_id}/metadata`

**Description**: Get all metadata for a specific data asset

**Scopes**: `datatrace:read`

**Response**: 200 OK

```json
{
  "metadata": [
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "key": "owner",
      "value": {"email": "john@example.com", "name": "John Doe", "team": "data"},
      "data_type": "json",
      "source": "manual",
      "classification": null,
      "sensitivity_level": null,
      "created_at": "2026-06-30T10:00:00Z",
      "updated_at": "2026-06-30T10:00:00Z"
    },
    {
      "id": "660e8400-e29b-41d4-a716-446655440002",
      "key": "classification_level",
      "value": "PII",
      "data_type": "string",
      "source": "auto_discovered",
      "classification": "PII",
      "sensitivity_level": "high",
      "created_at": "2026-06-30T10:00:00Z",
      "updated_at": "2026-06-30T10:00:00Z"
    }
  ]
}
```

#### Set Metadata

**Endpoint**: `PUT /assets/{asset_id}/metadata/{key}`

**Description**: Set metadata value for a data asset

**Scopes**: `datatrace:write`

**Request Body**:

```json
{
  "value": {"email": "john@example.com", "name": "John Doe", "team": "data"},
  "data_type": "json",
  "source": "manual"
}
```

**Response**: 200 OK

```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "key": "owner",
  "value": {"email": "john@example.com", "name": "John Doe", "team": "data"},
  "data_type": "json",
  "source": "manual",
  "created_at": "2026-06-30T10:00:00Z",
  "updated_at": "2026-06-30T11:00:00Z"
}
```

---

### Lineage

#### Get Lineage Graph

**Endpoint**: `GET /lineage/graph`

**Description**: Get the lineage graph for one or more assets

**Scopes**: `datatrace:read`

**Query Parameters**:

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `asset_id` | string | Yes | Source asset ID |
| `direction` | string | No | Direction to traverse (default: `both`) | `upstream`, `downstream`, `both` |
| `depth` | integer | No | Maximum depth to traverse (default: 5) | `3` |
| `include_columns` | boolean | No | Include column-level lineage (default: false) | `false` |

**Response**: 200 OK

```json
{
  "source_asset": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "raw_customers",
    "type": "bigquery_table"
  },
  "nodes": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "raw_customers",
      "type": "bigquery_table",
      "depth": 0
    },
    {
      "id": "770e8400-e29b-41d4-a716-446655440002",
      "name": "stg_customers",
      "type": "dbt_model",
      "depth": 1,
      "relationship": "transforms"
    },
    {
      "id": "880e8400-e29b-41d4-a716-446655440003",
      "name": "dim_customer",
      "type": "dbt_model",
      "depth": 2,
      "relationship": "transforms"
    }
  ],
  "edges": [
    {
      "id": "990e8400-e29b-41d4-a716-446655440004",
      "source_id": "550e8400-e29b-41d4-a716-446655440000",
      "target_id": "770e8400-e29b-41d4-a716-446655440002",
      "relationship_type": "transforms",
      "transformation_type": "dbt_model"
    },
    {
      "id": "110e8400-e29b-41d4-a716-446655440005",
      "source_id": "770e8400-e29b-41d4-a716-446655440002",
      "target_id": "880e8400-e29b-41d4-a716-446655440003",
      "relationship_type": "transforms",
      "transformation_type": "dbt_model"
    }
  ]
}
```

#### Get Impact Analysis

**Endpoint**: `GET /lineage/impact`

**Description**: Get downstream impact analysis for a source asset

**Scopes**: `datatrace:read`

**Query Parameters**:

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `asset_id` | string | Yes | Source asset ID |
| `depth` | integer | No | Maximum depth (default: 10) | `5` |

**Response**: 200 OK

```json
{
  "source_asset": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "raw_customers",
    "type": "bigquery_table"
  },
  "impact": {
    "direct": [
      {
        "asset_id": "770e8400-e29b-41d4-a716-446655440002",
        "name": "stg_customers",
        "type": "dbt_model",
        "depth": 1
      }
    ],
    "indirect": [
      {
        "asset_id": "880e8400-e29b-41d4-a716-446655440003",
        "name": "dim_customer",
        "type": "dbt_model",
        "depth": 2
      },
      {
        "asset_id": "990e8400-e29b-41d4-a716-446655440004",
        "name": "fct_orders",
        "type": "dbt_model",
        "depth": 2
      }
    ],
    "powerbi_models": [
      {
        "asset_id": "120e8400-e29b-41d4-a716-446655440005",
        "name": "Sales_Mart",
        "type": "powerbi_semantic_model",
        "depth": 3
      }
    ]
  },
  "stats": {
    "total_downstream": 50,
    "dbt_models": 45,
    "powerbi_models": 5,
    "max_depth": 3
  }
}
```

#### Get Lineage Path

**Endpoint**: `GET /lineage/path`

**Description**: Get the shortest path between two assets

**Scopes**: `datatrace:read`

**Query Parameters**:

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `source_id` | string | Yes | Source asset ID |
| `target_id` | string | Yes | Target asset ID |

**Response**: 200 OK

```json
{
  "source": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "raw_customers"
  },
  "target": {
    "id": "880e8400-e29b-41d4-a716-446655440003",
    "name": "dim_customer"
  },
  "path": [
    {
      "asset_id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "raw_customers",
      "type": "bigquery_table",
      "position": 0
    },
    {
      "asset_id": "770e8400-e29b-41d4-a716-446655440002",
      "name": "stg_customers",
      "type": "dbt_model",
      "position": 1
    },
    {
      "asset_id": "880e8400-e29b-41d4-a716-446655440003",
      "name": "dim_customer",
      "type": "dbt_model",
      "position": 2
    }
  ],
  "edges": [
    {
      "id": "990e8400-e29b-41d4-a716-446655440004",
      "source_id": "550e8400-e29b-41d4-a716-446655440000",
      "target_id": "770e8400-e29b-41d4-a716-446655440002",
      "relationship_type": "transforms"
    },
    {
      "id": "110e8400-e29b-41d4-a716-446655440005",
      "source_id": "770e8400-e29b-41d4-a716-446655440002",
      "target_id": "880e8400-e29b-41d4-a716-446655440003",
      "relationship_type": "transforms"
    }
  ],
  "distance": 2
}
```

---

### Discovery

#### Trigger Discovery

**Endpoint**: `POST /discovery/run`

**Description**: Trigger metadata and lineage discovery

**Scopes**: `datatrace:write`

**Request Body**:

```json
{
  "source_types": ["bigquery", "dbt"],
  "project_ids": ["my-project-123"],
  "dbt_projects": [
    {
      "path": "/path/to/dbt/project",
      "name": "my_dbt_project"
    }
  ],
  "full_scan": false,
  "incremental": true
}
```

**Response**: 202 Accepted

```json
{
  "discovery_id": "disc-550e8400-e29b-41d4-a716-446655440000",
  "status": "queued",
  "submitted_at": "2026-06-30T10:00:00Z",
  "source_types": ["bigquery", "dbt"],
  "estimated_duration": "PT10M"
}
```

#### Get Discovery Status

**Endpoint**: `GET /discovery/{discovery_id}/status`

**Description**: Get status of a discovery run

**Scopes**: `datatrace:read`

**Response**: 200 OK

```json
{
  "id": "disc-550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "progress": {
    "current": 100,
    "total": 100
  },
  "stats": {
    "assets_discovered": 50,
    "assets_updated": 10,
    "lineage_edges_created": 200,
    "lineage_edges_updated": 50,
    "errors": 0,
    "warnings": 5
  },
  "started_at": "2026-06-30T10:00:00Z",
  "completed_at": "2026-06-30T10:10:00Z",
  "duration": "PT10M"
}
```

---

### Verification

#### Get Lineage for Verification

**Endpoint**: `GET /verification/lineage`

**Description**: Get lineage edges that need verification

**Scopes**: `datatrace:read`

**Query Parameters**:

| Parameter | Type | Required | Description | Example |
|-----------|------|----------|-------------|---------|
| `status` | string | No | Filter by verification status | `needs_review` |
| `asset_id` | string | No | Filter by asset ID | `550e8400-e29b-41d4-a716-446655440000` |
| `page` | integer | No | Page number | `1` |
| `page_size` | integer | No | Results per page | `100` |

**Response**: 200 OK

```json
{
  "edges": [
    {
      "id": "990e8400-e29b-41d4-a716-446655440004",
      "source_id": "550e8400-e29b-41d4-a716-446655440000",
      "source_name": "raw_customers",
      "target_id": "770e8400-e29b-41d4-a716-446655440002",
      "target_name": "stg_customers",
      "relationship_type": "transforms",
      "verification_status": "needs_review",
      "discovered_at": "2026-06-30T10:00:00Z",
      "verified_at": null
    }
  ],
  "pagination": {
    "total": 10,
    "page": 1,
    "page_size": 100
  }
}
```

#### Verify Lineage

**Endpoint**: `POST /verification/lineage/{edge_id}`

**Description**: Verify a lineage edge

**Scopes**: `datatrace:write`

**Request Body**:

```json
{
  "status": "verified",
  "verified_by": "john@example.com",
  "notes": "Verified against dbt manifest and source code"
}
```

**Response**: 200 OK

```json
{
  "id": "990e8400-e29b-41d4-a716-446655440004",
  "verification_status": "verified",
  "verified_at": "2026-06-30T11:00:00Z",
  "verified_by": "john@example.com",
  "notes": "Verified against dbt manifest and source code"
}
```

---

## Webhooks

### Webhook Events

DataTrace can emit webhook events for important changes. Configure webhooks through the admin API.

**Webhook Payload**:

```json
{
  "event": "lineage.updated",
  "timestamp": "2026-06-30T10:00:00Z",
  "data": {
    "edge_id": "990e8400-e29b-41d4-a716-446655440004",
    "source_id": "550e8400-e29b-41d4-a716-446655440000",
    "target_id": "770e8400-e29b-41d4-a716-446655440002"
  },
  "metadata": {
    "webhook_id": "wh-123",
    "attempt": 1
  }
}
```

**Supported Events**:
- `asset.created` - New asset discovered
- `asset.updated` - Asset metadata updated
- `asset.deleted` - Asset deleted
- `lineage.created` - New lineage edge created
- `lineage.updated` - Lineage edge updated
- `lineage.deleted` - Lineage edge deleted
- `lineage.verified` - Lineage edge verified
- `discovery.completed` - Discovery run completed
- `verification.needed` - Lineage needs verification

---

## Schemas

### AssetType Enum

```json
{
  "type": "string",
  "enum": [
    "bigquery_table",
    "bigquery_view", 
    "bigquery_materialized_view",
    "bigquery_external",
    "dbt_model",
    "dbt_source",
    "dbt_seed",
    "dbt_snapshot",
    "dbt_analysis",
    "powerbi_semantic_model",
    "powerbi_report",
    "external_database",
    "api",
    "file",
    "other"
  ]
}
```

### SourceType Enum

```json
{
  "type": "string",
  "enum": ["bigquery", "dbt", "powerbi", "other"]
}
```

### RelationshipType Enum

```json
{
  "type": "string",
  "enum": [
    "transforms",
    "depends_on", 
    "feeds_into",
    "references",
    "materializes",
    "copies",
    "aggregates"
  ]
}
```

### VerificationStatus Enum

```json
{
  "type": "string",
  "enum": [
    "auto_discovered",
    "needs_review", 
    "verified",
    "rejected"
  ]
}

### SensitivityLevel Enum

```json
{
  "type": "string",
  "enum": ["high", "medium", "low"]
}
```

### MetadataSource Enum

```json
{
  "type": "string",
  "enum": [
    "auto_discovered",
    "manual", 
    "dbt",
    "powerbi",
    "user_provided"
  ]
}

### DataType Enum

```json
{
  "type": "string",
  "enum": ["string", "number", "boolean", "json", "date", "timestamp"]
}
```
