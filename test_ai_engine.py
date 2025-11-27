from ai_engine import AIEngine
import traceback

try:
    print("Initializing AI Engine...")
    ai = AIEngine()
    print("AI Engine initialized.")
    
    print("Testing generate_response...")
    response = ai.generate_response("Hello, are you working?")
    print(f"Response: {response}")
    
    if response and "Error" not in response:
        print("SUCCESS: AI Engine is working.")
    else:
        print("FAILURE: AI Engine returned an error or empty response.")

except Exception:
    traceback.print_exc()
