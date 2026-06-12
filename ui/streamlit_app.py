import os
import streamlit as st
import requests

API_URL = os.getenv("API_URL", "http://localhost:8000")
try:
    API_URL = st.secrets.get("api_url", API_URL)
except Exception:
    pass

st.set_page_config(page_title="Agentic Incident Triage", page_icon="🚨")
st.title("Agentic Incident Triage Platform")
st.write("Submit an IT incident ticket and get classification, risk scoring, similar incidents, and a recommended resolution.")

with st.form("incident_form"):
    ticket_id = st.text_input("Ticket ID", "INC-2031")
    title = st.text_input("Title", "Airflow DAG failed after schema change")
    description = st.text_area("Description", "Daily ETL pipeline failed after source schema update.")
    priority = st.selectbox("Priority", ["P1", "P2", "P3", "P4"], index=0)
    submitted = st.form_submit_button("Submit")

if submitted:
    payload = {
        "ticket_id": ticket_id,
        "title": title,
        "description": description,
        "priority": priority,
    }
    try:
        response = requests.post(f"{API_URL}/triage", json=payload, timeout=20)
        response.raise_for_status()
        data = response.json()

        st.subheader("Triage Result")
        st.markdown(f"**Category:** {data.get('category')}")
        st.markdown(f"**Urgency:** {data.get('urgency')}")
        st.markdown(f"**Risk Score:** {data.get('risk_score')}")
        st.markdown(f"**Escalation Required:** {data.get('escalation_required')}")
        st.markdown(f"**Assigned Team:** {data.get('assigned_team')}")
        st.markdown(f"**Next Action:** {data.get('next_action')}")
        st.markdown("**Recommended Resolution:**")
        st.write(data.get('recommended_resolution'))

        if data.get('similar_incidents'):
            st.subheader("Similar Incidents")
            for item in data['similar_incidents']:
                st.write(f"- {item['ticket_id']} ({item['similarity_score']}) — {item['title']}")
    except Exception as exc:
        st.error(f"Unable to reach triage API: {exc}")
