# %%
# %% 
# Basic imports
import os
from dotenv import load_dotenv
import sqlite3
from pathlib import Path
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import HumanMessage

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


# %%
# %% 
# Initialize LLM & embeddings
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
embeddings = OllamaEmbeddings(model="nomic-embed-text")

# Connect to existing Chroma DB (populated separately)
persist_directory = r"C:\Users\ishan\Automation\SIH25\RAG\chroma_db"
vector_store = Chroma(
    collection_name="college_pdfsn",
    embedding_function=embeddings,
    persist_directory=persist_directory
)

# Retriever for RAG
retriever = vector_store.as_retriever(search_kwargs={"k": 5})


# %%
# %% 
# SQLite DB file
DB_FILE = Path("conversation_memory.db")

# Initialize SQLite connection
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
cursor = conn.cursor()

# Drop old table if exists and create a new one with thread_id
cursor.execute("DROP TABLE IF EXISTS conversation_history")

cursor.execute("""
CREATE TABLE conversation_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    thread_id TEXT NOT NULL,
    role TEXT NOT NULL,  -- 'user' or 'assistant'
    text TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()


# %%
def get_conversation_history(user_id, thread_id, last_n=5):
    cursor.execute("""
        SELECT role, text FROM conversation_history
        WHERE user_id = ? AND thread_id = ?
        ORDER BY timestamp DESC
        LIMIT ?
    """, (user_id, thread_id, last_n))
    rows = cursor.fetchall()
    # Reverse to chronological order
    return [{"role": r[0], "text": r[1]} for r in reversed(rows)]

def save_turn(user_id, thread_id, role, text):
    cursor.execute("""
        INSERT INTO conversation_history (user_id, thread_id, role, text)
        VALUES (?, ?, ?, ?)
    """, (user_id, thread_id, role, text))
    conn.commit()


# %%
# %% 
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


# %%
def rg_generate(user_id, thread_id, rag_output, language="en", history_turns=5):
    # Retrieve conversation history for this thread
    history = get_conversation_history(user_id, thread_id, last_n=history_turns)
    history_text = ""
    for turn in history:
        history_text += f"{turn['role'].capitalize()}: {turn['text']}\n"

    # Context from RAG
    context = "\n".join(rag_output["context"])
    question = rag_output["query"]

    # Construct prompt
    final_prompt = f"""
You are an academic assistant. Answer the question using the previous conversation history and  given context as much as possible try to use the context as your main source of knowledge and try to relate as much information from the context as possible if the user asks anything which is completely not there in the context not even a little then use your own brain and when you do in the end just mention "(not from context)"
. And if the user in not talking about academics you can talk normally. Answer clearly and concisely.

Conversation History:
{history_text}

Context:
{context}

Question: {question}
Answer in {language}:
"""

    from langchain.schema import HumanMessage
    response = llm.invoke([HumanMessage(content=final_prompt)])
    response_text = response.content

    # Save current turn
    save_turn(user_id, thread_id, "user", question)
    save_turn(user_id, thread_id, "assistant", response_text)

    sources = [meta.get("source", "N/A") for meta in rag_output["metadata"]]
    return response_text, sources


# %%
user_id = "user_123"
thread_id = "thread_1"  # each separate chat can have a unique thread ID
user_query = "Whats my name"

rag_output = rag_query(user_query, retriever)
answer, sources = rg_generate(user_id, thread_id, rag_output, language="en")

print("Answer:\n", answer)



