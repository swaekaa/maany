# %% Testing with preprocessed + safety output
from agent1_preprocess import InputPreprocessorAgent
from agent2_safety import SafetyFilterAgent

# Initialize agents
preprocessor = InputPreprocessorAgent()
safety = SafetyFilterAgent()

# User input
user_id = "user_123"
thread_id = "thread_1"
user_query = "Hello"

# 1️⃣ Preprocess input
preprocessed_json = preprocessor.run({
    "thread_id": thread_id,
    "user_id": user_id,
    "query": user_query
})

# 2️⃣ Safety filter
preprocessed_json = safety.run(preprocessed_json)

# 3️⃣ Retrieve RAG context
rag_output = rag_query(preprocessed_json["query_en"], retriever)

# 4️⃣ Generate response using updated rg_generate
answer, sources = rg_generate(user_id, thread_id, preprocessed_json, rag_output)

# 5️⃣ Print nicely formatted output
print("Preprocessed & Safety Output:\n", preprocessed_json)
print("\nRAG Output:\n", rag_output)
print("\nGenerated Answer:\n", answer)
print("\nSources:\n", sources)
