from src.models.predict import predict_category


def classify_ticket(ticket):
    return predict_category(ticket.title, ticket.description)
