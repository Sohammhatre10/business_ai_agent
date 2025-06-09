import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv() # This line should be at the very top of config.py

# --- Audio Recording Configuration ---
RECORD_DURATION_SECONDS = 10  # How long to record customer's voice
SAMPLE_RATE = 16000           # Standard sample rate for speech
AUDIO_FILE_NAME = "customer_recording.wav" # Temporary file to store recording

# --- Speech-to-Text Configuration ---
WHISPER_MODEL = "base"        # 'tiny', 'base', 'small', 'medium', 'large'. 'base' is a good balance.

# --- Together AI (Llama 3) Configuration ---
# Get your Together AI API key from environment variable or replace with your actual key
# It's recommended to use environment variables for API keys for security
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY") 
if not TOGETHER_API_KEY:
    print("WARNING: TOGETHER_API_KEY not found in environment variables.")
    print("Please set it (e.g., export TOGETHER_API_KEY='YOUR_KEY') or replace the placeholder in the script.")
    # Fallback for demonstration, but strongy recommend using environment variable
    TOGETHER_API_KEY = "YOUR_TOGETHER_API_KEY_HERE" # <<< IMPORTANT: Replace with your actual key if not using env var

TOGETHER_API_URL = "https://api.together.ai/v1/chat/completions"
# Use "meta-llama/Llama-3-8b-chat-hf" or "meta-llama/Llama-3-70b-chat-hf"
LLAMA_MODEL = "meta-llama/Llama-3-8b-chat-hf" 
LLM_MAX_TOKENS = 500
LLM_TEMPERATURE = 0.7
LLM_MAX_TOOL_CALL_TURNS = 3 # Max turns for tool calls to prevent infinite loops

# --- Data Search Configuration ---
DATA_DIR = "data"
MOBILES_CSV_FILE = "mobiles.csv"
MOBILES_CSV_PATH = os.path.join(DATA_DIR, MOBILES_CSV_FILE)
