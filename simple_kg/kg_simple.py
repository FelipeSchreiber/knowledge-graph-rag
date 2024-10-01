from dotenv import load_dotenv
import os
from neo4j import GraphDatabase
load_dotenv()

AURA_INSTANCENAME = os.environ["AURA_INSTANCENAME"]
NEO4J_DATABASE=os.environ["NEO4J_DATABASE"]
NEO4J_URI = os.environ["NEO4J_URI"]
NEO4J_USERNAME=os.environ["NEO4J_USERNAME"]
NEO4J_PASSWORD=os.environ["NEO4J_PASSWORD"]
AURA_INSTANCEID=os.environ["AURA_INSTANCEID"]

AUTH = (NEO4J_USERNAME,NEO4J_PASSWORD)
driver = GraphDatabase.driver(NEO4J_URI,auth=AUTH)
try:
    driver.verify_connectivity()
    print("Connection established.")
    with driver.session(database=NEO4J_DATABASE) as session:
        result = session.run("MATCH (n) RETURN count (n)")
        count = result.single().value()
        print(f"Number of nodes is {count}")
except:
    print("Connection not established.")
# finally:
#     driver.close()
    
def create_entities(tx):
    tx.run("MERGE (a:Person {name:'Albert Einstein'})")
    tx.run("MERGE (p:Subject {name: 'Physics'})")
    tx.run("MERGE (n:NobelPrize {name: 'Nobel Prize in Physics'})")
    tx.run("MERGE (g:Country {name: 'Germany'})")
    tx.run("MERGE (u:Country {name: 'USA'})")
    

def create_relationships(tx):
    # Create studied relationship
    tx.run(
        """
    MATCH (a:Person {name: 'Albert Einstein'}), (p:Subject {name: 'Physics'})
    MERGE (a)-[:STUDIED]->(p)
    """
    )

    # Create won relationship
    tx.run(
        """
    MATCH (a:Person {name: 'Albert Einstein'}), (n:NobelPrize {name: 'Nobel Prize in Physics'})
    MERGE (a)-[:WON]->(n)
    """
    )

    # Create born in relationship
    tx.run(
        """
    MATCH (a:Person {name: 'Albert Einstein'}), (g:Country {name: 'Germany'})
    MERGE (a)-[:BORN_IN]->(g)
    """
    )

    # Create died in relationship
    tx.run(
        """
    MATCH (a:Person {name: 'Albert Einstein'}), (u:Country {name: 'USA'})
    MERGE (a)-[:DIED_IN]->(u)
    """
    )


# Function to connect and run a simple Cypher query
def query_graph_simple(cypher_query):
    driver = GraphDatabase.driver(NEO4J_URI, auth=AUTH)
    try:
        with driver.session(database=NEO4J_DATABASE) as session:
            result = session.run(cypher_query)
            for record in result:
                print(record["name"])
    except Exception as e:
        print(f"Error: {e}")
    # finally:
    #     driver.close()


# Function to connect and run a Cypher query
def query_graph(cypher_query):
    driver = GraphDatabase.driver(NEO4J_URI, auth=AUTH)
    try:
        with driver.session(database=NEO4J_DATABASE) as session:
            result = session.run(cypher_query)
            for record in result:
                print(record["path"])
    except Exception as e:
        print(f"Error: {e}")
    # finally:
    #     driver.close()


def build_knowledge_graph():
    # Open a session with the Neo4j database

    try:
        with driver.session(database=NEO4J_DATABASE) as session:
            # Create entities
            session.execute_write(create_entities)
            # Create relationships
            session.execute_write(create_relationships)

    except Exception as e:
        print(f"Error: {e}")
    # finally:
    #     driver.close()


# Cypher query to find paths related to Albert Einstein
einstein_query = """
MATCH path=(a:Person {name: 'Albert Einstein'})-[:STUDIED]->(s:Subject)
RETURN path
UNION
MATCH path=(a:Person {name: 'Albert Einstein'})-[:WON]->(n:NobelPrize)
RETURN path
UNION
MATCH path=(a:Person {name: 'Albert Einstein'})-[:BORN_IN]->(g:Country)
RETURN path
UNION
MATCH path=(a:Person {name: 'Albert Einstein'})-[:DIED_IN]->(u:Country)
RETURN path
"""


# Simple Cypher query to find all node names
simple_query = """
MATCH (n)
RETURN n.name AS name
"""

if __name__ == "__main__":
    # with driver.session() as session:
    #     session.run(f"DROP DATABASE {NEO4J_DATABASE} IF EXISTS")
    # Build the knowledge graph
    # build_knowledge_graph()

    query_graph_simple(simple_query)
    
    query_graph(einstein_query)
    driver.close()


# Run this to see the entire graph in the neo4j browser/console
# MATCH (n)-[r]->(m)
# RETURN n, r, m;
