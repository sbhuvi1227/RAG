import os
from dotenv import load_dotenv

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from web_rag import web_search_rag

load_dotenv()

# ----------------------------
# Embeddings Setup
# ----------------------------
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

PERSIST_DIR = "vectorstore"


# ----------------------------
# Load Vectorstore
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
# Load LLM
# ----------------------------
def load_llm():

    return ChatOpenAI(
        openai_api_key=os.getenv("GROQ_API_KEY"),
        openai_api_base="https://api.groq.com/openai/v1",
        model="llama-3.1-8b-instant",
        temperature=0,
        max_tokens=1024
    )


# ----------------------------
# Local RAG with Similarity Threshold
# ----------------------------
def local_rag(query: str):

    vectorstore = load_vectorstore()

    # Get docs with similarity scores
    results = vectorstore.similarity_search_with_score(query, k=3)

    if not results:
        return None

    # Chroma: lower score = better match
    best_score = results[0][1]

    print("Best similarity score:", best_score)

    # 🔥 IMPORTANT THRESHOLD
    # If score is too high → not relevant → trigger web search
    if best_score > 0.6:
        print("Low relevance. Triggering web search.")
        return None

    docs = [doc for doc, score in results]

    context = "\n".join([doc.page_content for doc in docs])

    prompt = ChatPromptTemplate.from_template(
        """
        Answer the question strictly using the context below.
        If the answer is not in the context, say:
        "Information not available in local database."

        Context:
        {context}

        Question:
        {question}
        """
    )

    chain = prompt | load_llm() | StrOutputParser()

    response = chain.invoke({
        "context": context,
        "question": query
    })

    # 🔥 EXTRA SAFETY CHECK
    if "Information not available" in response:
        return None

    return response


# ----------------------------
# Hybrid RAG Controller
# ----------------------------
def get_answer(query: str):

    # 1️⃣ Try local RAG
    local_answer = local_rag(query)

    if local_answer is not None:
        return local_answer

    # 2️⃣ Fallback to Web RAG
    return web_search_rag(query)
