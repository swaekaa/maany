# 1_2_pipeline.py
import sys
import os
from pathlib import Path
import json

sys.path.append(os.path.dirname(__file__))

from agent1_preprocess import InputPreprocessorAgent
from agent2_safety import SafetyFilterAgent
from RAG1 import rag_query, rg_generate

def main():
    # Initialize agents
    input_agent = InputPreprocessorAgent()
    safety_agent = SafetyFilterAgent()

    print("Choose input method:")
    print("1. Type your query")
    print("2. Speak your query")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        user_query = input("Enter your query: ")
        user_input = {
            "thread_id": "thread_001",
            "user_id": "user_001",
            "query": user_query
        }
        use_voice = False
    elif choice == "2":
        user_input = {
            "thread_id": "thread_002",
            "user_id": "user_002"
        }
        use_voice = True
    else:
        print("Invalid choice")
        return

    # Agent 1: Input Preprocessing
    try:
        processed_input = input_agent.run(user_input, use_voice=use_voice)
    except Exception as e:
        print("Error in preprocessing:", e)
        return

    # Agent 2: Safety Check
    safety_result = safety_agent.run(processed_input)
    if not safety_result["safety"]["safe"]:
        reason = safety_result["safety"]["reason"]
        print(f"Blocked by Safety Agent: {reason}")
        return

    # RAG Retrieval
    rag_output = rag_query(processed_input["query_en"])
    if not rag_output["context"]:
        print("No relevant context found in PDFs.")
        return

    # Response Generation
    response_text, sources = rg_generate(
        user_id=processed_input["user_id"],
        thread_id=processed_input["thread_id"],
        preprocessed_json=safety_result,
        rag_output=rag_output,
        history_turns=5
    )

    # Print concise output for live testing
    print("\n--- RAG Input (for inspection) ---")
    print(f"Query: {processed_input['query_en']}")
    print(f"Context (first 300 chars): {rag_output['context'][0][:300]}")
    print(f"Metadata: {rag_output['metadata']}")
    print("\n--- FINAL ANSWER ---")
    print(response_text)

    # Optional: Save log for debugging
    log_path = Path("live_test_log.json")
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump({
            "processed_input": processed_input,
            "safety_result": safety_result,
            "rag_output": rag_output,
            "final_answer": response_text,
            "sources": sources
        }, f, ensure_ascii=False, indent=4)
        print(f"\n✅ Log saved to {log_path}")

if __name__ == "__main__":
    main()
