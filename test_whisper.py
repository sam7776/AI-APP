from faster_whisper import WhisperModel
import traceback

print("Starting Whisper Test...")
try:
    print("Initializing WhisperModel (cpu, int8)...")
    model = WhisperModel("base", device="cpu", compute_type="int8")
    print("Model initialized successfully.")
    
    print("Running dummy transcription...")
    # Create a dummy silent audio chunk
    import numpy as np
    dummy_audio = np.zeros(16000, dtype=np.float32)
    segments, info = model.transcribe(dummy_audio, beam_size=5)
    print("Transcription finished.")
    for segment in segments:
        print(segment.text)
    print("Test Complete.")

except Exception:
    print("An error occurred:")
    traceback.print_exc()

input("Press Enter to exit...")
