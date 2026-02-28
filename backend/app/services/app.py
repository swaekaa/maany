# app.py
import streamlit as st
from agent1_preprocess import InputPreprocessorAgent
from agent2_safety import SafetyFilterAgent
from RAG1 import rag_query, rg_generate

st.set_page_config(page_title="RAG + RG Live Test", layout="wide")
st.title("RAG + Response Generation System")

# Initialize agents
input_agent = InputPreprocessorAgent()
safety_agent = SafetyFilterAgent()

# User input
input_method = st.radio("Choose input method:", ["Type Query", "Voice Query"])
user_id = "user_streamlit"
thread_id = "thread_streamlit"

if input_method == "Type Query":
    user_query = st.text_input("Enter your query:")
    use_voice = False
else:
    st.info("Voice input currently uses Vosk; click 'Record' to capture.")
    use_voice = True
    if st.button("Record"):
        user_query = None  # voice recording handled by agent internally

if st.button("Submit") or (use_voice and user_query is not None):
    # Prepare input JSON
    user_input = {
        "thread_id": thread_id,
        "user_id": user_id
    }
    if not use_voice:
        user_input["query"] = user_query

    # 1️⃣ Preprocess
    try:
        processed_input = input_agent.run(user_input, use_voice=use_voice)
    except Exception as e:
        st.error(f"Error in preprocessing: {e}")
        st.stop()

    # 2️⃣ Safety Check
    safety_result = safety_agent.run(processed_input)
    if not safety_result["safety"]["safe"]:
        st.warning(f"Blocked by Safety Agent: {safety_result['safety']['reason']}")
        st.stop()

    # 3️⃣ RAG Retrieval
    rag_output = rag_query(processed_input["query_en"])
    if not rag_output["context"]:
        st.info("No relevant context found in PDFs.")
        st.stop()

    # 4️⃣ Response Generation
    response_text, sources = rg_generate(
        user_id=processed_input["user_id"],
        thread_id=processed_input["thread_id"],
        preprocessed_json=safety_result,
        rag_output=rag_output,
        history_turns=5
    )

    # 5️⃣ Display results
    with st.expander("RAG Input (for inspection)"):
        st.write(f"Query: {processed_input['query_en']}")
        st.write(f"Context (first 300 chars): {rag_output['context'][0][:300]}")
        st.write(f"Metadata: {rag_output['metadata']}")

    st.success("Final Answer:")
    st.write(response_text)
