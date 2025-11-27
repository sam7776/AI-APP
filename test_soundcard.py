import soundcard as sc
import numpy as np

print("Testing SoundCard Library (Loopback)...")

try:
    # List all microphones including loopback
    print("Scanning for loopback devices...")
    mics = sc.all_microphones(include_loopback=True)
    
    loopback_mic = None
    default_speaker = sc.default_speaker()
    print(f"Default Speaker: {default_speaker.name}")

    # Try to find the loopback device for the default speaker
    for mic in mics:
        # print(f" - {mic.name} (Loopback: {mic.isloopback})")
        if mic.isloopback:
            # Simple heuristic: if speaker name is in mic name or vice versa
            if default_speaker.name in mic.name or mic.name in default_speaker.name:
                loopback_mic = mic
                break
    
    # Fallback: take first loopback
    if not loopback_mic:
        for mic in mics:
            if mic.isloopback:
                loopback_mic = mic
                break
    
    if loopback_mic:
        print(f"\nSelected Loopback Device: {loopback_mic.name}")
        print("Recording 3 seconds of system audio...")
        
        # Record
        data = loopback_mic.record(samplerate=16000, numframes=16000*3)
        print(f"Recorded data shape: {data.shape}")
        
        # Check signal
        if np.abs(data).mean() > 0:
            print("Success! Audio signal detected.")
        else:
            print("Warning: Recorded silence. Make sure audio is playing.")
    else:
        print("No loopback microphone found!")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

input("Press Enter to exit...")
