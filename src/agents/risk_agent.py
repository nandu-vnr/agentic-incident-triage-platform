from src.models.predict import predict_risk


def predict_escalation_risk(ticket, category):
    return predict_risk(ticket.priority, category, ticket.description)
