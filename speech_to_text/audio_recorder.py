import sounddevice as sd
import soundfile as sf
import numpy as np
from src.config import RECORD_DURATION_SECONDS, SAMPLE_RATE

def record_audio(filename: str) -> bool:
    """
    Records audio from the microphone for a specified duration.
    Args:
        filename (str): The path to save the recorded audio file.
    Returns:
        bool: True if recording was successful, False otherwise.
    """
    print(f"Recording customer feedback for {RECORD_DURATION_SECONDS} seconds...")
    try:
        # Record audio
        audio_data = sd.rec(int(RECORD_DURATION_SECONDS * SAMPLE_RATE), 
                            samplerate=SAMPLE_RATE, 
                            channels=1, 
                            dtype='int16')
        sd.wait()
        sf.write(filename, audio_data, SAMPLE_RATE)
        print(f"Recording saved to {filename}")
        return True
    except Exception as e:
        print(f"Error during recording: {e}")
        print("Please ensure your microphone is connected and working.")
        return False
