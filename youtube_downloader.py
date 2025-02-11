from yt_dlp import YoutubeDL
from pathlib import Path
import sys

def download_video(url, output_path=None):
    """
    Download a YouTube video in 1080p quality when available.
    
    Args:
        url (str): YouTube video URL
        output_path (str, optional): Directory to save the video
    """
    try:
        # Create output directory if specified
        if output_path:
            output_path = Path(output_path)
            output_path.mkdir(parents=True, exist_ok=True)
            output_template = str(output_path / '%(title)s.%(ext)s')
        else:
            output_template = '%(title)s.%(ext)s'

        # Configure yt-dlp options for 1080p
        ydl_opts = {
            'format': 'bestvideo[height=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height=1080]+bestaudio/best[height=1080]/best',
            'outtmpl': output_template,
            'progress_hooks': [show_progress],
            'quiet': True,
            'no_warnings': True,
            'merge_output_format': 'mp4'
        }

        # Download the video
        print(f"Fetching video information...")
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            print(f"\nDownloading: {info['title']}")
            print(f"Channel: {info.get('channel', 'Unknown')}")
            
            # Get available formats
            formats = info.get('formats', [])
            available_heights = set(f.get('height', 0) for f in formats if f.get('height'))
            if 1080 in available_heights:
                print("1080p quality available - downloading at 1080p")
            else:
                print(f"1080p not available. Available qualities: {sorted(available_heights)}px")
            
            ydl.download([url])
            
        print(f"\nDownload completed successfully!")
        print(f"Saved to: {output_path if output_path else Path.cwd()}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Check your internet connection")
        print("2. Verify the video URL is correct")
        print("3. Make sure you have write permissions in the output directory")
        print("4. Update yt-dlp using: pip install -U yt-dlp")
        print("5. If you see 'Requested format is not available', the video might not be available in 1080p")

def show_progress(d):
    """Show download progress."""
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes')
        downloaded_bytes = d.get('downloaded_bytes', 0)
        
        if total_bytes:
            percentage = (downloaded_bytes / total_bytes) * 100
            downloaded_mb = downloaded_bytes / (1024 * 1024)
            total_mb = total_bytes / (1024 * 1024)
            sys.stdout.write(f"\rProgress: {percentage:.1f}% ({downloaded_mb:.1f}MB / {total_mb:.1f}MB)")
            sys.stdout.flush()

# Example usage
if __name__ == "__main__":
    video_url = input("Enter YouTube video URL: ")
    output_dir = input("Enter output directory (press Enter for current directory): ").strip()
    
    download_video(video_url, output_dir)
    