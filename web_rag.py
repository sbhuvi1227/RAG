import os
from dotenv import load_dotenv

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.chat_models import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

def load_llm():
    return ChatOpenAI(
        openai_api_key=os.getenv("GROQ_API_KEY"),
        openai_api_base="https://api.groq.com/openai/v1",
        model="llama-3.1-8b-instant",
        temperature=0,
        max_tokens=1024
    )

def web_search_rag(query: str):

    search = DuckDuckGoSearchRun()

    web_results = search.run(query)

    if not web_results:
        return "No relevant information found online."

    prompt = ChatPromptTemplate.from_template(
        """
        You are an intelligent assistant.

        Use the web search results below to answer the question clearly and accurately.

        Web Results:
        {context}

        Question:
        {question}
        """
    )

    chain = prompt | load_llm() | StrOutputParser()

    return chain.invoke({
        "context": web_results,
        "question": query
    })
