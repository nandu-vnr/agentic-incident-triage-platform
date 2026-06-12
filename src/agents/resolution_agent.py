import os
from typing import Dict

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


def _build_resolution(ticket, category: str, risk_score: float, similar_incidents: list):
    steps = [
        f"Review the incident details for ticket {ticket.ticket_id}.",
        f"Predicted category: {category}.",
        f"Priority: {ticket.priority}.",
        f"Risk score: {risk_score}.",
    ]
    if similar_incidents:
        steps.append("Check similar past incidents for matching root cause and resolution patterns.")
    steps.append("Generate a targeted remediation plan based on the category and runbooks.")

    recommendation = (
        f"Validate the root cause for {category.lower()} incident, execute targeted remediation steps, "
        f"and coordinate with the assigned team. "
        f"Use the historical similar incidents as a reference for resolution."
    )
    assigned_team = {
        "Access Management": "IAM",
        "Data Engineering": "Data Platform",
        "Cloud Infrastructure": "Cloud Platform",
        "Application Support": "App Support",
        "Security Alert": "Security Operations",
        "Database": "DBA",
        "Network": "Network Operations",
        "Deployment Failure": "Platform Engineering",
    }.get(category, "Operations")

    next_action = (
        "Escalate to on-call "
        f"{assigned_team} engineer because this incident is high risk." if risk_score >= 0.75 or ticket.priority == "P1"
        else f"Review the recommended resolution with {assigned_team} and close after validation."
    )

    return {
        "recommended_resolution": recommendation,
        "assigned_team": assigned_team,
        "next_action": next_action,
        "confidence": "high" if risk_score >= 0.75 or ticket.priority == "P1" else "medium",
    }


def recommend_resolution(ticket, category: str, risk_score: float, similar_incidents: list) -> Dict[str, str]:
    resolution = _build_resolution(ticket, category, risk_score, similar_incidents)

    if OPENAI_API_KEY:
        try:
            import openai

            openai.api_key = OPENAI_API_KEY
            prompt = (
                f"Ticket summary: {ticket.title} - {ticket.description}\n"
                f"Category: {category}\n"
                f"Priority: {ticket.priority}\n"
                f"Risk score: {risk_score}\n"
                f"Similar incidents: {[item['ticket_id'] for item in similar_incidents]}\n"
                f"Provide a concise recommended resolution, assigned team, next action, and escalation guidance."
            )
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=220,
                temperature=0.3,
            )
            content = response.choices[0].message.content.strip()
            resolution["recommended_resolution"] = content
            resolution["confidence"] = "high"
        except Exception:
            pass

    return resolution
