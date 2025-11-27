from faster_whisper import WhisperModel
import numpy as np
import os

class STTEngine:
    def __init__(self, model_size="small"):
        print(f"Loading Faster-Whisper model: {model_size}...")
        # Run on CPU with INT8 quantization for speed and compatibility
        self.model = WhisperModel(model_size, device="cpu", compute_type="int8")
        print("Faster-Whisper model loaded.")

    def transcribe(self, audio_chunk):
        """
        Transcribe a numpy array of audio.
        audio_chunk: np.array of shape (N, channels) or (N,)
        """
        if audio_chunk is None or len(audio_chunk) == 0:
            return ""

        # Faster-Whisper expects float32 mono audio
        if len(audio_chunk.shape) > 1:
            audio_chunk = audio_chunk.mean(axis=1)
        
        audio_chunk = audio_chunk.astype(np.float32)

        # Skip very short chunks
        if len(audio_chunk) < 16000 * 0.5: 
            return ""

        # faster-whisper transcribe expects a file path or a binary file-like object.
        # However, it also accepts a numpy array directly in recent versions.
        # segments, info = model.transcribe(audio_chunk, beam_size=5)
        
        try:
            segments, info = self.model.transcribe(audio_chunk, beam_size=5)
            
            # Collect text from segments
            text = " ".join([segment.text for segment in segments]).strip()
            
            # Filter hallucinations
            hallucinations = ["You", "Thank you", "Thanks", "Subtitle by", "Amara.org", "MBC", "Copyright"]
            if text in hallucinations or len(text) < 2:
                return ""
            
            # Check for repeated hallucinations (e.g. "You You You")
            if text.replace(" ", "") in ["You"*i for i in range(1, 10)]:
                return ""

            return text
        except Exception as e:
            print(f"Transcription error: {e}")
            return ""
