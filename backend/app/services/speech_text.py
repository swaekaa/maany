# speech_text.py
import vosk
import sounddevice as sd
import queue
import json
import os

q = queue.Queue()

def vosk_callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

class VoskRecognizer:
    def __init__(self, model_path=None):
        # Use your downloaded Vosk model if none is provided
        if model_path is None:
            model_path = r"C:\Users\Ishan\Automation\SIH25\vosk-model-small-en-us-0.15"


        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Vosk model folder not found at {model_path}")
        self.model = vosk.Model(model_path)
        self.rec = vosk.KaldiRecognizer(self.model, 16000)

    def record_and_transcribe(self, duration=5):
        text = ""
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, callback=vosk_callback):
            print("Speak now...")
            for _ in range(0, int(16000 / 8000 * duration)):
                data = q.get()
                if self.rec.AcceptWaveform(data):
                    res = json.loads(self.rec.Result())
                    text += " " + res.get("text", "")
            final_res = json.loads(self.rec.FinalResult())
            text += " " + final_res.get("text", "")
        return text.strip()
