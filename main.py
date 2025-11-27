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

        # 2. Profile Selection
        print("Launching Profile Selection...")
        from PyQt5.QtWidgets import QApplication
        from profile_ui import ProfileSelectionWindow
        
        # We need a temporary QApplication for the profile window if one doesn't exist
        # But AppController creates one too. 
        # Strategy: Create one QApplication here, pass it or let AppController handle it.
        # Actually, AppController creates QApplication(sys.argv). 
        # We should create it ONCE here.
        
        app = QApplication(sys.argv)
        
        profile_win = ProfileSelectionWindow()
        profile_win.show()
        app.exec_() # Wait for window to close
        
        profile_data, profile_filename = profile_win.get_profile()
        
        if not profile_data:
            print("No profile selected. Exiting.")
            sys.exit(0)
            
        print(f"Profile loaded: {profile_data.get('name')}")

        # 3. NOW import and start AppController
        print("Importing UI modules...")
        from app_controller import AppController
        
        print("Initializing Controller...")
        # Pass app instance to avoid creating another one, or just pass profile
        # We need to modify AppController to accept existing app or not create new one if exists.
        # Let's modify AppController to accept profile_data and profile_filename
        
        # Note: AppController.__init__ creates QApplication. We should change that.
        # But for now, let's just pass the data.
        controller = AppController(stt_engine, profile_data, profile_filename, app_instance=app)
        print("Controller initialized. Starting...")
        controller.start()
        
    except Exception as e:
        print("CRITICAL ERROR in Main:")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
