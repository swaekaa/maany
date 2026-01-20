import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

class ResponseGeneratorAgent:
    def __init__(self, model="gemini-1.5-flash"):
        # Load .env file if present
        load_dotenv()

        # Ensure API key is set
        if not os.getenv("GOOGLE_API_KEY"):
            raise ValueError("❌ GOOGLE_API_KEY not found. Please set it in .env or environment variables.")

        # Initialize Gemini LLM
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            temperature=0.3  # low = factual, high = creative
        )

    def run(self, input_json: dict) -> dict:
        query_en = input_json.get("query_en", input_json["query"])
        context = input_json.get("context", "")

        # Build structured prompt
        prompt = f"""
        You are CampusConnect AI, a helpful assistant for university queries.

        Context:
        {context}

        User Question:
        {query_en}

        Answer in a clear, concise, and factual way.
        """

        # Call Gemini LLM
        try:
            response = self.llm.invoke(prompt)
            answer = response.content
        except Exception as e:
            answer = f"⚠️ LLM call failed: {str(e)}"

        # Return structured response
        return {
            "thread_id": input_json["thread_id"],
            "user_id": input_json["user_id"],
            "query": input_json["query"],
            "query_en": query_en,
            "lang": input_json.get("lang", "en"),
            "response": answer,
            "sources": input_json.get("sources", []),
            "safety": input_json.get("safety", {})
        }