import yt_dlp
import os
import sys
from pathlib import Path

def list_formats(url, use_cookies=False, browser_name="chrome"):
    """List available formats for a URL to help debug download issues."""
    try:
        cookie_opts = {}
        if use_cookies:
            cookie_opts = {
                "cookiesfrombrowser": (browser_name,),
            }

        ydl_opts = {
            "quiet": False,
            "no_warnings": False,
            "extract_flat": False,
            "listformats": True,
            **cookie_opts,
        }

        print(f"\n🔍 Available formats for: {url}\n")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=False)
        return True
    except Exception as e:
        print(f"❌ Error listing formats: {str(e)}")
        return False

def download_media(url, download_type="video", use_cookies=False, browser_name="chrome"):
    """Download media from YouTube or other supported platforms."""

    # Create downloads directory if it doesn't exist
    downloads_dir = Path("downloads")
    downloads_dir.mkdir(exist_ok=True)

    # Validate URL
    if not url.strip():
        print("❌ Error: URL cannot be empty.")
        return False

    try:
        # Build cookie options if requested
        cookie_opts = {}
        if use_cookies:
            print(f"🍪 Using cookies from {browser_name} browser...")
            cookie_opts = {
                "cookiesfrombrowser": (browser_name,),
            }

        # Use simpler client configuration - just one at a time
        common_opts = {
            "outtmpl": str(downloads_dir / "%(title)s.%(ext)s"),
            "extractor_args": {
                "youtube": {
                    "player_client": ["web"] if use_cookies else ["android"],
                }
            },
            "retries": 3,
            "fragment_retries": 3,
            "quiet": False,
            "no_warnings": False,
            **cookie_opts,
        }

        if download_type == "audio":
            ydl_opts = {
                **common_opts,
                "format": "bestaudio/best",
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
            }
        else:  # video
            ydl_opts = {
                **common_opts,
                "format": "bestvideo+bestaudio/best",
                "merge_output_format": "mp4",
            }

        print(f"\n🎬 Starting {download_type} download...")
        print(f"📺 URL: {url}")
        print(f"📁 Save location: {downloads_dir.absolute()}\n")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        print(f"\n✅ Download complete! Files saved in: {downloads_dir.absolute()}")
        return True

    except Exception as e:
        error_msg = str(e)
        print(f"\n❌ Error during download: {error_msg}")

        # Check if it's an authentication error
        if "sign in" in error_msg.lower() or "login" in error_msg.lower():
            print("\n🔐 This video requires authentication!")
            print("Solutions:")
            print("  1. Run the app with cookies enabled")
            print("  2. Try a different video URL")
            print("\nTo use cookies from your browser, restart and choose 'yes' when asked.")

        # Check if formats are not available
        elif "not available" in error_msg.lower() or "only images" in error_msg.lower():
            print("\n🚫 This video has strong protection and formats are not accessible.")
            print("Solutions:")
            print("  1. Try without cookies (restart and choose 'n')")
            print("  2. Try a different video URL")
            print("  3. Some videos cannot be downloaded due to YouTube's restrictions")

            # Offer to list formats
            list_formats_choice = input("\n🔍 Would you like to see available formats? (y/n): ").lower().strip()
            if list_formats_choice in ['y', 'yes']:
                list_formats(url, use_cookies, browser_name)

        else:
            print("Please check:")
            print("  - The URL is correct and accessible")
            print("  - You have a stable internet connection")
            print("  - FFmpeg is properly installed (required for audio/video processing)")

        return False

def main():
    """Main function to handle user interaction."""
    print("=" * 60)
    print("🎥 YouTube Media Downloader")
    print("=" * 60)
    print("Supports: YouTube, Vimeo, and many other platforms")
    print("Download options: audio (MP3) or video (MP4)")
    print("=" * 60 + "\n")

    # Ask about cookies once at startup
    print("🍪 Some videos require authentication (age-restricted, etc.)")
    use_cookies_input = input("Use cookies from browser for authentication? (y/n, default: n): ").lower().strip()
    use_cookies = use_cookies_input in ['y', 'yes']

    browser_name = "chrome"
    if use_cookies:
        print("\nAvailable browsers: chrome, firefox, safari, edge, opera, brave, chromium")
        browser_input = input("Which browser to use? (default: chrome): ").lower().strip()
        if browser_input:
            browser_name = browser_input
        print(f"✅ Will use cookies from {browser_name}\n")

    while True:
        try:
            link = input("🔗 YouTube URL (or 'q' to quit): ").strip()

            if link.lower() in ['q', 'quit', 'exit']:
                print("👋 Goodbye!")
                break

            if not link:
                print("❌ Please enter a valid URL.\n")
                continue

            mode = input("📥 Download type ('audio' or 'video', default: video): ").lower().strip()

            if not mode:
                mode = "video"

            if mode not in ["audio", "video"]:
                print("❌ Invalid mode. Please choose 'audio' or 'video'.\n")
                continue

            success = download_media(link, mode, use_cookies, browser_name)

            if success:
                another = input("\n🔄 Download another file? (y/n): ").lower().strip()
                if another not in ['y', 'yes']:
                    print("👋 Thanks for using YouTube Media Downloader!")
                    break
                print()  # Add blank line for next iteration

        except KeyboardInterrupt:
            print("\n\n⚠️  Download cancelled by user.")
            print("👋 Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}")
            print("Please try again.\n")

if __name__ == "__main__":
    main()