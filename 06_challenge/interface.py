import streamlit as st
import requests
import uuid

# — your local API endpoint and agent identifiers —
API_URL = "http://localhost:8000"
APP_NAME = "brand_monitor_agent"       # replace with your agent folder name
USER_ID = "streamlit_user"         # arbitrary user ID

st.title("ADK Agent Interface")

# 1) get user input
user_input = st.text_input("Enter your query:")

if st.button("Send"):
    # 2) new session per run
    session_id = uuid.uuid4().hex

    # 3) create session (empty state)
    session_url = f"{API_URL}/apps/{APP_NAME}/users/{USER_ID}/sessions/{session_id}"
    requests.post(session_url, json={"state": {}})

    # 4) send message to /run
    payload = {
        "app_name": APP_NAME,
        "user_id": USER_ID,
        "session_id": session_id,
        "new_message": {
            "role": "user",
            "parts": [{"text": user_input}]
        }
    }
    resp = requests.post(f"{API_URL}/run", json=payload)

    # 5) show response as Markdown
    if resp.ok:
        events = resp.json()
        md = ""
        for ev in events:
            content = ev.get("content", {})
            if content.get("role") == "model":
                for part in content.get("parts", []):
                    md += part.get("text", "")
        st.markdown(md)
    else:
        st.error(f"Error {resp.status_code}: {resp.text}")
