from agent1_preprocess import InputPreprocessorAgent
from agent2_safety import SafetyFilterAgent
from agent4_response import ResponseGeneratorAgent
import json

def main():
    # Initialize all agents
    preprocessor = InputPreprocessorAgent()
    safety_filter = SafetyFilterAgent()
    response_agent = ResponseGeneratorAgent()

    # Example raw user input
    raw_input = {
        "thread_id": "abc123",
        "user_id": "u001",
        "query": "Hostel fee kab dena hai?"  # Hinglish input
    }

    # 1️⃣ Preprocess input (translate, detect language)
    preprocessed = preprocessor.run(raw_input)
    print("After preprocessing:")
    print(json.dumps(preprocessed, indent=2))

    # 2️⃣ Safety check
    safety_checked = safety_filter.run(preprocessed)
    print("\nAfter safety check:")
    print(json.dumps(safety_checked, indent=2))

    # 3️⃣ Generate response
    # Add some context for testing
    safety_checked["context"] = "According to the official notice, hostel fees are due on September 10, 2025."
    final_output = response_agent.run(safety_checked)
    print("\nFinal Response:")
    print(json.dumps(final_output, indent=2))

if __name__ == "__main__":
    main()

# python 4_pipeline.py