"""
Streamlit entrypoint.

For now this wires up: DB init, sign up, log in, log out, and a placeholder
home screen. Ingestion, chunking, retrieval, and QA screens get added as
those modules are built.
"""

import streamlit as st

from database.db import init_db
from auth.auth import sign_up, log_in, AuthError

st.set_page_config(page_title="Multi-Doc RAG Chatbot", page_icon="💬", layout="wide")

init_db()

if "user" not in st.session_state:
    st.session_state.user = None


def render_login_signup() -> None:
    st.title("💬 Multi-Document RAG Chatbot")
    login_tab, signup_tab = st.tabs(["Log in", "Sign up"])

    with login_tab:
        with st.form("login_form"):
            identifier = st.text_input("Username or email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Log in")
        if submitted:
            try:
                st.session_state.user = log_in(identifier, password)
                st.rerun()
            except AuthError as e:
                st.error(str(e))

    with signup_tab:
        with st.form("signup_form"):
            username = st.text_input("Username")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password", key="signup_pw")
            confirm = st.text_input("Confirm password", type="password")
            submitted = st.form_submit_button("Create account")
        if submitted:
            if password != confirm:
                st.error("Passwords do not match.")
            else:
                try:
                    st.session_state.user = sign_up(username, email, password)
                    st.rerun()
                except AuthError as e:
                    st.error(str(e))


def render_home() -> None:
    user = st.session_state.user
    with st.sidebar:
        st.write(f"Signed in as **{user.username}**")
        if st.button("Log out"):
            st.session_state.user = None
            st.rerun()

    st.title("💬 Multi-Document RAG Chatbot")
    st.info(
        "Auth and database layers are live. Document upload, chunking, "
        "retrieval, and chat come next."
    )


def main() -> None:
    if st.session_state.user is None:
        render_login_signup()
    else:
        render_home()


if __name__ == "__main__":
    main()
