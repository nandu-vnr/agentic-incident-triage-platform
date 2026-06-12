.PHONY: install train embed run-api run-ui test lint

install:
	pip install -r requirements.txt

train:
	python src/models/train_classifier.py
	python src/models/train_risk_model.py
	python src/retrieval/embed_tickets.py

embed:
	python src/retrieval/embed_tickets.py

run-api:
	uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000

run-ui:
	streamlit run ui/streamlit_app.py

test:
	pytest tests

lint:
	python -m py_compile src/api/main.py src/agents/*.py src/models/*.py src/retrieval/*.py src/schemas/*.py src/evaluation/*.py
