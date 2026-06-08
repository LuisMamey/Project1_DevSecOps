# 005 — Checkov skip policy

**Status:** Accepted

## Context

Checkov is a static analysis tool that scans Terraform files against hundreds of security rules. Not all rules apply to every project — some require external resources not available in this project, some are appropriate only for production environments with compliance requirements, and some are intentional design decisions.

## Decision

Skip the following checks with documented justification:

| Check | Category | Justification |
|---|---|---|
| `CKV_AWS_374` | Not applicable | Geo restriction disabled intentionally — the API is public |
| `CKV_AWS_305` | Not applicable | Default root object applies to web apps, not APIs |
| `CKV_AWS_174` | Not applicable | Cannot configure minimum TLS version with the default CloudFront certificate |
| `CKV2_AWS_42` | Not applicable | No custom domain — using the default CloudFront certificate |
| `CKV2_AWS_47` | Not applicable | `AWSManagedRulesKnownBadInputsRuleSet` already covers Log4j |
| `CKV_AWS_117` | Omitted in dev | Lambda in VPC requires NAT Gateway (~$32/month); no private resources to protect |
| `CKV_AWS_158` | Omitted in dev | CloudWatch KMS CMK adds cost; AWS managed key sufficient for dev |
| `CKV_AWS_119` | Omitted in dev | DynamoDB KMS CMK adds cost; AWS managed key sufficient for dev |
| `CKV_AWS_173` | Omitted in dev | Lambda env vars contain no sensitive data (`TABLE_NAME` only) |
| `CKV2_AWS_32` | Omitted in dev | Response headers policy is a future improvement |
| `CKV_AWS_338` | Omitted in dev | 1-year retention required for compliance; 30 days sufficient for dev |
| `CKV2_AWS_31` | Omitted in dev | WAF logging requires additional S3 bucket; deferred to a future sprint |

## Consequences

**Gained:**
- Pipeline fails on genuine misconfigurations while ignoring rules that do not apply.
- Every skip has a documented reason — reviewers can audit the decision without context from the author.

**Lost:**
- Some skipped checks would be mandatory in a production environment with compliance requirements (HIPAA, SOC2). Promoting this project to production would require revisiting this list.
