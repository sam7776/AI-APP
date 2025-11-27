import sys
import threading
import time
import queue
# NOTE: Do NOT import PyQt5 or AppController here to avoid DLL conflicts with faster-whisper

from audio_capture import AudioCapture
from stt_engine import STTEngine
from ai_engine import AIEngine
from screen_capture import ScreenCapture

# Global flags
running = True

if __name__ == "__main__":
    # Minimize Console Window
    import ctypes
    try:
        kernel32 = ctypes.WinDLL('kernel32')
        user32 = ctypes.WinDLL('user32')
        hwnd = kernel32.GetConsoleWindow()
        if hwnd:
            user32.ShowWindow(hwnd, 6) # SW_MINIMIZE = 6
    except Exception:
        pass

    print("Initializing Application...")
    try:
        # 1. Initialize STT Engine FIRST (loads faster-whisper / CTranslate2)
        # This must happen before ANY PyQt5 imports to avoid DLL conflicts (libomp/mkl)
        print("Pre-initializing STT Engine...")
        stt_engine = STTEngine(model_size="base")
        print("STT Engine pre-initialized successfully.")

        # 2. NOW we can import PyQt5 and the AppController
        print("Importing UI modules...")
        from app_controller import AppController
        
        print("Initializing Controller...")
        controller = AppController(stt_engine)
        print("Controller initialized. Starting...")
        controller.start()
        
    except Exception as e:
        print("CRITICAL ERROR in Main:")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
