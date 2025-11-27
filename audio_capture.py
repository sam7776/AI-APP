import soundcard as sc
import numpy as np
import threading
import time
import queue

import warnings
# Suppress soundcard runtime warnings (data discontinuity)
warnings.filterwarnings("ignore", category=UserWarning, module='soundcard')
# Note: soundcard seems to use a custom warning class or UserWarning. 
# Let's try to catch the specific one if possible, or just ignore all from soundcard.
# Based on the log: SoundcardRuntimeWarning.
try:
    from soundcard.mediafoundation import SoundcardRuntimeWarning
    warnings.simplefilter("ignore", SoundcardRuntimeWarning)
except ImportError:
    pass

class AudioCapture:
    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate
        self.audio_queue = queue.Queue()
        self.is_recording = False
        self.thread = None

    def _record_loop(self):
        """Background loop to record audio using soundcard with VAD."""
        print("Finding loopback device...")
        try:
            # Find loopback mic
            mics = sc.all_microphones(include_loopback=True)
            default_speaker = sc.default_speaker()
            loopback_mic = None
            
            # Heuristic to find the loopback for default speaker
            for mic in mics:
                if mic.isloopback and (default_speaker.name in mic.name or mic.name in default_speaker.name):
                    loopback_mic = mic
                    break
            
            # Fallback
            if not loopback_mic:
                for mic in mics:
                    if mic.isloopback:
                        loopback_mic = mic
                        break
            
            if not loopback_mic:
                print("Error: No loopback device found! Audio capture will fail.")
                return

            print(f"Recording from: {loopback_mic.name}")
            
            # VAD Parameters
            FRAME_DURATION = 0.1  # seconds
            SILENCE_THRESHOLD = 0.03 # RMS amplitude (Increased to filter noise)
            SILENCE_DURATION = 1.5 # seconds of silence to trigger processing
            MAX_DURATION = 30.0 # seconds max before forcing processing
            
            buffer = []
            silence_start_time = None
            has_speech = False
            
            with loopback_mic.recorder(samplerate=self.sample_rate) as recorder:
                while self.is_recording:
                    # Record small chunks
                    num_frames = int(self.sample_rate * FRAME_DURATION)
                    data = recorder.record(numframes=num_frames)
                    
                    # Convert to mono
                    if data.shape[1] > 1:
                        data = data.mean(axis=1)
                    
                    data = data.flatten().astype(np.float32)
                    
                    # Calculate RMS amplitude
                    rms = np.sqrt(np.mean(data**2))
                    
                    if rms > SILENCE_THRESHOLD:
                        # Speech detected
                        if not has_speech:
                            print("Speech started...")
                            has_speech = True
                        silence_start_time = None
                        buffer.append(data)
                    else:
                        # Silence detected
                        if has_speech:
                            buffer.append(data) # Keep trailing silence for natural cut
                            
                            if silence_start_time is None:
                                silence_start_time = time.time()
                            
                            # Check if silence has lasted long enough
                            if time.time() - silence_start_time > SILENCE_DURATION:
                                print("Silence detected, processing phrase...")
                                # Concatenate buffer
                                full_audio = np.concatenate(buffer)
                                self.audio_queue.put(full_audio)
                                
                                # Reset
                                buffer = []
                                has_speech = False
                                silence_start_time = None
                        else:
                            # Just silence, ignore
                            pass
                            
                    # Force flush if too long
                    if len(buffer) * num_frames / self.sample_rate > MAX_DURATION:
                         print("Max duration reached, forcing process...")
                         full_audio = np.concatenate(buffer)
                         self.audio_queue.put(full_audio)
                         buffer = []
                         has_speech = False
                         silence_start_time = None
                    
        except Exception as e:
            print(f"Error in audio recording loop: {e}")
            import traceback
            traceback.print_exc()

    def start(self):
        """Start capturing audio."""
        if self.is_recording:
            return
            
        self.is_recording = True
        self.thread = threading.Thread(target=self._record_loop)
        self.thread.daemon = True
        self.thread.start()
        print("Audio capture started.")

    def stop(self):
        """Stop audio capture."""
        self.is_recording = False
        if self.thread:
            self.thread.join(timeout=1.0)
            self.thread = None

    def get_audio_chunk(self):
        """Retrieve a chunk of audio from the queue."""
        try:
            return self.audio_queue.get_nowait()
        except queue.Empty:
            return None
