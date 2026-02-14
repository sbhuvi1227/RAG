import streamlit as st
from rag_pipeline import get_answer

st.set_page_config(page_title="College FAQ RAG", layout="centered")

st.title("📚 College FAQ Chatbot")
st.markdown("Ask questions about admission, fees, deadlines, placements, etc.")

query = st.text_input("Enter your question:")

if st.button("Search"):
    if query.strip():
        with st.spinner("Generating answer..."):
            answer = get_answer(query)
        st.success(answer)
    else:
        st.warning("Please enter a valid question.")
