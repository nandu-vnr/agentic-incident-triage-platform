# IT Incident Triage Knowledge Base

## Incident categories
- Access Management
- Data Engineering
- Cloud Infrastructure
- Application Support
- Security Alert
- Database
- Network
- Deployment Failure

## Common root causes
- Authentication and authorization failures
- Data pipeline schema drift
- Infrastructure resource exhaustion
- Service deployment and configuration errors
- Network connectivity and DNS issues
- Security events and suspicious account activity

## Recommended resolution patterns
- Validate user identity and access policies
- Verify infrastructure health and resource limits
- Analyze pipeline logs, schema changes, and upstream dependencies
- Rerun failed jobs, backfill missing data, and test recovery steps
- Escalate high-risk incidents to on-call platform, security, or DBA teams

## Example runbook snippets
- Update dbt model and rerun Great Expectations validation
- Increase connection pool limits and restart the database client
- Rotate credentials, block suspicious IPs, and audit logs
- Fix deployment manifest, rebuild service image, and redeploy with readiness checks
