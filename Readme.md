# AI Customer Feedback Agent

This project implements an AI-powered customer feedback agent that can process customer input (either via audio recording or direct text query), analyze it using a Llama 3 model, and respond with synthesized speech. It also includes a tool for searching mobile phone data.

## Features

- **Audio Recording & Transcription**: Records customer feedback using the microphone and transcribes it into text using the Google Web Speech API.
- **Text Query Input**: Allows direct text input for analysis.
- **Llama 3 Analysis**: Utilizes Llama 3 for sentiment analysis, key feedback extraction, and intelligent responses.
- **Tool Calling**: Integrates a `search_mobiles` tool, enabling the LLM to search for mobile phone products based on customer queries.
- **Text-to-Speech (TTS)**: Converts the AI's analysis and responses into audible speech.
- **Continuous Operation**: The agent can run continuously, processing multiple feedback inputs until explicitly stopped.

## Setup

### Prerequisites

- Python 3.8+
- A microphone (for `record` mode)
- An API Key from Together AI.

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/business_ai_agent.git
    cd business_ai_agent
    ```

2.  **Install dependencies:**
    It's recommended to use a virtual environment.

    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate

    pip install -r requirements.txt
    ```

3.  **Configure API Key:**
    Create a `.env` file in the root directory of your project (if it doesn't exist) and add your Together AI API key:
    ```
    TOGETHER_API_KEY="YOUR_TOGETHER_API_KEY_HERE"
    ```
    Replace `YOUR_TOGETHER_API_KEY_HERE` with your actual Together AI API key.

## Usage

The agent can be run in two modes: `record` (for audio input) or `query` (for text input). Both modes now support continuous operation until you decide to stop.

### Running the Agent

```bash
python -m src.main --mode [record|query]
```

Replace `[record|query]` with your desired mode.

#### 1. Record Mode (Audio Input)

In this mode, the agent will automatically start recording audio from your microphone, transcribe it, analyze it, and speak the response. It will then automatically prepare for the next recording.

- **To run in record mode:**
  ```bash
  python -m src.main --mode record
  ```
- **To stop the agent:** Press `Ctrl+C` (or `Cmd+C` on macOS) at any time.

#### 2. Query Mode (Text Input)

In this mode, the agent will prompt you to enter text queries. It will then analyze your text and speak the response. After responding, it will prompt you for another query.

- **To run in query mode:**
  ```bash
  python -m src.main --mode query
  ```
- **To stop the agent:** Type `exit` or `quit` when prompted for input and press Enter.

### Example Interaction

**Record Mode:**

1.  Run `python -m src.main --mode record`
2.  Speak your feedback (e.g., "The customer service was excellent, but I wish you had more phones under 500 dollars.").
3.  The agent will transcribe your speech, analyze it, and speak its response.
4.  It will then wait for your next recording. Press `Ctrl+C` to end.

**Query Mode:**

1.  Run `python -m src.main --mode query`
2.  You will see `Please enter your query: `
3.  Type your feedback (e.g., "I need a new phone, can you list some options around 800 dollars with at least 256GB storage?").
4.  The agent will analyze your text and speak its response (potentially using the `search_mobiles` tool).
5.  You will be prompted `Please enter your query: ` again.
6.  Type `exit` or `quit` to end the session.

## Project Structure

- `src/main.py`: The main entry point of the application.
- `src/config.py`: Configuration settings (API keys, model names, etc.).
- `speech_to_text/`: Contains modules for audio recording and transcription.
  - `audio_recorder.py`: Handles microphone input and saving audio files.
  - `stt_transcriber.py`: Transcribes audio to text using `speech_recognition`.
- `prompts/`: Contains modules related to LLM interaction.
  - `llm_analyzer.py`: Manages communication with Llama 3, including tool calling.
- `text_to_speech/`: Contains modules for text-to-speech conversion.
  - `tts_speaker.py`: Converts text to speech and plays it.
- `search/`: Contains data search functionalities for LLM tools.
  - `data_searcher.py`: Implements the `search_mobiles` function.
- `dataset/mobiles.csv`: Sample mobile phone data for the search tool.

## Configuration

You can customize the agent's behavior by modifying the `config.py` file:

- `RECORD_DURATION_SECONDS`: Adjust how long the agent records audio.
- `SAMPLE_RATE`: Audio sample rate.
- `WHISPER_MODEL`: Change the Whisper model size (`'tiny'`, `'base'`, `'small'`, `'medium'`, `'large'`). Larger models are more accurate but require more resources and download time.
- `LLAMA_MODEL`: Switch between Llama 3 models available on Together AI (e.g., `"meta-llama/Llama-3-70b-chat-hf"` for a larger model).
- `LLM_MAX_TOKENS`, `LLM_TEMPERATURE`: Fine-tune the LLM's response generation.

## Troubleshooting

- **Microphone Issues:** If recording fails, ensure your microphone is properly connected and recognized by your operating system. Check microphone permissions for your terminal/IDE if applicable.
- **Together AI API Key Error:** Double-check that your `TOGETHER_API_KEY` is correctly set as an environment variable or in your `.env` file, and that it's active and valid on Together AI.
- **No TTS Output:** Ensure your operating system has a functional Text-to-Speech engine installed (e.g., SAPI on Windows).
- **Whisper Model Download:** The first run of Whisper might take time as it downloads the model weights. Subsequent runs will be faster.

---
