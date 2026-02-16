import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(uri, auth=(user, password))


def extract_keyword(user_query: str) -> str:
    """
    Extract important keyword from user query
    to improve KG matching accuracy
    """

    query = user_query.lower()

    if "infrastructure" in query:
        return "infrastructure"
    elif "admission" in query:
        return "admission"
    elif "eligibility" in query:
        return "eligibility"
    elif "fee" in query or "fees" in query:
        return "fee"
    elif "department" in query:
        return "department"
    elif "duration" in query:
        return "duration"
    else:
        return query   # fallback to full query


def query_kg(user_query: str) -> str:
    """
    Retrieve structured triples from Neo4j Knowledge Graph
    """

    search_term = extract_keyword(user_query)

    with driver.session() as session:

        result = session.run(
            """
            MATCH (a)-[r]->(b)
            WHERE 
                toLower(a.name) CONTAINS toLower($term)
                OR toLower(b.name) CONTAINS toLower($term)
                OR toLower(type(r)) CONTAINS toLower($term)
                OR toLower(a.criteria) CONTAINS toLower($term)
                OR toLower(a.amount) CONTAINS toLower($term)
                OR toLower(a.facility) CONTAINS toLower($term)
                OR toLower(a.years) CONTAINS toLower($term)
            RETURN 
                coalesce(a.name, a.criteria, a.amount, a.facility, a.years) AS source,
                type(r) AS relation,
                coalesce(b.name, b.criteria, b.amount, b.facility, b.years) AS target
            LIMIT 20
            """,
            {"term": search_term}
        )

        records = result.data()

    if not records:
        return "No relevant knowledge graph data found."

    # Format triples into readable text
    kg_context = ""
    for record in records:
        kg_context += f"{record['source']} {record['relation']} {record['target']}\n"

    return kg_context


if __name__ == "__main__":
    # Test
    question = input("Ask your academic question: ")
    response = query_kg(question)
    print("\n--- Knowledge Graph Results ---")
    print(response)

