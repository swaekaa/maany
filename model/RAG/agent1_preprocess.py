# Preprocessor Agent: language detection, translation, voice-to-text
import json
from langdetect import detect
from deep_translator import GoogleTranslator  # more stable than googletrans
from speech_text import VoskRecognizer  # your Vosk wrapper

class InputPreprocessorAgent:   
    def __init__(self):
        # Update this path to your downloaded Vosk model
        model_path = r"C:\Users\Ishan\Automation\SIH25\vosk-model-small-en-us-0.15"



        self.vosk = VoskRecognizer(model_path)

    def run(self, input_json: dict, use_voice: bool = False) -> dict:
        """
        use_voice: if True, record audio and convert to text
        """

        # 1. Validate required fields
        required_fields = ["thread_id", "user_id"]
        for field in required_fields:
            if field not in input_json:
                raise ValueError(f"Missing required field: {field}")

        # 2. Get query (typed or voice)
        if use_voice:
            print("Recording voice input...")
            query = self.vosk.record_and_transcribe(duration=5)  # 5 seconds default
            print(f"Transcribed voice: {query}")
        else:
            if "query" not in input_json:
                raise ValueError("Missing 'query' for typed input")
            query = input_json["query"]

        # 3. Detect language
        try:
            lang = detect(query)
        except:
            lang = "en"

        # 4. Hinglish fix
        hinglish_words = ["hai", "kab", "nahi", "kya", "tum", "mera", "aap"]
        if lang in ["da","tl", "en"] and any(word in query.lower() for word in hinglish_words):
            lang = "hi"

        # 5. Translate to English if not English
        query_en = query
        if lang != "en":
            try:
                query_en = GoogleTranslator(source=lang, target='en').translate(query)
            except Exception as e:
                print("Translation failed:", e)

        # 6. Return normalized JSON
        return {
            "thread_id": input_json["thread_id"],
            "user_id": input_json["user_id"],
            "query": query,
            "query_en": query_en,
            "lang": lang
        }
