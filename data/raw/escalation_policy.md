# Escalation Policy

## Priority definitions
- P1: Critical incident impacting production services or security.
- P2: High-impact incident affecting customer experience or core workflows.
- P3: Medium-impact incident requiring investigation but not immediate action.
- P4: Low-impact incident or informational event.

## Escalation rules
- Automatically route P1 incidents to human review.
- Route incidents with risk score >= 0.75 to human review.
- Auto-resolve P2/P3 incidents when there is a strong historical match and low risk.
- Assign incidents to domain teams based on category and incident context.

## Human review triggers
- Any security alert or suspicious activity.
- P1 incidents affecting critical systems such as databases, authentication, or deployments.
- Escalation probability above 75%.
- Similar incidents with unresolved or high impact outcomes.
