import streamlit as st
from rag_pipeline import get_answer

st.set_page_config(
    page_title="College FAQ RAG + Web Search",
    layout="centered"
)

st.title("📚 Enhanced College FAQ Chatbot")

query = st.text_input("Enter your question:")

if st.button("Search"):
    if query.strip():
        with st.spinner("Getting answer…"):
            answer = get_answer(query)
        st.success(answer)
    else:
        st.warning("Please enter a question.")
