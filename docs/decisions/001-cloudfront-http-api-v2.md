# 001 — Use CloudFront + HTTP API v2 instead of REST API

**Status:** Accepted

## Context

API Gateway offers two flavors: REST API (v1) and HTTP API (v2). WAF v2 with CLOUDFRONT scope cannot be attached directly to HTTP API v2 — only to CloudFront distributions, Application Load Balancers, and REST APIs. The project requires WAF for rate limiting and managed rule protection.

## Decision

Use HTTP API v2 behind a CloudFront distribution. CloudFront acts as the WAF target and forwards requests to the API Gateway origin.

## Consequences

**Gained:**
- HTTP API v2 is ~70% cheaper than REST API for the same request volume.
- WAF managed rules and rate limiting apply at the CloudFront edge before traffic reaches the API.
- CloudFront adds DDoS protection and global edge delivery at no extra configuration cost.

**Lost:**
- One additional layer of infrastructure to maintain and debug.
- CloudFront TTL must be set to 0 for all dynamic routes to prevent caching API responses.
- End-to-end latency increases slightly due to the extra hop.
