import os
from dotenv import load_dotenv
import openai
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential


from database import execute_query

load_dotenv()


AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")
API_VERSION = os.getenv("API_VERSION")

AZURE_SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
AZURE_SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
INDEX_NAME = os.getenv("INDEX_NAME", "aaitech-index") 

# Azure Search setup
search_client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=INDEX_NAME,
    credential=AzureKeyCredential(AZURE_SEARCH_KEY)
)

def search_index(query_text, top=1):
    results = search_client.search(query_text, top=top)
    docs = []
    for result in results:
        docs.append(result)
    return docs

def build_schema_context(doc):
    return (
        f"Table: {doc.get('name', '')}\n"
        f"Description: {doc.get('description', '')}\n"
        f"Columns: {doc.get('columns', '')}\n"
    )

# Azure OpenAI setup
openai.api_type = "azure"
openai.api_key = AZURE_OPENAI_API_KEY
openai.api_base = AZURE_OPENAI_ENDPOINT
openai.api_version = API_VERSION

def clean_sql(sql: str):
    lines = sql.strip().splitlines()
    cleaned_lines = [line for line in lines if not line.strip().startswith("```")]
    return "\n".join(cleaned_lines).strip()
    


def question_to_sql(question: str):
    # Retrieve top search results for RAG context
    search_results = search_index(question, top=1)
    context = ""
    if search_results:
        doc = search_results[0]
        context = build_schema_context(doc)

    system_prompt = (
        "You are an assistant that converts natural language business questions into SQL queries"
        "Available table names for your information:" \
        "customers, suppliers, products, orders, order_details"
        
        "Use the following database schema context to help you:\n"
        f"{context}\n"
        "Return only the SQL query. Do not explain anything."
    )


    message = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]

    response = openai.chat.completions.create(
        model = DEPLOYMENT_NAME,
        messages = message,
        temperature=0,
        max_tokens=150
    )
    sql = response.choices[0].message.content.strip()
    cln_sql = clean_sql(sql)
    return cln_sql


if __name__ == "__main__":
    question = "What is the total shipping cost of orders for each country?" 
    sql_query = question_to_sql(question)
    print("Generated SQL:\n", sql_query)

    # Execute the generated SQL query using the database connection
    try:
        results = execute_query(sql_query)
        print("Query Results:")
        print(results)
    except Exception as e:
        print("Error executing query:", e)

    
