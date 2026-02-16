🎓 College Academic Advisor (KG-RAG)

An intelligent academic advisory system powered by Hybrid Retrieval-Augmented Generation (RAG) combining:

📚 Vector Database Retrieval

🧠 Knowledge Graph (Neo4j)

🔎 Corrective Context Merging

This system provides accurate, structured, and context-aware responses to academic queries such as admissions, eligibility, fees, infrastructure, and course details.

🚀 Project Overview

The College Academic Advisor uses a Hybrid RAG architecture:

Vector Retrieval

Retrieves semantically similar documents using embeddings.

Handles unstructured academic information.

Knowledge Graph Retrieval

Uses Neo4j to store structured academic relationships.

Retrieves precise entity-based data (e.g., course → fee → duration).

Corrective RAG Layer

Merges vector and KG context.

Improves factual consistency and response quality.

🏗️ Architecture

User Query
→ Vector DB Retrieval
→ Knowledge Graph Retrieval
→ Context Merging
→ LLM Response Generation