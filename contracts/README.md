# DataTrace Contracts

This directory contains interface contracts for the DataTrace system. These contracts define how external systems and users interact with DataTrace.

## Contract Types

| Contract | Type | Purpose | Audience |
|----------|------|---------|----------|
| [api-contract.md](api-contract.md) | REST API | Programmatic access to DataTrace functionality | Developers, Applications |
| [cli-contract.md](cli-contract.md) | Command-Line Interface | Terminal-based operations | Data Engineers, DevOps |
| [dbt-contract.md](dbt-contract.md) | Integration | dbt project integration | dbt Developers |
| [bigquery-contract.md](bigquery-contract.md) | Integration | BigQuery metadata extraction | Data Engineers |
| [powerbi-contract.md](powerbi-contract.md) | Integration | Power BI metadata extraction | BI Developers |

## Contract Structure

Each contract follows a consistent structure:

1. **Overview**: Description of the interface and its purpose
2. **Endpoints/Commands**: List of available operations
3. **Authentication**: How to authenticate and authorize
4. **Request/Response Formats**: Schema definitions
5. **Error Handling**: Error codes and messages
6. **Examples**: Practical usage examples
7. **Rate Limiting**: Performance and usage constraints

## Versioning

Contracts are versioned using semantic versioning:
- **MAJOR**: Breaking changes to existing contracts
- **MINOR**: Backward-compatible additions to contracts
- **PATCH**: Backward-compatible bug fixes and clarifications

The current contract version is **v1.0.0**.

## Compatibility

DataTrace is committed to maintaining backward compatibility within MAJOR versions. When breaking changes are necessary, they will be communicated through:

1. Release notes
2. Migration guides
3. Deprecation warnings in responses

## Testing

Each contract includes test cases that can be used to verify compatibility. See the `quickstart.md` for validation scenarios.

## Feedback

Contract changes are governed by the DataTrace constitution. To request changes:
1. Open a GitHub Issue with the "contract-change" label
2. Include rationale, impact assessment, and migration plan
3. Follow the amendment procedure in the constitution
