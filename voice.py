import whisper

model = whisper.load_model("base")

def voice_to_text(path):
    result = model.transcribe(path, language="ru")
    return result["text"]
