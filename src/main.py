import os
import argparse
from src.config import AUDIO_FILE_NAME, DATA_DIR
from speech_to_text.audio_recorder import record_audio
from speech_to_text.stt_transcriber import transcribe_audio
from prompts.llm_analyzer import analyze_with_llama3
from text_to_speech.tts_speaker import text_to_speech_and_play

def run_automation(mode: str, voice_option: str):
    """
    Main function to run the AI automation workflow.
    Args:
        mode (str): Determines the input method. 'record' for audio recording, 'query' for text input.
        voice_option (str): Option for TTS voice. 'male', 'female', 'list', or 'default'.
    """
    print("--- Starting AI Customer Feedback Agent ---")

    # Handle voice listing before starting core automation
    if voice_option == 'list':
        print("Listing available voices and exiting.")
        # Pass an empty string for text as we only want to list voices
        text_to_speech_and_play("", voice_option=voice_option)
        return # Exit after listing

    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"Ensured data directory '{DATA_DIR}' exists.")

    if mode == "record":
        print("\n--- Record Mode: Recording will start automatically. Press Ctrl+C to stop at any time. ---")
        while True:
            if not record_audio(AUDIO_FILE_NAME):
                print("Audio recording failed. Please ensure your microphone is connected and working. Trying again...")
                continue

            transcribed_text = transcribe_audio(AUDIO_FILE_NAME)

            if os.path.exists(AUDIO_FILE_NAME):
                os.remove(AUDIO_FILE_NAME)
                print(f"Cleaned up {AUDIO_FILE_NAME}")

            if not transcribed_text:
                print("Transcription failed or no speech detected. Please try recording again.")
                continue
            print(f"Transcribed Text: {transcribed_text}")

            llama_analysis = analyze_with_llama3(transcribed_text)
            if llama_analysis.startswith("Error:") or llama_analysis.startswith("No analysis"):
                print(f"Llama 3 analysis failed: {llama_analysis}. Continuing with next recording.")
                continue

            text_to_speech_and_play(llama_analysis, voice_option)

    elif mode == "query":
        print("\n--- Query Mode: Enter your feedback. Type 'exit' or 'quit' to end the session. ---")
        while True:
            transcribed_text = input("Please enter your query: ")
            if not transcribed_text:
                print("No query entered. Please try again.")
                continue
            if transcribed_text.lower() in ["exit", "quit"]:
                print("Exiting query mode. Goodbye!")
                break

            llama_analysis = analyze_with_llama3(transcribed_text)
            if llama_analysis.startswith("Error:") or llama_analysis.startswith("No analysis"):
                print(f"Llama 3 analysis failed: {llama_analysis}. Continuing with next query.")
                continue

            text_to_speech_and_play(llama_analysis, voice_option)
    else:
        print(f"Invalid mode: {mode}. Please use 'record' or 'query'. Exiting.")
        return

    print("--- AI Customer Feedback Agent Finished ---")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the AI Customer Feedback Agent.")
    parser.add_argument(
        "--mode",
        type=str,
        choices=["record", "query"],
        default="record",
        help="Specify the input mode: 'record' for audio recording, 'query' for direct text input."
    )
    parser.add_argument(
        "--voice-option",
        type=str,
        choices=["male", "female", "list", "default"],
        default="default",
        help="Specify TTS voice: 'male', 'female', 'list' (to show available options and exit), or 'default'."
    )
    args = parser.parse_args()

    run_automation(args.mode, args.voice_option)
