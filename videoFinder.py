"""
Simple script to get all video IDs from your YouTube channel
Run this first to get your video IDs, then use them in the main chatbot
"""

import sys

print("=" * 60)
print("YouTube Video ID Fetcher")
print("=" * 60)

# Check which methods are available
try:
    import yt_dlp
    HAS_YTDLP = True
    print("✓ yt-dlp is installed")
except ImportError:
    HAS_YTDLP = False
    print("✗ yt-dlp NOT installed")

try:
    from googleapiclient.discovery import build
    HAS_API = True
    print("✓ Google API client is installed")
except ImportError:
    HAS_API = False
    print("✗ Google API client NOT installed")

print()

def get_videos_ytdlp(channel_url):
    """Get videos using yt-dlp (RECOMMENDED - no API key needed)"""
    if not HAS_YTDLP:
        print("Please install yt-dlp first:")
        print("  pip install yt-dlp")
        return []
    
    try:
        ydl_opts = {
            'quiet': False,
            'extract_flat': True,
            'force_generic_extractor': False,
        }
        
        print(f"\nFetching videos from: {channel_url}")
        print("This may take 30-60 seconds...\n")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(channel_url, download=False)
            
            if 'entries' not in result:
                print("No videos found. Make sure the URL is correct.")
                return []
            
            videos = []
            for entry in result['entries']:
                if entry and 'id' in entry:
                    duration = entry.get('duration', 0)
                    title = entry.get('title', 'Unknown')
                    
                    # Exclude Shorts (under 60 seconds)
                    if duration > 60:  # More than 1 minute = long-form
                        videos.append({
                            'id': entry['id'],
                            'title': title,
                            'duration_mins': duration // 60 if duration else 0
                        })
            
            return videos
            
    except Exception as e:
        print(f"Error: {e}")
        return []


def get_videos_api(channel_id, api_key):
    """Get videos using YouTube API"""
    if not HAS_API:
        print("Please install Google API client first:")
        print("  pip install google-api-python-client")
        return []
    
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        videos = []
        next_page_token = None
        
        print(f"\nFetching videos from channel: {channel_id}")
        
        while True:
            request = youtube.search().list(
                part='id,snippet',
                channelId=channel_id,
                maxResults=50,
                pageToken=next_page_token,
                type='video',
                order='date'
            )
            response = request.execute()
            
            video_ids = [item['id']['videoId'] for item in response['items']]
            
            # Get video details to check duration
            details_request = youtube.videos().list(
                part='contentDetails,snippet',
                id=','.join(video_ids)
            )
            details_response = details_request.execute()
            
            for item in details_response['items']:
                duration_str = item['contentDetails']['duration']
                
                # Parse ISO 8601 duration (PT1H30M45S)
                import re
                match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration_str)
                if match:
                    hours = int(match.group(1) or 0)
                    minutes = int(match.group(2) or 0)
                    total_mins = hours * 60 + minutes
                    
                    # Exclude Shorts (under 60 seconds)
                    if total_mins > 1 or (total_mins == 1 and int(match.group(3) or 0) > 0):
                        videos.append({
                            'id': item['id'],
                            'title': item['snippet']['title'],
                            'duration_mins': total_mins
                        })
            
            next_page_token = response.get('nextPageToken')
            if not next_page_token:
                break
        
        return videos
        
    except Exception as e:
        print(f"Error: {e}")
        return []


def main():
    print("\nChoose a method to fetch your videos:\n")
    print("1. yt-dlp (RECOMMENDED - no API key needed)")
    print("2. YouTube API (requires API key)")
    print("3. Exit")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    videos = []
    
    if choice == "1":
        if not HAS_YTDLP:
            print("\n❌ yt-dlp is not installed!")
            print("Install it with: pip install yt-dlp")
            return
        
        print("\n" + "=" * 60)
        print("Method 1: Using yt-dlp")
        print("=" * 60)
        print("\nYou can use any of these URL formats:")
        print("  • https://www.youtube.com/@YourChannelHandle")
        print("  • https://www.youtube.com/@YourChannelHandle/videos")
        print("  • https://www.youtube.com/c/YourChannelName")
        print("  • https://www.youtube.com/channel/UC...")
        
        channel_url = input("\nEnter your channel URL: ").strip()
        
        if not channel_url:
            print("No URL provided!")
            return
        
        videos = get_videos_ytdlp(channel_url)
        
    elif choice == "2":
        if not HAS_API:
            print("\n❌ Google API client is not installed!")
            print("Install it with: pip install google-api-python-client")
            return
        
        print("\n" + "=" * 60)
        print("Method 2: Using YouTube API")
        print("=" * 60)
        
        api_key = input("\nEnter your YouTube API key: ").strip()
        channel_id = input("Enter your channel ID (UC...): ").strip()
        
        if not api_key or not channel_id:
            print("API key and channel ID are required!")
            return
        
        videos = get_videos_api(channel_id, api_key)
        
    else:
        print("Exiting...")
        return
    
    # Display results
    print("\n" + "=" * 60)
    print(f"✓ Found {len(videos)} long-form videos (excluding Shorts)")
    print("=" * 60)
    
    if not videos:
        print("\n❌ No videos found!")
        print("\nTroubleshooting:")
        print("1. Make sure the URL/Channel ID is correct")
        print("2. Check if your videos are public")
        print("3. Verify videos are 10+ minutes long")
        return
    
    # Show first 5 videos
    print("\nFirst 5 videos:")
    for i, video in enumerate(videos[:5], 1):
        print(f"\n{i}. {video['title']}")
        print(f"   ID: {video['id']}")
        print(f"   Duration: {video['duration_mins']} minutes")
    
    if len(videos) > 5:
        print(f"\n... and {len(videos) - 5} more videos")
    
    # Save to file
    print("\n" + "=" * 60)
    save = input("\nSave video IDs to file? (yes/no): ").strip().lower()
    
    if save == 'yes':
        filename = "video_ids.txt"
        with open(filename, 'w') as f:
            f.write("# YouTube Video IDs\n")
            f.write("# Copy these into the VIDEO_IDS list in main.py\n\n")
            f.write("VIDEO_IDS = [\n")
            for video in videos:
                f.write(f'    "{video["id"]}",  # {video["title"][:50]}\n')
            f.write("]\n")
        
        print(f"\n✓ Saved to {filename}")
        print(f"\nNow copy the VIDEO_IDS list from {filename} into your main chatbot script!")
    
    # Also save Python code
    filename = "video_ids.py"
    with open(filename, 'w') as f:
        f.write("# Video IDs for chatbot\n\n")
        f.write("VIDEO_IDS = [\n")
        for video in videos:
            f.write(f'    "{video["id"]}",  # {video["title"][:60]}\n')
        f.write("]\n")
    
    print(f"✓ Also saved as Python list to {filename}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting...")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()