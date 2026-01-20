import re
from detoxify import Detoxify

class SafetyFilterAgent:
    def __init__(self, toxicity_threshold=0.5):
        self.toxicity_threshold = toxicity_threshold
        self.detoxify = Detoxify('original')  # pre-trained toxicity model

    def contains_pii(self, text: str) -> bool:
        # Regex patterns
        phone_pattern = r"\b\d{10}\b"
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}"
        aadhaar_pattern = r"\b\d{4}\s\d{4}\s\d{4}\b"

        # Keyword-based rules
        sensitive_keywords = [
            "aadhaar", "pan card", "passport",
            "account number", "ifsc", "upi",
            "password", "ssn", "social security",
            "credit card", "debit card", "cvv"
        ]

        if (re.search(phone_pattern, text) or 
            re.search(email_pattern, text) or 
            re.search(aadhaar_pattern, text)):
            return True

        for kw in sensitive_keywords:
            if kw in text.lower():
                return True

        return False

    def run(self, preprocessed_json: dict) -> dict:
        query = preprocessed_json["query_en"]

        # 1. Toxicity check
        tox_scores = self.detoxify.predict(query)
        toxic_prob = tox_scores.get("toxicity", 0)

        # 2. PII check
        has_pii = self.contains_pii(query)

        # 3. Decide safety
        safe = True
        reason = None
        if toxic_prob > self.toxicity_threshold:
            safe = False
            reason = "Toxic content detected"
        elif has_pii:
            safe = False
            reason = "PII detected"

        # Return extended JSON
        return {
            **preprocessed_json,
            "safety": {
                "safe": safe,
                "reason": reason,
                "toxicity_score": float(toxic_prob),
                "pii": has_pii
            }
        }