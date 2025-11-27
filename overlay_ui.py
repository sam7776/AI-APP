from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject
from PyQt5.QtGui import QColor, QFont
import sys

class OverlayWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Window flags for transparency and stay-on-top
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Make the window click-through (optional, but good for overlays)
        # self.setAttribute(Qt.WA_TransparentForMouseEvents) 
        
        # Hide from Screen Capture (Windows only)
        try:
            import ctypes
            # WDA_EXCLUDEFROMCAPTURE = 0x00000011
            # This prevents the window from being captured by screen sharing/recording
            hwnd = int(self.winId())
            ctypes.windll.user32.SetWindowDisplayAffinity(hwnd, 0x00000011)
            print("Window display affinity set to EXCLUDEFROMCAPTURE")
        except Exception as e:
            print(f"Failed to set window affinity: {e}") 

        # Geometry
        screen_geometry = QApplication.desktop().screenGeometry()
        window_width = 500
        window_height = 600
        x_pos = (screen_geometry.width() - window_width) // 2
        y_pos = 50
        self.setGeometry(x_pos, y_pos, window_width, window_height) # Top Center

        # Central Widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # Layout
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Labels
        self.status_label = QLabel("AI Assistant Active")
        self.status_label.setStyleSheet("color: lime; font-size: 12px;")
        self.layout.addWidget(self.status_label)

        self.text_label = QLabel("Listening...")
        self.text_label.setStyleSheet("color: white; font-size: 14px; background-color: rgba(0, 0, 0, 150); padding: 10px; border-radius: 5px;")
        self.text_label.setWordWrap(True)
        self.text_label.setAlignment(Qt.AlignTop)
        self.layout.addWidget(self.text_label)
        
        self.suggestion_label = QLabel("")
        self.suggestion_label.setStyleSheet("color: #00ffff; font-size: 14px; background-color: rgba(0, 0, 0, 180); padding: 10px; border-radius: 5px; border: 1px solid #00ffff;")
        self.suggestion_label.setWordWrap(True)
        self.suggestion_label.setAlignment(Qt.AlignTop)
        self.suggestion_label.hide() # Hide initially
        self.layout.addWidget(self.suggestion_label)

        self.layout.addStretch()

    def update_status(self, text):
        self.status_label.setText(text)

    def update_text(self, text):
        self.text_label.setText(text)

    def update_suggestion(self, text):
        if text:
            self.suggestion_label.setText(text)
            self.suggestion_label.show()
        else:
            self.suggestion_label.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = OverlayWindow()
    window.show()
    sys.exit(app.exec_())
