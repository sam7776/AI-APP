import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class AIEngine:
    def __init__(self, profile_data=None):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-flash-latest')
        self.chat = self.model.start_chat(history=[])
        
        # Build Context from Profile
        intro_context = ""
        if profile_data:
            name = profile_data.get('name', 'Candidate')
            intro = profile_data.get('intro', '')
            company = profile_data.get('company', '')
            skills = profile_data.get('skills', '')
            projects = profile_data.get('projects', '')
            
            intro_context = f"""
            **YOUR PERSONA (The User):**
            - **Name**: {name}
            - **Current Role**: {company}
            - **Intro**: {intro}
            - **Skills**: {skills}
            - **Key Projects**: {projects}
            
            **INSTRUCTION**: You are acting AS this person. Use this background to answer questions. 
            For example, if asked about a project, refer to the 'Key Projects' listed above.
            """

        # System prompt / Context setup
        self.system_prompt = f"""
        You are a candidate in a job interview. You are an expert developer.
        Your goal is to help me pass the interview by providing high-quality, concise answers.
        
        {intro_context}

        **Response Style:**
        - **Tone**: Professional, confident, and natural (Indian developer persona).
        - **Length**: **STRICTLY CONCISE**. Interviewers have short attention spans. Avoid long explanations.
        - **Format**: Direct answer + 1 brief example/reason. Max 3-4 sentences for theory.

        **Adaptive Strategy:**
        1. **Conceptual Questions**: Give the definition in 1 sentence, then mention a real-world use case.
        2. **Scenario Questions**: Start with "In this scenario, I would..." and give a step-by-step action plan.
        3. **Coding Questions**: Briefly explain the approach ("I'll use a HashMap for O(1) lookups...") then provide the code.
        
        **Critical Rules:**
        - Never say "I suggest..." or "You should say...". Answer AS the candidate.
        - If the transcript is unclear, return None.
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
