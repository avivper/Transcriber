import sys 
import os
from splitter import VideoSplitter
from transcriber import Transcriber
from config import Config

def split_videos_to_audios(input_path: str, parts_to_split: int) -> list[str]:
    print(f"Splitting '{input_path} into {parts_to_split} parts...")
    video_splitter: VideoSplitter = VideoSplitter(input_path, parts_to_split)
    
    print(f"Video duration: {video_splitter.duration_ms / 1000:.1f}s")
    
    parts:list[str] = video_splitter.split()
    print(f"\nCreated {len(parts)} parts:")
    for path in parts:
        print(f"  {path}")
    
    return parts

def transcribe_audios(audio_paths: list[str]) -> dict[str,str]:
    api_key: str = load_key()
    #TODO add a catch error if api key is null
    transcriber: Transcriber = Transcriber(api_key=api_key)
    print(f"\nTranscribing {len(audio_paths)} parts...")
    results: dict[str, str] = transcriber.transcribe_many(audio_paths)
    for path, transcript in results.items():
        print(f"\n--- {os.path.basename(path)} ---\n")
        print(transcript)
    return results

def load_key() -> str:
    try:
        config: str = Config.load()
        print("API Key loaded successfully!")
        return config.api_key
    except ValueError as e:
        print(f"Error: {e}")

def run(input_path: str, parts_to_split: int) -> None:
    audio_paths: list[str] = split_videos_to_audios(
        input_path, parts_to_split
        )
    if audio_paths is None: 
        print("Error")
    transcribe_audios(audio_paths)

if __name__ == "__main__":
    if (len(sys.argv) < 3):
        print("Usage: python main.py <input.mp4> <parts_to_split>")

    input_path: str = sys.argv[1]
    parts_to_split: int = int(sys.argv[2])
    run(input_path, parts_to_split)



