# AI Meeting Assistant

A real-time AI assistant that listens to your meetings/interviews, transcribes the audio, and provides context-aware answers instantly.

## Features

*   **Real-Time Transcription**: Uses `faster-whisper` (Small model) for high-accuracy, low-latency speech-to-text.
*   **Smart Listening (VAD)**: Automatically detects when you stop speaking to process the query.
*   **Adaptive AI Persona**:
    *   **Short Questions** -> Crisp, direct answers.
    *   **Deep Questions** -> Detailed explanations.
    *   **Coding Questions** -> Technical logic & snippets.
    *   **Scenario Questions** -> Practical, scenario-based solutions.
    *   **Humanized Tone**: Speaks like a professional developer (First-person perspective).
*   **Stealth Mode**: The overlay window is **invisible to screen sharing** (Windows only). You see it, but others don't.
*   **Overlay UI**: Transparent, top-centered window that stays on top of other apps.
*   **Auto-Clear**: Automatically clears old transcripts when a new question is asked.
*   **Global Hotkey**: Toggle the overlay with `Ctrl + \`.

## Prerequisites

*   **Python 3.10+** installed on your system.
*   **Git** installed.
*   A **Google Gemini API Key** (Free tier available).

## Installation

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/sam7776/AI-APP.git
    cd AI-APP
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: If you face issues with `soundcard` or `faster-whisper`, ensure you have the necessary C++ build tools installed.*

3.  **Configure API Key**:
    *   Create a file named `.env` in the root directory.
    *   Add your Gemini API key:
        ```env
        GEMINI_API_KEY=your_api_key_here
        ```

## Usage

1.  **Run the Application**:
    *   Double-click `run.bat` (Windows).
    *   OR run via terminal:
        ```bash
        python main.py
        ```
    *   The console window will automatically minimize to keep your screen clean.

2.  **How it Works**:
    *   The app sits in your system tray.
    *   The overlay appears at the top center of your screen.
    *   **Just speak!** The app listens to your system audio (loopback).
    *   When you pause, it transcribes and fetches an answer from the AI.

3.  **Controls**:
    *   **Toggle Overlay**: Press `Ctrl + \` to show/hide.
    *   **Exit**: Right-click the system tray icon and select "Exit".

## Troubleshooting

*   **"404 models/gemini... not found"**: Ensure your API key is valid and has access to the `gemini-flash-latest` model.
*   **No Audio Detected**: Check your system volume. The app listens to the *default output device* (what you hear).
*   **Overlay not hiding on screen share**: Ensure you are sharing the *screen*, not just a specific window (though it works best with full screen share).

## License

[MIT](LICENSE)