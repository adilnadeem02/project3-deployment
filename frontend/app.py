import streamlit as st
import requests

# URL of the FastAPI backend
API_URL = "http://backend-service:8000/todos"

st.set_page_config(page_title="Task Manager", layout="centered")
st.title("TO-DO LIST")
st.markdown("---")

# Add new task
with st.form(key="add_task_form", clear_on_submit=True):
    new_task = st.text_input("New Task", placeholder="Enter a task...")
    submit_button = st.form_submit_button(label="Add")
    
    if submit_button and new_task:
        requests.post(API_URL, json={"task": new_task})
        st.rerun()

# Display tasks
st.subheader("Current Tasks")
try:
    response = requests.get(API_URL)
    if response.status_code == 200:
        todos = response.json()
        if not todos:
            st.write("No tasks yet.")
        else:
            for todo in todos:
                col1, col2, col3 = st.columns([0.1, 0.7, 0.2])
                
                # Checkbox for completion
                is_completed = col1.checkbox("", value=todo["completed"], key=f"check_{todo['id']}")
                if is_completed != todo["completed"]:
                    requests.put(f"{API_URL}/{todo['id']}")
                    st.rerun()
                
                # Task text
                text_style = "strikethrough" if todo["completed"] else "normal"
                if todo["completed"]:
                    col2.markdown(f"~{todo['task']}~")
                else:
                    col2.markdown(f"{todo['task']}")
                
                # Delete button
                if col3.button("Drop", key=f"del_{todo['id']}"):
                    requests.delete(f"{API_URL}/{todo['id']}")
                    st.rerun()
    else:
        st.error("Backend is not responding.")
except requests.exceptions.ConnectionError:
    st.error("Cannot connect to the backend. Is FastAPI running?")