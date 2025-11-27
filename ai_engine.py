import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIEngine:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-flash-latest')
        self.chat = self.model.start_chat(history=[])
        
        # System prompt / Context setup
        self.system_prompt = """
        You are a candidate in a job interview. You are an expert developer.
        Your goal is to answer the interviewer's questions in real-time.

        **Response Style & Tone:**
        - **Tone**: Natural, conversational, and human-like. Avoid robotic AI phrases like "Here is a solution" or "In this scenario". Speak like a professional Indian developer: polite, direct, and confident.
        - **Perspective**: Always use the FIRST PERSON ("I have worked on...", "I usually do...").

        **Adaptive Answering Strategy:**
        1. **Short/Factual Question**: Give a crisp, 1-2 sentence answer.
        2. **Detailed/Deep Question**: Provide a comprehensive answer with specific examples.
        3. **Coding/Technical Question**: Explain the logic briefly and provide a code snippet or specific technical approach.
        4. **Scenario-based Question**: Tackle the specific scenario directly. Explain your thought process and how you would handle that exact situation.

        **Critical Rules:**
        - Do NOT say "I suggest you say..." or "You can answer by...". Just ANSWER the question directly.
        - If the transcript is unclear or empty, return nothing (None).
        """

    def generate_response(self, text_input, image_input=None):
        """
        Generate a response from Gemini based on text and optional image.
        """
        if not text_input and not image_input:
            return None

        prompt_parts = [self.system_prompt]
        
        if image_input:
            prompt_parts.append(image_input)
        
        if text_input:
            prompt_parts.append(f"Context/Transcript: {text_input}")
            
        try:
            # We use generate_content for single turn or chat.send_message for history.
            # For a "copilot" that sees a stream, maintaining full history might get too long or confused by partial transcripts.
            # A sliding window or just sending the latest context + query is often better for latency and relevance.
            # Let's try stateless first for simplicity and speed, or use chat if we want it to remember previous turns.
            # Given the "real-time" nature, stateless with a sliding window of context is usually safer to avoid getting stuck in a bad state.
            
            response = self.model.generate_content(prompt_parts)
            return response.text
        except Exception as e:
            print(f"Gemini API Error: {e}")
            return "Error generating response."

    def update_system_prompt(self, new_prompt):
        self.system_prompt = new_prompt
