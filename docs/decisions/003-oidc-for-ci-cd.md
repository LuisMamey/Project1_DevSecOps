# 003 — Use OIDC instead of static access keys for CI/CD

**Status:** Accepted

## Context

GitHub Actions needs AWS credentials to run `terraform plan` and `terraform apply`. The traditional approach is creating an IAM user, generating long-lived access keys, and storing them as GitHub secrets. Long-lived keys are a persistent security risk: they can be leaked, they never expire automatically, and rotation is a manual process.

## Decision

Use OpenID Connect (OIDC) federation between GitHub Actions and AWS. GitHub acts as the identity provider. The pipeline exchanges a short-lived GitHub token for temporary AWS credentials via `sts:AssumeRoleWithWebIdentity`.

## Consequences

**Gained:**
- No static credentials stored anywhere — no keys to leak, rotate, or audit.
- Credentials are scoped to a single pipeline run and expire automatically.
- The IAM trust policy restricts which repository and branch can assume the role, preventing lateral movement from other GitHub repositories.

**Lost:**
- One-time bootstrap required: the OIDC provider and IAM role must be created locally before the pipeline can run for the first time.
- Slightly more complex setup compared to creating an IAM user.
