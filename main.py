import sys 
import os
from splitter import VideoSplitter
from transcriber import Transcriber
from config import Config
from translator import Translator

def load_key() -> str:
    try:
        config: str = Config.load()
        print("API Key loaded successfully!")
        return config.api_key
    except ValueError as e:
        print(f"Error: {e}")

def split_videos_to_audios(input_path: str, parts_to_split: int) -> list[str]:
    print(f"Splitting '{input_path} into {parts_to_split} parts...")
    video_splitter: VideoSplitter = VideoSplitter(input_path, parts_to_split)
    
    print(f"Video duration: {video_splitter.duration_ms / 1000:.1f}s")
    
    parts:list[str] = video_splitter.split()
    print(f"\nCreated {len(parts)} parts:")
    for path in parts:
        print(f"  {path}")
    return parts

def transcribe_audios(audio_paths: list[str], api_key: str) -> dict[str,str]:
    transcriber: Transcriber = Transcriber(api_key)
    print(f"\nTranscribing {len(audio_paths)} parts...")
    results: dict[str, str] = transcriber.transcribe_files(audio_paths)
    return results

def print_generated_data_transcribed_results(transcribed_data: dict[str, str]) -> None:
    for path, transcript in transcribed_data.items():
        print(f"\n--- {os.path.basename(path)} ---\n")
        print(transcript)

def translate_data(transcribed_audio: dict[str, str], api_key: str) -> list[str]:
    translator: Translator = Translator(api_key)
    print("Translating parts...")
    return translator.translate_from_dict(transcribed_audio)

def print_translated_results(translated_results: list[str]) -> None: 
    for data in translated_results:
        print(data)

def print_results(
        transcribed_audio: dict[str, str] = None, 
        translated_results: list[str] = None
        ) -> None: 
    if transcribed_audio != None: 
        print_generated_data_transcribed_results(transcribed_audio)
    if translated_results != None:
        print_translated_results(translated_results)

def run(input_path: str, parts_to_split: int) -> None:
    api_key: str = load_key()
    if (api_key is None):
        print("Failed process the API Key")
        return
    audio_file_paths: list[str] = split_videos_to_audios(input_path, parts_to_split)
    transcribed_audio: dict[str, str] = transcribe_audios(audio_file_paths, api_key)
    translated_data: list[str] = translate_data(transcribed_audio, api_key)
    print_results(transcribed_audio, translated_data)

if __name__ == "__main__":
    if (len(sys.argv) < 3):
        print("Usage: python main.py <input.mp4> <parts_to_split>")

    input_path: str = sys.argv[1]
    parts_to_split: int = int(sys.argv[2])
    run(input_path, parts_to_split)



