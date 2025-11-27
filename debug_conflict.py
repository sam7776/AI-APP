print("Starting Conflict Test...")
try:
    print("Importing PyQt5...")
    from PyQt5.QtWidgets import QApplication
    print("PyQt5 imported.")
    
    print("Importing faster_whisper...")
    from faster_whisper import WhisperModel
    print("faster_whisper imported.")
    
    print("Initializing WhisperModel...")
    model = WhisperModel("base", device="cpu", compute_type="int8")
    print("WhisperModel initialized successfully.")

except Exception as e:
    print("CRITICAL ERROR:")
    import traceback
    traceback.print_exc()

input("Press Enter to exit...")
