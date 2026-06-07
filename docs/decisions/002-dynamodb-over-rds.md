# 002 — Use DynamoDB instead of RDS

**Status:** Accepted

## Context

The application stores notes with a simple structure: an ID, a title, and a body. There are no relational requirements — no joins, no foreign keys, no transactions across multiple entities.

## Decision

Use DynamoDB as the primary data store with `id` (UUID) as the partition key.

## Consequences

**Gained:**
- No fixed infrastructure cost — DynamoDB charges per request and storage used.
- Scales automatically with Lambda without connection pool management.
- Built-in PITR (Point-in-Time Recovery) and SSE with a single configuration flag.
- No patching, upgrades, or server management.

**Lost:**
- No support for complex queries without a secondary index.
- Scan operations are expensive at scale — the current `GET /` implementation must use pagination to avoid full table scans.
- Changing the data model (e.g., adding a sort key) requires migrating all existing items.
