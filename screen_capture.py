import mss
import numpy as np
from PIL import Image

class ScreenCapture:
    def __init__(self):
        self.sct = mss.mss()

    def capture_screen(self):
        """Capture the primary screen and return a PIL Image."""
        # Capture the first monitor (primary)
        monitor = self.sct.monitors[1] 
        sct_img = self.sct.grab(monitor)
        
        # Convert to PIL Image
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        return img

    def capture_region(self, top, left, width, height):
        """Capture a specific region."""
        monitor = {"top": top, "left": left, "width": width, "height": height}
        sct_img = self.sct.grab(monitor)
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        return img
