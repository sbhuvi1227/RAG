import os
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# ----------------------------
# Embeddings Setup
# ----------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

PERSIST_DIR = "vectorstore"


# ----------------------------
# Load or Create Vector Store
# ----------------------------
def load_vectorstore():

    if not os.path.exists(PERSIST_DIR):

        with open("data/college_info.txt", "r", encoding="utf-8") as file:
            texts = file.readlines()

        vectorstore = Chroma.from_texts(
            texts=texts,
            embedding=embeddings,
            persist_directory=PERSIST_DIR
        )
    else:
        vectorstore = Chroma(
            persist_directory=PERSIST_DIR,
            embedding_function=embeddings
        )

    return vectorstore


# ----------------------------
# Load Groq LLM (OpenAI-compatible)
# ----------------------------
def load_llm():

    return ChatOpenAI(
        openai_api_key=os.getenv("GROQ_API_KEY"),
        openai_api_base="https://api.groq.com/openai/v1",
        model="llama-3.1-8b-instant",  # Active Groq model
        temperature=0,
        max_tokens=1024
    )


# ----------------------------
# RAG Function (Modern LCEL)
# ----------------------------
def get_answer(query: str):

    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever()

    llm = load_llm()

    # Retrieve documents
    docs = retriever.invoke(query)
    context = "\n".join([doc.page_content for doc in docs])

    # Prompt
    prompt = ChatPromptTemplate.from_template(
        """
        Answer the question based only on the context below.

        Context:
        {context}

        Question:
        {question}
        """
    )

    chain = (
        prompt
        | llm
        | StrOutputParser()
    )

    return chain.invoke({
        "context": context,
        "question": query
    })
