import os
import pandas as pd
from dotenv import load_dotenv

from azure.search.documents.indexes import SearchIndexClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes.models import SearchIndex, SimpleField, SearchableField
from azure.search.documents import SearchClient

# Load environment variables
load_dotenv()
endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
key = os.getenv("AZURE_SEARCH_KEY")
index_name = "aaitech-index"

# Create SearchIndexClient
client = SearchIndexClient(endpoint=endpoint, credential=AzureKeyCredential(key))

# Delete index if it already exists
if index_name in [idx.name for idx in client.list_indexes()]:
    client.delete_index(index_name)

# Define fields
fields = [
    SimpleField(name="id", type="Edm.String", key=True, searchable=False),
    SearchableField(name="type", type="Edm.String", sortable=True, analyzer_name="standard.lucene"),
    SearchableField(name="name", type="Edm.String", sortable=True, analyzer_name="standard.lucene"),
    SearchableField(name="description", type="Edm.String", sortable=True, analyzer_name="standard.lucene"),
    SearchableField(name="columns", type="Edm.String", sortable=True, analyzer_name="standard.lucene"),
]

# Create index
index = SearchIndex(name=index_name, fields=fields)
client.create_index(index)
print(f"Created index: {index_name}")

# Load CSV
df = pd.read_csv("data/aaitech_vector_schema_info.csv")
df = df.fillna("")


# Initialize Search client
search_client = SearchClient(
    endpoint=endpoint,
    index_name=index_name,
    credential=AzureKeyCredential(key)
)

# Prepare and clean documents
documents = []
for _, row in df.iterrows():
    doc = {
        "id": str(row["id"]),
        "type": str(row["type"]),
        "name": str(row["name"]),
        "description": str(row["description"]),
        "columns": str(row["columns"])
    }
    documents.append(doc)

# Upload documents
result = search_client.upload_documents(documents=documents)
print(f"[✓] Uploaded {len(result)} documents.")