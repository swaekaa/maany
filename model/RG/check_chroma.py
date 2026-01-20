from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

# Point to your persist directory
persist_directory = r"C:\Users\ishan\Automation\SIH25\RAG\chroma_db"

# Use the same embedding model you used when creating the DB
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Load the existing vector store
vs = Chroma(
    collection_name="college_pdfsn",
    embedding_function=embeddings,
    persist_directory=persist_directory
)

# === Sanity checks ===
print("✅ Connected to Chroma")
print("Total docs in collection:", vs._collection.count())

# Try retrieving something simple
retriever = vs.as_retriever(search_kwargs={"k": 3})
docs = retriever.get_relevant_documents("software engineering")

print("Docs retrieved:", len(docs))
for i, d in enumerate(docs, 1):
    print(f"\n--- Doc {i} ---\n{d.page_content[:300]}")
