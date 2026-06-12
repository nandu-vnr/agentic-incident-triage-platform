from src.retrieval.similar_ticket_search import find_similar_incidents


def retrieve_similar_incidents(ticket):
    return find_similar_incidents(ticket.title, ticket.description, top_k=3)
