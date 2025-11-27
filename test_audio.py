import sounddevice as sd
import traceback

print(f"SoundDevice Version: {sd.__version__}")

print("\nHost APIs:")
print(sd.query_hostapis())

print("\nDevices:")
print(sd.query_devices())

print("\nAttempting to open loopback stream...")
try:
    # Try finding the default output device
    wasapi_index = -1
    for i, api in enumerate(sd.query_hostapis()):
        if 'WASAPI' in api['name']:
            wasapi_index = i
            break
    
    if wasapi_index == -1:
        print("WASAPI not found!")
    else:
        default_output = sd.query_devices(kind='output')
        print(f"Default Output Device: {default_output['name']}")
        
        # Try method 1: Direct kwarg
        try:
            print("Method 1: loopback=True kwarg")
            with sd.InputStream(device=default_output['index'], channels=1, loopback=True) as stream:
                print("Success with loopback=True!")
        except Exception as e:
            print(f"Method 1 failed: {e}")

        # Try method 2: extra_settings
        try:
            print("Method 2: extra_settings=sd.WasapiSettings(loopback=True)")
            wasapi_settings = sd.WasapiSettings(loopback=True)
            with sd.InputStream(device=default_output['index'], channels=1, extra_settings=wasapi_settings) as stream:
                print("Success with extra_settings!")
        except Exception as e:
            print(f"Method 2 failed: {e}")

except Exception as e:
    traceback.print_exc()

input("Press Enter to exit...")
