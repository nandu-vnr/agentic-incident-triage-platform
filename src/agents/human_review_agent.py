

def needs_human_review(priority: str, risk_score: float) -> bool:
    return priority == "P1" or risk_score >= 0.75
