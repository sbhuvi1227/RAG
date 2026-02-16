import os
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from kg_retriever import query_kg

load_dotenv()

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Chroma(
    persist_directory="vectorstore",
    embedding_function=embeddings
)

def load_llm():
    return ChatOpenAI(
        openai_api_key=os.getenv("GROQ_API_KEY"),
        openai_api_base="https://api.groq.com/openai/v1",
        model="llama-3.1-8b-instant",
        temperature=0
    )

def get_answer(query):

    # 1️⃣ Vector Retrieval
    docs = vectorstore.similarity_search(query, k=3)
    vector_context = "\n".join([d.page_content for d in docs])

    # 2️⃣ KG Retrieval
    kg_context = query_kg(query)

    # 3️⃣ Merge Context
    combined_context = f"""
    Vector Context:
    {vector_context}

    Knowledge Graph Context:
    {kg_context}
    """

    # 4️⃣ Corrective RAG Prompt
    prompt = ChatPromptTemplate.from_template("""
    You are an academic advisor chatbot.

    Use both vector and knowledge graph context.
    If answer seems incomplete, improve it logically.

    Context:
    {context}

    Question:
    {question}
    """)

    chain = prompt | load_llm() | StrOutputParser()

    return chain.invoke({
        "context": combined_context,
        "question": query
    })
