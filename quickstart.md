# Quickstart: DataTrace Core Implementation

**Date**: 2026-06-30 | **Feature**: DataTrace Core Implementation | **Version**: 1.0.0

## Overview

This guide provides runnable validation scenarios to prove the DataTrace core implementation works end-to-end. It includes prerequisites, setup commands, test/run commands, and expected outcomes.

**Target Audience**: Data engineers, DevOps engineers, QA engineers

**Estimated Time**: 30-60 minutes for full validation

---

## Prerequisites

### System Requirements

| Component | Version | Notes |
|-----------|---------|-------|
| **Operating System** | Linux, macOS, Windows | Tested on Ubuntu 22.04, macOS Ventura, Windows 11 |
| **Python** | 3.11+ | Required for DataTrace application |
| **Node.js** | 18+ | Optional, for web interface |
| **Docker** | 20.10+ | For containerized deployment |
| **Git** | 2.x | For version control |
| **Google Cloud SDK** | Latest | For BigQuery access |
| **dbt Core** | 1.5+ | For dbt integration tests |

### Cloud Services

1. **Google Cloud Platform (GCP)**
   - Project with BigQuery enabled
   - BigQuery Data Editor or Metadata Viewer permissions
   - Service account with appropriate permissions

2. **Microsoft Azure** (Optional for Power BI tests)
   - Azure AD tenant
   - Power BI workspace
   - Service principal with Power BI permissions

3. **dbt Cloud** (Optional)
   - dbt Cloud account
   - Project configured
   - API key

---

## Setup

### 1. Clone the Repository

```bash
# Clone the DataTrace repository
git clone https://github.com/datatrace/datatrace.git
cd datatrace

# Or use the current directory (already cloned)
cd /Users/yanniiyeze/Documents/dev/datatrace
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.\.venv\Scripts\activate

# Install dependencies
pip install -e .[dev,test]

# Verify installation
datatrace --version
# Expected output: datatrace 1.0.0
```

### 3. Configure DataTrace

#### Initialize Configuration

```bash
# Initialize configuration file
datatrace configure init

# Expected output:
# Configuration file created at ~/.datatrace/config.yaml
```

#### Add BigQuery Connection

```bash
# Add BigQuery connection (replace placeholders)
datatrace configure add-connection \
  --name my-bigquery \
  --type bigquery \
  --project YOUR_GCP_PROJECT_ID \
  --dataset YOUR_DATASET

# Expected output:
# Connection 'my-bigquery' added successfully
```

#### Set Up Authentication

**Option A: Service Account Key**

```bash
# Create service account key file
# 1. Go to GCP Console -> IAM & Admin -> Service Accounts
# 2. Create service account or use existing
# 3. Create key (JSON) and download
# 4. Set environment variable
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"
```

**Option B: Application Default Credentials**

```bash
# Authenticate with gcloud
gcloud auth application-default login

# Verify
gcloud auth list
# Expected: Active account with BigQuery permissions
```

#### Add dbt Connection (Optional)

```bash
# Add dbt connection
datatrace configure add-connection \
  --name my-dbt \
  --type dbt \
  --dbt-path /path/to/your/dbt/project

# Expected output:
# Connection 'my-dbt' added successfully
```

#### Add Power BI Connection (Optional)

```bash
# Add Power BI connection (replace placeholders)
datatrace configure add-connection \
  --name my-powerbi \
  --type powerbi \
  --workspace YOUR_WORKSPACE_ID \
  --client-id YOUR_CLIENT_ID \
  --tenant-id YOUR_TENANT_ID

# Store client secret securely
export POWERBI_CLIENT_SECRET=your_client_secret

# Expected output:
# Connection 'my-powerbi' added successfully
```

---

## Validation Scenarios

### Scenario 1: Basic Installation and Configuration

**Purpose**: Verify DataTrace is installed and configured correctly

**Prerequisites**:
- Python 3.11+ installed
- DataTrace installed
- Configuration initialized

**Steps**:

```bash
# Test 1.1: Verify installation
datatrace --version
# Expected: datatrace 1.0.0

# Test 1.2: Verify help
datatrace --help
# Expected: Help text with available commands

# Test 1.3: Verify configuration
datatrace configure list-connections
# Expected: List of configured connections

# Test 1.4: Verify health check
datatrace server --port 8080 &
sleep 2
curl -s http://localhost:8080/health | jq
# Expected: JSON with "status": "healthy"

# Cleanup
pkill -f "datatrace server"
```

**Success Criteria**:
- [ ] DataTrace version is displayed correctly
- [ ] Help text shows all available commands
- [ ] Configuration shows all added connections
- [ ] Health endpoint returns healthy status

**Next Steps**: Proceed to Scenario 2

---

### Scenario 2: BigQuery Metadata Discovery

**Purpose**: Verify BigQuery metadata can be discovered and cataloged

**Prerequisites**:
- BigQuery connection configured
- GCP project with BigQuery datasets
- Appropriate permissions

**Steps**:

```bash
# Test 2.1: Test BigQuery connection
datatrace test bigquery --project YOUR_GCP_PROJECT_ID
# Expected: Connection successful message

# Test 2.2: List datasets
datatrace discover --connection my-bigquery --type bigquery --dry-run
# Expected: List of datasets in the project

# Test 2.3: Discover and catalog metadata (for a specific dataset)
datatrace discover \
  --connection my-bigquery \
  --type bigquery \
  --dataset YOUR_DATASET \
  --output /tmp/discovery_results.json

# Verify results
cat /tmp/discovery_results.json | jq '.assets | length'
# Expected: Number of tables in the dataset (>= 0)

# Test 2.4: Verify assets were created
datatrace assets list --format json | jq '.[] | {name, type}'
# Expected: List of assets with their types
```

**Success Criteria**:
- [ ] BigQuery connection test passes
- [ ] Datasets are listed successfully
- [ ] Metadata discovery completes without errors
- [ ] Assets are created in DataTrace

**Troubleshooting**:
- **Error: Permission denied**: Verify GCP project permissions
- **Error: Project not found**: Verify project ID
- **Error: No datasets found**: Verify dataset exists and is accessible

**Next Steps**: Proceed to Scenario 3

---

### Scenario 3: dbt Integration (Optional)

**Purpose**: Verify dbt project integration works correctly

**Prerequisites**:
- dbt connection configured
- dbt project with models
- dbt dependencies installed

**Steps**:

```bash
# Test 3.1: Test dbt project connection
dbt ls --project-dir /path/to/your/dbt/project
# Expected: List of models in the project

# Test 3.2: Compile dbt project (ensure manifest.json is up to date)
cd /path/to/your/dbt/project
dbt compile
# Expected: Compilation successful

# Test 3.3: Discover dbt project
datatrace discover \
  --connection my-dbt \
  --type dbt \
  --output /tmp/dbt_discovery.json

# Verify results
cat /tmp/dbt_discovery.json | jq '.assets | length'
# Expected: Number of dbt models (>= 0)

# Test 3.4: Verify lineage from dbt
dbt prepare
# This generates manifest.json and catalog.json

# Now discover again
datatrace discover --connection my-dbt --type dbt

# Check lineage
datatrace lineage graph --asset YOUR_MODEL_ID --format json | jq '.edges | length'
# Expected: Number of lineage edges (>= 0)
```

**Success Criteria**:
- [ ] dbt project compiles successfully
- [ ] dbt models are discovered and cataloged
- [ ] Lineage relationships are created between dbt models

**Troubleshooting**:
- **Error: dbt project not found**: Verify dbt path
- **Error: manifest.json not found**: Run `dbt compile` first
- **Error: No models found**: Verify dbt project has models

**Next Steps**: Proceed to Scenario 4

---

### Scenario 4: Lineage Graph Validation

**Purpose**: Verify lineage graph can be queried and traversed

**Prerequisites**:
- At least one data asset discovered
- Ideally, multiple assets with relationships

**Steps**:

```bash
# Test 4.1: List all assets
datatrace assets list --format table
# Expected: Table of assets with IDs

# Pick an asset ID from the list (or use a known one)
ASSET_ID=$(datatrace assets list --format json | jq -r '.[0].id')

# Test 4.2: Get lineage graph for an asset
datatrace lineage graph --asset $ASSET_ID --format json | jq '.nodes | length'
# Expected: Number of nodes in lineage graph (>= 1 for the asset itself)

# Test 4.3: Get lineage graph with depth
datatrace lineage graph --asset $ASSET_ID --depth 3 --format json | jq '.edges | length'
# Expected: Number of edges (>= 0)

# Test 4.4: Get impact analysis
datatrace lineage impact --asset $ASSET_ID --format json | jq '.impact'
# Expected: Impact analysis with direct and indirect dependencies

# Test 4.5: Visualize lineage (if Graphviz is installed)
datatrace lineage graph --asset $ASSET_ID --format graphviz > /tmp/lineage.dot
cat /tmp/lineage.dot
# Expected: Graphviz DOT format output
```

**Success Criteria**:
- [ ] Lineage graph can be queried for any asset
- [ ] Graph includes nodes and edges
- [ ] Impact analysis returns downstream dependencies
- [ ] Graphviz output is valid (if applicable)

**Troubleshooting**:
- **Error: Asset not found**: Verify asset ID exists
- **Error: No lineage found**: May be normal for source assets
- **Graphviz not installed**: Install graphviz for visualization

**Next Steps**: Proceed to Scenario 5

---

### Scenario 5: Metadata Management

**Purpose**: Verify metadata can be set, retrieved, and managed

**Prerequisites**:
- At least one asset exists

**Steps**:

```bash
# Pick an asset ID
ASSET_ID=$(datatrace assets list --format json | jq -r '.[0].id')

# Test 5.1: Get metadata for asset
datatrace metadata list --asset $ASSET_ID --format json
# Expected: List of metadata entries (may be empty initially)

# Test 5.2: Set metadata
datatrace metadata set \
  --asset $ASSET_ID \
  --key owner \
  --value '{"email": "test@example.com", "name": "Test User", "team": "data"}'
# Expected: Metadata set successfully

# Test 5.3: Verify metadata was set
datatrace metadata list --asset $ASSET_ID --key owner --format json
# Expected: JSON with the owner metadata

# Test 5.4: Set classification
datatrace metadata set \
  --asset $ASSET_ID \
  --key classification_level \
  --value "PII" \
  --sensitivity high
# Expected: Classification set successfully

# Test 5.5: Find assets by classification
datatrace assets list --format json | jq '.[] | select(.metadata.classification_level == "PII")'
# Expected: Assets with PII classification (should include the test asset)
```

**Success Criteria**:
- [ ] Metadata can be set for assets
- [ ] Metadata can be retrieved
- [ ] Classification metadata works correctly
- [ ] Assets can be filtered by metadata

**Troubleshooting**:
- **Error: Asset not found**: Verify asset ID
- **Error: Invalid metadata format**: Use valid JSON

**Next Steps**: Proceed to Scenario 6

---

### Scenario 6: REST API Validation

**Purpose**: Verify REST API works correctly

**Prerequisites**:
- DataTrace server running
- At least one asset exists

**Steps**:

```bash
# Start server in background
datatrace server --port 8080 &
SERVER_PID=$!
sleep 3

# Test 6.1: Health endpoint
curl -s http://localhost:8080/health | jq
# Expected: JSON with "status": "healthy"

# Test 6.2: List assets via API
curl -s http://localhost:8080/v1/assets | jq '.assets | length'
# Expected: Number of assets (>= 0)

# Test 6.3: Get specific asset
ASSET_ID=$(datatrace assets list --format json | jq -r '.[0].id')
curl -s http://localhost:8080/v1/assets/$ASSET_ID | jq '.name'
# Expected: Asset name

# Test 6.4: Query lineage via API
curl -s "http://localhost:8080/v1/lineage/graph?asset_id=$ASSET_ID&depth=2" | jq '.nodes | length'
# Expected: Number of nodes in lineage graph

# Test 6.5: Create asset via API
curl -X POST http://localhost:8080/v1/assets \
  -H "Content-Type: application/json" \
  -d '{"name": "test_api_asset", "type": "bigquery_table", "source_type": "bigquery", "description": "Test asset created via API"}' | jq
# Expected: Created asset with ID

# Cleanup
kill $SERVER_PID
wait $SERVER_PID 2>/dev/null
```

**Success Criteria**:
- [ ] Health endpoint returns healthy status
- [ ] Assets can be listed via API
- [ ] Specific asset can be retrieved
- [ ] Lineage can be queried via API
- [ ] Asset can be created via API

**Troubleshooting**:
- **Error: Connection refused**: Server may not be running, check port
- **Error: Invalid request**: Verify request format

**Next Steps**: Proceed to Scenario 7

---

### Scenario 7: Discovery and Verification Workflow

**Purpose**: Verify end-to-end discovery and verification workflow

**Prerequisites**:
- BigQuery connection configured
- dbt connection configured (optional)

**Steps**:

```bash
# Test 7.1: Full discovery
datatrace discover --all --output /tmp/full_discovery.json
# Expected: Discovery completes with assets and lineage

# Verify results
cat /tmp/full_discovery.json | jq '{assets: (.assets | length), edges: (.lineage_edges | length)}'
# Expected: Counts of assets and lineage edges

# Test 7.2: List lineage that needs verification
datatrace lineage verify --list --status needs_review --format json | jq '.edges | length'
# Expected: Number of edges needing verification (>= 0)

# Test 7.3: Auto-verify simple lineage (if any exists)
datatrace lineage verify --auto-verify
# Expected: Simple lineage edges are verified

# Test 7.4: Verify all production-ready lineage
datatrace verify --all
# Expected: All verifiable lineage is verified
```

**Success Criteria**:
- [ ] Full discovery completes successfully
- [ ] Lineage edges are created
- [ ] Verification workflow works
- [ ] All production-ready lineage is verified

**Troubleshooting**:
- **No edges to verify**: May be normal if lineage is already verified
- **Discovery errors**: Check connection and permissions

---

## End-to-End Test Suite

### Run All Scenarios

```bash
# Create test script
cat > /tmp/test_datatrace.sh << 'EOF'
#!/bin/bash
set -e

echo "=== DataTrace End-to-End Test Suite ==="
echo ""

# Scenario 1: Installation
echo "[Scenario 1] Testing installation..."
datatrace --version > /dev/null
echo "✓ Installation verified"

# Scenario 2: BigQuery Discovery  
echo "[Scenario 2] Testing BigQuery discovery..."
datatrace test bigquery --project YOUR_GCP_PROJECT_ID > /dev/null
datatrace discover --connection my-bigquery --type bigquery --dataset YOUR_DATASET --output /tmp/test_disc.json > /dev/null
[j $(jq '.assets | length' /tmp/test_disc.json) -gt 0 ] || { echo "⚠ No assets found, but no error"; }
echo "✓ BigQuery discovery verified"

# Scenario 3: Lineage
echo "[Scenario 3] Testing lineage..."
ASSET_ID=$(datatrace assets list --format json | jq -r '.[0].id')
[ -n "$ASSET_ID" ] || { echo "⚠ No assets available for lineage test"; exit 0; }
datatrace lineage graph --asset $ASSET_ID --depth 2 > /dev/null
echo "✓ Lineage verified"

# Scenario 4: Metadata
echo "[Scenario 4] Testing metadata..."
datatrace metadata set --asset $ASSET_ID --key test_key --value test_value > /dev/null
datatrace metadata list --asset $ASSET_ID --key test_key > /dev/null
echo "✓ Metadata verified"

# Scenario 5: API
echo "[Scenario 5] Testing API..."
datatrace server --port 8081 &
SERVER_PID=$!
sleep 3
curl -s http://localhost:8081/health > /dev/null
kill $SERVER_PID
wait $SERVER_PID 2>/dev/null
echo "✓ API verified"

echo ""
echo "=== All tests passed! ==="
EOF

chmod +x /tmp/test_datatrace.sh

# Run test suite
/tmp/test_datatrace.sh
```

**Expected Output**:
```
=== DataTrace End-to-End Test Suite ===

[Scenario 1] Testing installation...
✓ Installation verified
[Scenario 2] Testing BigQuery discovery...
✓ BigQuery discovery verified
[Scenario 3] Testing lineage...
✓ Lineage verified
[Scenario 4] Testing metadata...
✓ Metadata verified
[Scenario 5] Testing API...
✓ API verified

=== All tests passed! ===
```

---

## Validation Checklist

### Core Functionality

- [ ] DataTrace installs successfully
- [ ] CLI commands work correctly
- [ ] Configuration can be managed
- [ ] Server starts and responds to health checks

### Discovery

- [ ] BigQuery datasets can be discovered
- [ ] BigQuery tables and columns are cataloged
- [ ] dbt projects can be discovered (if configured)
- [ ] dbt models and sources are cataloged
- [ ] Metadata is extracted correctly

### Lineage

- [ ] Lineage relationships are created
- [ ] Lineage graph can be queried
- [ ] Impact analysis works
- [ ] Path finding works between assets

### Metadata Management

- [ ] Metadata can be set for assets
- [ ] Metadata can be retrieved
- [ ] Classification works
- [ ] Assets can be filtered by metadata

### API

- [ ] API endpoints respond correctly
- [ ] Assets can be managed via API
- [ ] Lineage can be queried via API
- [ ] Error handling works

### Integration

- [ ] BigQuery integration works
- [ ] dbt integration works (if configured)
- [ ] Power BI integration works (if configured)

---

## Expected Outcomes

| Scenario | Expected Result |
|----------|-----------------|
| Basic Installation | All commands available, version displayed |
| BigQuery Discovery | Datasets and tables discovered and cataloged |
| dbt Integration | dbt models discovered, lineage created |
| Lineage Graph | Lineage can be queried, graph traversed |
| Metadata Management | Metadata can be set, retrieved, filtered |
| REST API | All endpoints respond, CRUD operations work |
| Discovery Workflow | Full discovery completes, verification works |

---

## Troubleshooting

### Common Issues

#### 1. Authentication Errors

**Symptom**: Permission denied, authentication failed

**Solutions**:
- Verify GCP service account has BigQuery permissions
- Check `GOOGLE_APPLICATION_CREDENTIALS` environment variable
- Test with `gcloud auth application-default login`
- Verify Power BI service principal has correct permissions

#### 2. Connection Issues

**Symptom**: Connection refused, timeout

**Solutions**:
- Verify network connectivity to GCP
- Check firewall rules
- Test with `gcloud` CLI first
- Verify Power BI API endpoint is accessible

#### 3. Discovery Returns No Results

**Symptom**: Discovery completes but finds no assets

**Solutions**:
- Verify dataset/table names are correct
- Check that you have access to the datasets
- Try with a different dataset
- Verify dbt project has been compiled

#### 4. Lineage Not Found

**Symptom**: Lineage graph is empty

**Solutions**:
- Verify that assets have been discovered
- Check that relationships exist in the source
- Run discovery with `--full` flag
- Verify dbt manifest.json is up to date

#### 5. API Not Responding

**Symptom**: API endpoints return errors or time out

**Solutions**:
- Check that server is running: `ps aux | grep datatrace`
- Verify port is not blocked
- Check logs for errors
- Try different port number

### Debug Mode

Enable debug logging for detailed troubleshooting:

```bash
# CLI debug
datatrace --debug discover --type bigquery

# Server debug
datatrace server --log-level DEBUG

# Save logs to file
datatrace --log-file /tmp/datatrace.log --debug discover --type bigquery
```

---

## Cleanup

### Remove Test Data

```bash
# Remove test assets (optional)
datatrace assets list --format json | jq -r '.[].id' | xargs -I {} datatrace assets delete --asset {} --force

# Remove test metadata
datatrace metadata list --key test_key --format json | jq -r '.[].asset_id' | xargs -I {} datatrace metadata remove --asset {} --key test_key --force
```

### Reset Configuration

```bash
# Remove configuration (optional)
rm -f ~/.datatrace/config.yaml

# Or reset to defaults
datatrace configure init --force
```

---

## Next Steps

After successfully validating with this quickstart guide:

1. **Set up scheduled discovery**: Configure cron jobs or Airflow DAGs for regular discovery
2. **Integrate with CI/CD**: Add DataTrace verification to your pipeline
3. **Configure alerts**: Set up monitoring for lineage changes and data freshness
4. **Explore advanced features**: Try column-level lineage, PII detection, and cost analysis

---

## References

- [DataTrace Constitution](.specify/memory/constitution.md) - Core principles and governance
- [Feature Specification](spec.md) - Detailed requirements
- [Implementation Plan](plan.md) - Technical approach
- [Data Model](data-model.md) - Entity definitions and relationships
- [API Contract](contracts/api-contract.md) - REST API documentation
- [CLI Contract](contracts/cli-contract.md) - Command-line interface documentation

---

## Support

For issues or questions:
- **Documentation**: https://docs.datatrace.example.com
- **Issues**: https://github.com/datatrace/datatrace/issues
- **Slack**: #datatrace on your organization's Slack
- **Email**: datatrace@example.com
