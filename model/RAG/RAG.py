import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# ==========================
# Load API Keys
# ==========================
load_dotenv("api.env")

langsmith_key = os.getenv("LANGSMITH_API_KEY")
if not langsmith_key:
    raise ValueError("LANGSMITH_API_KEY not found in environment or api.env!")
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = langsmith_key

google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment or api.env!")
os.environ["GOOGLE_API_KEY"] = google_api_key

# ==========================
# Initialize Core Components
# ==========================
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
embeddings = OllamaEmbeddings(model="nomic-embed-text")
persist_directory = r"C:\Users\ishan\Automation\SIH25\RAG\chroma_db"


vector_store = Chroma(
    collection_name="college_pdfsn",
    embedding_function=embeddings,
    persist_directory="persist_directory"
)

retriever = vector_store.as_retriever(search_kwargs={"k": 5})

# ==========================
# PDF Loading & Chunking
# ==========================
pdf_folder = r"C:\Users\ishan\Automation\SIH25\RAG\pdfs"
all_docs = []

for file in os.listdir(pdf_folder):
    if file.endswith(".pdf"):
        pdf_path = os.path.join(pdf_folder, file)
        print(f"📄 Loading: {file}")
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()
        all_docs.extend(docs)

print(f"\n✅ Total documents loaded: {len(all_docs)}")
if all_docs:
    print("Example:", all_docs[0].page_content[:500])

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100
)

splits = text_splitter.split_documents(all_docs)
print(f"✅ Total chunks created: {len(splits)}")
if splits:
    print("Example chunk:\n", splits[0].page_content[:500])

# ==========================
# RAG Query Function
# ==========================

def rag_query(query: str, retriever=retriever):
    """
    Takes a user query and returns:
    - retrieved document chunks
    - metadata
    """
    retrieved_docs = retriever.get_relevant_documents(query)
    output = {
        "query": query,
        "context": [doc.page_content for doc in retrieved_docs],
        "metadata": [doc.metadata for doc in retrieved_docs]
    }
    return output

print("🔎 Retriever test:")
docs = retriever.get_relevant_documents("software engineering")
print("Docs returned:", len(docs))
if docs:
    print(docs[0].page_content[:500])

