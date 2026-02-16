import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(uri, auth=(user, password))


def ingest_kg():

    with driver.session() as session:

        # Course Node
        session.run("MERGE (c:Course {name:'B.Tech'})")

        # Department
        session.run("""
            MERGE (d:Department {name:'Computer Science'})
            MERGE (c:Course {name:'B.Tech'})
            MERGE (c)-[:HAS_DEPARTMENT]->(d)
        """)

        # Eligibility
        session.run("""
            MERGE (e:Eligibility {criteria:'Minimum 60% in 12th grade'})
            MERGE (c:Course {name:'B.Tech'})
            MERGE (c)-[:HAS_ELIGIBILITY]->(e)
        """)

        # Admission Process
        session.run("""
            MERGE (a:Admission {type:'Entrance Exam + Interview'})
            MERGE (c:Course {name:'B.Tech'})
            MERGE (c)-[:HAS_ADMISSION_PROCESS]->(a)
        """)

        # Fee
        session.run("""
            MERGE (f:Fee {amount:'1,20,000 per year'})
            MERGE (c:Course {name:'B.Tech'})
            MERGE (c)-[:HAS_FEE]->(f)
        """)

        # Infrastructure
        session.run("""
            MERGE (i:Infrastructure {facility:'Modern Labs, Library, Hostel'})
            MERGE (c:Course {name:'B.Tech'})
            MERGE (c)-[:HAS_INFRASTRUCTURE]->(i)
        """)

        # Duration
        session.run("""
            MERGE (du:Duration {years:'4 Years'})
            MERGE (c:Course {name:'B.Tech'})
            MERGE (c)-[:HAS_DURATION]->(du)
        """)

    print("✅ Knowledge Graph Created Successfully!")


if __name__ == "__main__":
    ingest_kg()
