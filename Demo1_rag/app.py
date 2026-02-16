import streamlit as st
from rag_pipeline import get_answer

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(
    page_title="KG RAG Academic Advisor",
    page_icon="🎓",
    layout="centered"
)

# ----------------------------
# Session State
# ----------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# ----------------------------
# Header
# ----------------------------
st.markdown("""
# 🎓 College Academic Advisor (KG RAG)
""")

st.markdown("---")

# ----------------------------
# User Input
# ----------------------------
query = st.text_input(
    "Ask your academic question:",
    placeholder="e.g., What is the syllabus for B.Tech Computer Science?"
)

# ----------------------------
# Search Button
# ----------------------------
if st.button("🔍 Get Answer"):

    if query.strip() == "":
        st.warning("Please enter a valid question.")
    else:
        with st.spinner("Retrieving from Vector DB + Knowledge Graph..."):
            try:
                answer = get_answer(query)

                # Store in history
                st.session_state.history.append({
                    "question": query,
                    "answer": answer
                })

                st.success("Answer Generated Successfully ✅")
                st.markdown("### 📘 Answer:")
                st.write(answer)

            except Exception as e:
                st.error(f"Error occurred: {str(e)}")

# ----------------------------
# Conversation History
# ----------------------------
if st.session_state.history:
    st.markdown("---")
    st.markdown("## 📝 Conversation History")

    for idx, item in enumerate(reversed(st.session_state.history)):
        with st.expander(f"Q{len(st.session_state.history) - idx}: {item['question']}"):
            st.write(item["answer"])

# ----------------------------
# Footer
# ----------------------------
st.markdown("---")
st.markdown(
    "Built with ❤️ using LangChain + Neo4j + Groq LLM + Streamlit"
)
