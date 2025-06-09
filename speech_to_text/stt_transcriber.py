import speech_recognition as sr
# from src.config import WHISPER_MODEL # No longer needed for SpeechRecognition

def transcribe_audio(audio_path: str) -> str | None:
    """
    Transcribes an audio file to text using the SpeechRecognition library.
    Args:
        audio_path (str): The path to the audio file.
    Returns:
        str | None: The transcribed text if successful, None otherwise.
    """
    recognizer = sr.Recognizer()
    
    try:
        with sr.AudioFile(audio_path) as source:
            print("Reading audio file...")
            audio_data = recognizer.record(source) # read the entire audio file

        print("Transcribing audio using Google Web Speech API...")
        # You can specify other recognizers like recognizer.recognize_sphinx for offline
        transcription = recognizer.recognize_google(audio_data) 
        
        print("Transcription complete.")
        print(f"Transcription: {transcription}")
        return transcription
    except sr.UnknownValueError:
        print("Speech Recognition could not understand audio")
        return None
    except sr.RequestError as e:
        print(f"Could not request results from Google Web Speech API service; {e}")
        return None
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None
