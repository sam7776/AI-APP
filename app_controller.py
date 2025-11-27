import sys
import keyboard
import threading
import time
from PyQt5.QtWidgets import QApplication
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw

from audio_capture import AudioCapture
from ai_engine import AIEngine
from overlay_ui import OverlayWindow
from screen_capture import ScreenCapture

def create_tray_icon(app_exit_callback):
    # Create a simple icon
    image = Image.new('RGB', (64, 64), color = (73, 109, 137))
    d = ImageDraw.Draw(image)
    d.text((10,10), "AI", fill=(255,255,0))

    def on_exit(icon, item):
        icon.stop()
        app_exit_callback()

    menu = Menu(MenuItem('Exit', on_exit))
    icon = Icon("AI Assistant", image, "AI Assistant", menu)
    return icon

from PyQt5.QtCore import QObject, pyqtSignal

class AppController(QObject):
    update_text_signal = pyqtSignal(str)
    update_status_signal = pyqtSignal(str)
    update_suggestion_signal = pyqtSignal(str)

    def __init__(self, stt_engine):
        super().__init__()
        print("Initializing AppController...")
        self.app = QApplication(sys.argv)
        print("PyQt App created.")
        self.window = OverlayWindow()
        print("Overlay Window created.")
        
        # Connect signals
        self.update_text_signal.connect(self.window.update_text)
        self.update_status_signal.connect(self.window.update_status)
        self.update_suggestion_signal.connect(self.window.update_suggestion)
        
        self.audio_capture = AudioCapture()
        print("Audio Capture initialized.")
        
        self.stt_engine = stt_engine
        print("STT Engine assigned.")
        
        self.ai_engine = AIEngine()
        print("AI Engine initialized.")
        self.screen_capture = ScreenCapture()
        print("Screen Capture initialized.")
        
        self.running = True
        self.transcript = ""
        self.last_ai_time = 0
        self.clear_transcript_next = False

    def start(self):
        self.window.show()
        
        # Register Hotkey
        try:
            keyboard.add_hotkey('ctrl+\\', self.toggle_overlay)
            print("Hotkey 'ctrl+\\' registered.")
        except Exception as e:
            print(f"Failed to register hotkey: {e}")
        
        # Start processing thread
        self.thread = threading.Thread(target=self.process_loop)
        self.thread.daemon = True
        self.thread.start()
        
        # Start Tray Icon
        self.tray_icon = create_tray_icon(self.quit_app)
        self.tray_thread = threading.Thread(target=self.tray_icon.run)
        self.tray_thread.daemon = True
        self.tray_thread.start()

        sys.exit(self.app.exec_())

    def toggle_overlay(self):
        if self.window.isVisible():
            self.window.hide()
        else:
            self.window.show()

    def quit_app(self):
        self.running = False
        self.app.quit()

    def process_loop(self):
        self.audio_capture.start()
        print("Listening...")
        
        while self.running:
            try:
                # 1. Audio
                audio_chunk = self.audio_capture.get_audio_chunk()
                if audio_chunk is not None:
                    # 2. STT
                    text = self.stt_engine.transcribe(audio_chunk)
                    if text:
                        # Clear previous transcript if AI has responded
                        if self.clear_transcript_next:
                            self.transcript = ""
                            self.clear_transcript_next = False
                            
                        print(f"Transcribed: {text}")
                        self.transcript += " " + text
                        
                        # Update UI via Signal
                        self.update_text_signal.emit(self.transcript[-300:])
                        
                        # 3. AI Trigger
                        current_time = time.time()
                        if "?" in text or (current_time - self.last_ai_time > 5 and len(text) > 10):
                            print("Querying Gemini...")
                            try:
                                self.update_status_signal.emit("Thinking...")
                                response = self.ai_engine.generate_response(self.transcript[-1000:])
                                if response:
                                    self.update_suggestion_signal.emit(response)
                                    self.clear_transcript_next = True # Reset transcript on next input
                                self.update_status_signal.emit("Active")
                            except:
                                pass
                            self.last_ai_time = current_time
                
                time.sleep(0.05)
            except Exception as e:
                print(f"Error in loop: {e}")
                time.sleep(1)

        self.audio_capture.stop()
