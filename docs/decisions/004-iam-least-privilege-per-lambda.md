# 004 — IAM least privilege per Lambda

**Status:** Accepted

## Context

A common shortcut is attaching a single broad IAM policy (e.g., `AmazonDynamoDBFullAccess`) to all Lambda functions. This violates the principle of least privilege: a compromised function gains access to all DynamoDB operations across all tables.

## Decision

Each Lambda function has its own IAM execution role with a custom policy that grants only the DynamoDB actions that function needs, scoped to the specific table ARN.

| Function | Permissions |
|---|---|
| GetAll | `dynamodb:Scan` |
| GetOne | `dynamodb:GetItem` |
| Create | `dynamodb:PutItem` |
| Update | `dynamodb:UpdateItem` |
| Delete | `dynamodb:DeleteItem` |

## Consequences

**Gained:**
- Blast radius of a compromised function is limited to its own permissions.
- IAM policies serve as documentation of what each function does.
- Satisfies AWS Well-Architected Framework security pillar requirements.

**Lost:**
- More IAM resources to manage — 5 roles and 5 policies instead of 1 of each.
- Adding a new Lambda requires defining its permissions explicitly.
