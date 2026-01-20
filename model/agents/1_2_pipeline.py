# 1_2_pipeline.py
import sys
import os

sys.path.append(os.path.dirname(__file__))

from agent1_preprocess import InputPreprocessorAgent
from agent2_safety import SafetyFilterAgent  # <- import real agent

def main():
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

    print("Processed input:", processed_input)

    # Agent 2: Safety Check
    safety_result = safety_agent.run(processed_input)
    if not safety_result["safety"]["safe"]:
        print("Blocked by Safety Agent:", safety_result["safety"]["reason"])
        return

    # Ready for next stage (Responder/RAG)
    print("Input passed safety check, ready for processing by Responder/RAG")

if __name__ == "__main__":
    main()

