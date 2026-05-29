import sys 
from splitter import VideoSplitter

def split_videos_to_audios(input_path: str, parts_to_split: int) -> None:
    print(f"Splitting '{input_path} into {parts_to_split} parts...")
    video_splitter: VideoSplitter = VideoSplitter(input_path, parts_to_split)
    
    print(f"Video duration: {video_splitter.duration_ms / 1000:.1f}s")
    
    parts:list[str] = video_splitter.split()
    print(f"\nCreated {len(parts)} parts:")
    for path in parts:
        print(f"  {path}")

if __name__ == "__main__":
    if (len(sys.argv) < 3):
        print("Usage: python main.py <input.mp4> <parts_to_split>")

    input_path: str = sys.argv[1]
    parts_to_split: int = int(sys.argv[2])
    split_videos_to_audios(input_path, parts_to_split)


