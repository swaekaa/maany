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
# %%
def rg_generate(user_id, thread_id, preprocessed_json, rag_output, history_turns=5):
    """
    Generate response based on RAG context, conversation history, and safety checks.
    preprocessed_json: output from preprocessor + safety agent
    """
    # 1️⃣ Retrieve conversation history
    history = get_conversation_history(user_id, thread_id, last_n=history_turns)
    history_text = ""
    for turn in history:
        history_text += f"{turn['role'].capitalize()}: {turn['text']}\n"

    # 2️⃣ Extract context & user info
    context_text = "\n".join(rag_output.get("context", []))
    question = preprocessed_json["query_en"]
    language = preprocessed_json.get("lang", "en")

    # 3️⃣ Safety handling
    safety = preprocessed_json.get("safety", {})
    safe = safety.get("safe", True)
    toxic_reason = safety.get("reason", "")
    pii_flag = safety.get("pii", False)

    # 4️⃣ Construct dynamic prompt
    if not safe:
        if pii_flag:
            # PII case
            final_prompt = f"""
You are an academic assistant.
A user has shared sensitive personal information. 
You must NOT use the context for answering.
Respond clearly that sensitive information was shared and you cannot provide a response.
"""
        else:
            # Toxic case
            final_prompt = f"""
You are an academic assistant.
A user query was flagged as unsafe due to: {toxic_reason}.
Do NOT use the context for answering.
Respond clearly stating that the request cannot be processed because of this reason.
"""
    else:
        # Safe case → normal prompt
        final_prompt = f"""
You are an academic assistant. Answer clearly and concisely.
Use the context as your main source of knowledge and relate information from it whenever possible.
If the query is not related to the context at all reply like an Academic assistant normally without refering to the context.

{f'Conversation History:\n{history_text}' if history_text else ''}

Context:
{context_text}

Question: {question}
Answer in {language}:
"""

    # 5️⃣ Invoke LLM                  
    response = llm.invoke([HumanMessage(content=final_prompt)])
    response_text = response.content

    # 6️⃣ Save conversation (even blocked queries)
    save_turn(user_id, thread_id, "user", question)
    save_turn(user_id, thread_id, "assistant", response_text)

    sources = [meta.get("source", "N/A") for meta in rag_output.get("metadata", [])]
    return response_text, sources





