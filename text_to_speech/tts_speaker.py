import pyttsx3

def text_to_speech_and_play(text: str, voice_option: str = None):
    """
    Converts text to speech and plays it back, with options for voice selection.
    Args:
        text (str): The text to be spoken.
        voice_option (str, optional): Option for voice selection.
                                      'male' for male voice, 'female' for female voice.
                                      'list' to list available voices (no speech playback).
                                      Defaults to system default if None or not found.
    """
    print("Converting analysis to speech and playing back...")
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')

        if voice_option and voice_option.lower() == 'list':
            print("\nAvailable TTS Voices")
            for i, voice in enumerate(voices):
                print(f"  {i}: ID='{voice.id}', Name='{voice.name}', Lang='{voice.languages[0] if voice.languages else 'N/A'}'")
            print("----------------------------\n")
            return

        selected_voice_id = None
        if voice_option and voice_option.lower() in ['male', 'female']:
            target_gender = voice_option.lower()
            print(f"Attempting to find a {target_gender} voice...")
            for voice in voices:
                voice_name_lower = voice.name.lower()
                if (target_gender == 'male' and ('male' in voice_name_lower or 'david' in voice_name_lower or 'alex' in voice_name_lower)) or \
                   (target_gender == 'female' and ('female' in voice_name_lower or 'zira' in voice_name_lower or 'helen' in voice_name_lower or 'eva' in voice_name_lower)):
                    selected_voice_id = voice.id
                    break
        
        if selected_voice_id:
            engine.setProperty('voice', selected_voice_id)
            try:
                current_voice_id = engine.getProperty('voice')
                voice_name = next((v.name for v in voices if v.id == current_voice_id), "Unknown Voice")
                print(f"Set voice to: '{voice_name}' (ID: {current_voice_id})")
            except Exception:
                print(f"Set voice to ID: {selected_voice_id}")
        else:
            if voice_option and voice_option.lower() in ['male', 'female']:
                print(f"Could not find a suitable '{voice_option}' voice. Using default system voice.")
            else:
                print("Using default system voice.")

        engine.say(text)
        engine.runAndWait()
        print("Playback finished.")
    except Exception as e:
        print(f"Error during text-to-speech: {e}")
        print("Please ensure your system has a TTS engine installed (e.g., SAPI on Windows).")
