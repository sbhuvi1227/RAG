import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

PERSIST_DIR = "vectorstore"

def ingest():

    with open("data/college_academic_extended_file.txt", "r", encoding="utf-8") as f:
        texts = f.readlines()

    Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        persist_directory=PERSIST_DIR
    )

    print("Vector DB Created Successfully.")

if __name__ == "__main__":
    ingest()
