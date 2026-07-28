import yt_dlp
import os
import sys
import shutil
from pathlib import Path


def find_js_runtime():
    """Detect an installed JS runtime yt-dlp can use for signature/n-challenge solving.
    Returns a (name, ydl_js_runtimes_dict) tuple, or (None, {}) if nothing is found.
    """
    for name in ("deno", "node", "bun"):
        if shutil.which(name):
            return name, {name: {}}
    return None, {}


def list_formats(url, use_cookies=False, browser_name="chrome", cookie_file=None, js_runtimes=None):
    """List available formats for a URL to help debug download issues."""
    try:
        cookie_opts = {}
        if cookie_file and Path(cookie_file).exists():
            cookie_opts = {"cookiefile": cookie_file}
        elif use_cookies:
            cookie_opts = {"cookiesfrombrowser": (browser_name,)}

        ydl_opts = {
            "quiet": False,
            "no_warnings": False,
            "extract_flat": False,
            "listformats": True,
            **cookie_opts,
        }
        if js_runtimes:
            ydl_opts["js_runtimes"] = js_runtimes

        print(f"\n🔍 Available formats for: {url}\n")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(url, download=False)
        return True
    except Exception as e:
        print(f"❌ Error listing formats: {str(e)}")
        return False


def download_media(url, download_type="video", use_cookies=False, browser_name="chrome",
                    cookie_file=None, js_runtimes=None):
    """Download media from YouTube or other supported platforms."""

    downloads_dir = Path("downloads")
    downloads_dir.mkdir(exist_ok=True)

    if not url.strip():
        print("❌ Error: URL cannot be empty.")
        return False

    try:
        cookie_opts = {}
        if cookie_file:
            print(f"🍪 Using cookies from file: {cookie_file}")
            if Path(cookie_file).exists():
                cookie_opts = {"cookiefile": cookie_file}
            else:
                print(f"⚠️  Cookie file not found: {cookie_file}")
                print("Continuing without cookies...")
        elif use_cookies:
            print(f"🍪 Using cookies from {browser_name} browser...")
            cookie_opts = {"cookiesfrombrowser": (browser_name,)}

        using_cookies_now = bool(cookie_opts)

        # "ios" doesn't support cookies at all, and gets silently skipped by yt-dlp
        # when cookies are supplied. "mediaconnect" isn't a real player client.
        #
        # "web" and "tv" formats now require a PO Token for the actual media
        # download (GVS) — without one you'll get metadata/format-list success
        # followed by "HTTP Error 403: Forbidden" on every video, OR a silent
        # fallback to low-quality legacy format 18 (360p).
        #
        # When cookies are in play (e.g. for members-only content), "web" is
        # put first because YouTube's membership/age-gate checks are tied to
        # the "web" client's handling of your session cookie. "tv_simply" is
        # kept as a fallback since it still works for public videos without a
        # PO Token in most cases.
        #
        # For a more robust long-term fix (full-quality formats via "web"/"tv"
        # without hitting the PO Token wall), install a PO Token provider:
        #   pip install bgutil-ytdlp-pot-provider
        # yt-dlp will pick it up automatically — after that you can rely on
        # "web" alone for both cookie and no-cookie cases if you want.
        if using_cookies_now:
            clients = ["web", "tv_simply"]
        else:
            clients = ["android", "web", "tv_simply"]

        common_opts = {
            "outtmpl": str(downloads_dir / "%(title)s.%(ext)s"),
            "extractor_args": {
                "youtube": {
                    "player_client": clients,
                }
            },
            "retries": 3,
            "fragment_retries": 3,
            "quiet": False,
            "no_warnings": False,
            "ignoreerrors": True,
            **cookie_opts,
        }

        # Required since yt-dlp 2025.11.12 for reliable format availability
        # (YouTube's "n challenge" signature decryption). Without this, you get
        # "n challenge solving failed" / "Only images are available for download".
        if js_runtimes:
            common_opts["js_runtimes"] = js_runtimes
        else:
            print("⚠️  No JS runtime (deno/node/bun) found on PATH.")
            print("   YouTube downloads will be unreliable without one — see the note printed at startup.\n")

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
        else:
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
        print("\n💡 Tip: Some videos may have been skipped due to:")
        print("   - Membership restrictions (members-only content) — requires cookies")
        print("     from a browser logged into an account that actually holds that")
        print("     channel's membership tier.")
        print("   - Regional restrictions")
        print("   - Age restrictions without authentication")
        print("   - Video availability issues")
        return True

    except Exception as e:
        error_msg = str(e)
        print(f"\n❌ Error during download: {error_msg}")

        if "sign in" in error_msg.lower() or "login" in error_msg.lower():
            print("\n🔐 This video requires authentication!")
            print("Solutions:")
            print("  1. Run the app with cookies enabled")
            print("  2. Try a different video URL")
            print("\nTo use cookies from your browser, restart and choose 'yes' when asked.")

        elif "members" in error_msg.lower() or "join this channel" in error_msg.lower():
            print("\n👥 This video is members-only content.")
            print("Solutions:")
            print("  1. Make sure you're actually a member of the required tier for this channel")
            print("  2. Restart and enable cookies, using the browser profile logged into")
            print("     the member account")
            print("  3. Otherwise this video cannot be downloaded — skip it")

        elif "not available" in error_msg.lower() or "only images" in error_msg.lower():
            print("\n🚫 This video has strong protection and formats are not accessible.")
            print("Solutions:")
            print("  1. Install a JS runtime: e.g. 'brew install deno' / 'sudo apt install nodejs' / winget install DenoLand.Deno")
            print("  2. Update yt-dlp: pip install -U \"yt-dlp[default]\"")
            print("  3. Try without cookies (restart and choose 'n')")
            print("  4. Try a different video URL")

            list_formats_choice = input("\n🔍 Would you like to see available formats? (y/n): ").lower().strip()
            if list_formats_choice in ['y', 'yes']:
                list_formats(url, use_cookies, browser_name, cookie_file, js_runtimes)

        else:
            print("Please check:")
            print("  - The URL is correct and accessible")
            print("  - You have a stable internet connection")
            print("  - FFmpeg is properly installed (required for audio/video processing)")

        return False


def main():
    """Main function to handle user interaction."""
    print("=" * 60)
    print("🎥 big_DOWNLOAD")
    print("=" * 60)
    print("Supports: YouTube, Vimeo, and many other platforms")
    print("Download options: audio (MP3) or video (MP4)")
    print("=" * 60 + "\n")

    js_runtime_name, js_runtimes = find_js_runtime()
    if js_runtime_name:
        print(f"✅ Detected JS runtime: {js_runtime_name} (used for YouTube signature solving)\n")
    else:
        print("⚠️  No JS runtime detected (deno / node / bun).")
        print("   YouTube now requires one for reliable downloads — without it you'll likely")
        print("   see 'n challenge solving failed' / 'Only images are available for download'.")
        print("   Install Deno (recommended): https://docs.deno.com/runtime/getting_started/installation/")
        print("   or Node.js 20+: https://nodejs.org")
        print("   Also make sure yt-dlp itself is current: pip install -U \"yt-dlp[default]\"\n")

    cookie_file = None
    use_cookies = False
    browser_name = "chrome"

    cookies_path = Path("cookies.txt")
    if cookies_path.exists():
        print("🍪 Found cookies.txt file in project directory!")
        use_cookies_file = input("Use cookies from cookies.txt? (y/n, default: y): ").lower().strip()
        if use_cookies_file in ['', 'y', 'yes']:
            cookie_file = str(cookies_path)
            print(f"✅ Will use cookies from cookies.txt\n")
        else:
            print("Proceeding without cookies.txt...\n")

    if not cookie_file:
        print("🍪 Some videos require authentication (age-restricted, members-only, etc.)")
        use_cookies_input = input("Use cookies from browser for authentication? (y/n, default: n): ").lower().strip()
        use_cookies = use_cookies_input in ['y', 'yes']

        if use_cookies:
            print("\nAvailable browsers: chrome, firefox, safari, edge, opera, brave, chromium")
            browser_input = input("Which browser to use? (default: chrome): ").lower().strip()
            if browser_input:
                browser_name = browser_input
            print(f"✅ Will use cookies from {browser_name}\n")
            print("⚠️  Make sure this browser is logged into the account that holds any")
            print("   channel memberships you need for members-only videos.\n")

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

            success = download_media(link, mode, use_cookies, browser_name, cookie_file, js_runtimes)

            if success:
                another = input("\n🔄 Download another file? (y/n): ").lower().strip()
                if another not in ['y', 'yes']:
                    print("👋 Thanks for using big_DOWNLOAD!")
                    break
                print()

        except KeyboardInterrupt:
            print("\n\n⚠️  Download cancelled by user.")
            print("👋 Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Unexpected error: {str(e)}")
            print("Please try again.\n")


if __name__ == "__main__":
    main()