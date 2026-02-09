import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Documentation Generator Agent",
    page_icon="📄",
    layout="wide"
)

# -------------------------------------------------
# Header
# -------------------------------------------------
st.title("📄 Documentation Generator Agent")
st.caption(
    "Generate README, API docs, and tutorials directly from a GitHub repository using AI."
)

st.markdown("---")

# -------------------------------------------------
# Input Form
# -------------------------------------------------
with st.form("doc_form"):
    github_url = st.text_input(
        "GitHub Repository URL",
        placeholder="https://github.com/username/repository"
    )

    version = st.text_input(
        "Version Name",
        placeholder="v1.0"
    )

    submitted = st.form_submit_button("🚀 Generate Documentation")

# -------------------------------------------------
# Submit Action
# -------------------------------------------------
if submitted:
    if not github_url or not version:
        st.error("Please provide both GitHub URL and version name.")
    else:
        with st.spinner("Generating documentation, please wait…"):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json={
                        "github_url": github_url,
                        "version": version
                    },
                    timeout=300
                )
            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")
                st.stop()

        # -------------------------------------------------
        # Handle Backend Response
        # -------------------------------------------------
        if response.status_code != 200:
            st.error("Backend returned an error")
            st.code(response.text)
            st.stop()

        data = response.json()

        if "docs" not in data:
            st.error("Backend did not return documentation content.")
            st.code(data)
            st.stop()

        docs = data["docs"]

        st.success("✅ Documentation generated successfully!")

        # -------------------------------------------------
        # README
        # -------------------------------------------------
        if docs.get("readme"):
            with st.expander("📄 README.md", expanded=True):
                st.markdown(docs["readme"])
                st.download_button(
                    "⬇️ Download README.md",
                    docs["readme"],
                    file_name="README.md"
                )

        # -------------------------------------------------
        # API Docs
        # -------------------------------------------------
        if docs.get("api"):
            with st.expander("📘 API Documentation"):
                st.markdown(docs["api"])
                st.download_button(
                    "⬇️ Download api.md",
                    docs["api"],
                    file_name="api.md"
                )

        # -------------------------------------------------
        # Tutorial
        # -------------------------------------------------
        if docs.get("tutorial"):
            with st.expander("📗 Tutorial"):
                st.markdown(docs["tutorial"])
                st.download_button(
                    "⬇️ Download tutorial.md",
                    docs["tutorial"],
                    file_name="tutorial.md"
                )
