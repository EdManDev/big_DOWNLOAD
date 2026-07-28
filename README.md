# big_DOWNLOAD

A simple Python application to download videos and audio from YouTube and other supported platforms using yt-dlp.

## Features

- **Download videos** in MP4 format with best available quality
- **Download audio** in MP3 format with high-quality extraction (192 kbps)
- **Cookie authentication** support for age-restricted and member-only content
- **Smart client selection** - automatically chooses the best download method (web/android/tv)
- **JS Runtime detection** - automatically detects Deno/Node/Bun for YouTube signature decryption
- **PO Token support** - includes provider to prevent fallback to low-quality formats
- **Cookie file support** - can use `cookies.txt` from project directory
- **Automatic retry mechanism** for failed downloads (3 attempts)
- **Format debugging** - see available formats when downloads fail
- **Multi-platform support** - YouTube, Vimeo, and 1000+ other sites
- **Continuous operation** - download multiple files without restarting
- **Organized downloads** - all files saved in dedicated downloads folder
- **Progress feedback** - clear status messages and error handling

## 🚀 Quick Start (Copy & Paste)

### macOS/Linux:
```bash
cd big_DOWNLOAD
rm -rf venv
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirement.txt
python3 app.py
```

### Windows:
```cmd
cd big_DOWNLOAD
rmdir /s /q venv
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirement.txt
python app.py
```

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- FFmpeg (required for audio extraction and video merging)
- **JS Runtime** (Deno, Node.js, or Bun) - Required for YouTube's signature decryption ("n challenge")

### Installing a JS Runtime

YouTube now requires a JavaScript runtime for reliable downloads. Without one, you'll see "n challenge solving failed" or "Only images are available for download" errors.

**Recommended: Deno**
```bash
# macOS
brew install deno

# Linux
curl -fsSL https://deno.land/install.sh | sh

# Windows
winget install DenoLand.Deno
```

**Alternative: Node.js 20+**
```bash
# macOS
brew install node

# Ubuntu/Debian
sudo apt install nodejs npm

# Windows
winget install OpenJS.NodeJS.LTS
```

**Alternative: Bun**
```bash
# macOS/Linux
curl -fsSL https://bun.sh/install | bash

# Windows
powershell -c "irm bun.sh/install.ps1 | iex"
```

## Installation

### 1. Clone or Download the Project

```bash
cd /path/to/big_DOWNLOAD
sudo apt install -y python3-venv python3-full
```

### 2. Create Virtual Environment (Recommended)

#### On macOS and Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

#### On Windows:
```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirement.txt
```

This installs:
- `yt-dlp[default]` — Core downloader with all required dependencies
- `bgutil-ytdlp-pot-provider` — PO Token provider for full-quality formats (prevents fallback to low-res format 18)

### 4. Install FFmpeg

#### On macOS:
```bash
brew install ffmpeg
```

#### On Ubuntu/Debian:
```bash
sudo apt update
sudo apt install ffmpeg
```

#### On Windows:
1. Download FFmpeg from https://ffmpeg.org/download.html
2. Extract the files
3. Add the FFmpeg `bin` folder to your system PATH

## Usage

### Running the Application

Make sure your virtual environment is activated, then run:

```bash
python app.py
```

### Interactive Mode

When you run the application, you'll be prompted to:

1. **JS Runtime check** - App auto-detects Deno/Node/Bun (warns if missing)
2. **cookies.txt detection** - If found in project directory, prompts to use it
3. **Cookie authentication**: Choose whether to use browser cookies for restricted content
4. **Browser selection**: If using cookies, select your browser (chrome, firefox, safari, etc.)
5. **Enter the YouTube URL**: Paste the link to the video you want to download
6. **Choose download type**: Type either `audio` or `video`
7. **Continue or exit**: Choose to download more files or exit the app

Example session:
```
============================================================
🎥 big_DOWNLOAD
============================================================
Supports: YouTube, Vimeo, and many other platforms
Download options: audio (MP3) or video (MP4)
============================================================

✅ Detected JS runtime: deno (used for YouTube signature solving)

🔗 YouTube URL (or 'q' to quit): https://www.youtube.com/watch?v=dQw4w9WgXcQ
📥 Download type ('audio' or 'video', default: video): audio

🎬 Starting audio download...
📺 URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ
📁 Save location: /path/to/downloads

✅ Download complete! Files saved in: /path/to/downloads

🔄 Download another file? (y/n): n
👋 Thanks for using big_DOWNLOAD!
```

### Downloaded Files

All downloaded files are saved in the `downloads/` directory with the video's original title as the filename.

## Features in Detail

### Video Download
- Downloads the best available quality video (MP4 format)
- Combines video and audio streams for optimal quality
- Smart client selection for maximum compatibility
- Automatic format selection for best results

### Audio Download
- Extracts audio from videos and converts to MP3
- High-quality output (192 kbps)
- Faster download than full video
- Perfect for music, podcasts, and lectures

### Authentication Methods

#### Without Cookies (Default - Recommended)
- Uses Android client for better compatibility
- Works for most public videos
- No browser dependency
- Faster and more reliable

#### With Browser Cookies
- Access age-restricted content
- Download member-only videos (requires account with active membership)
- Support for private videos (if you have access)
- Supports: Chrome, Firefox, Safari, Edge, Opera, Brave, Chromium
- Uses "web" client first for better membership authentication

#### Using cookies.txt File
- Place `cookies.txt` in project directory
- App will detect and prompt to use it automatically
- Export cookies from browser using browser extensions

## Understanding YouTube's Protection

YouTube has different levels of protection for videos:

### 🟢 Easy to Download (Most Videos)
- Regular public videos
- Educational content
- Most music videos
- **Solution**: Works without cookies

### 🟡 Medium Protection
- Age-restricted content
- Some copyrighted material
- Region-restricted videos
- **Solution**: Try with browser cookies

### 🔴 Strong Protection (Cannot Download)
- Very recent uploads
- Premium content
- YouTube Originals
- Music with strict Content ID
- **Solution**: Try a different video or wait

### Technical Implementation Details

The app uses several techniques to handle YouTube's protection:

**1. Signature Decryption ("n challenge")**
- YouTube encrypts video URLs with a signature that changes
- Requires a JS runtime (Deno/Node/Bun) to decrypt
- Without this: "Only images are available for download"

**2. PO Token (Proof of Origin Token)**
- New requirement for "web" and "tv" client media downloads
- Without PO Token: HTTP 403 errors or fallback to 360p format 18
- The included `bgutil-ytdlp-pot-provider` handles this automatically

**3. Client Selection**
- `android`: Best for public videos without authentication
- `web`: Best for member-only content when cookies are present
- `tv_simply`: Fallback for public videos without PO Token

> **Note**: Some videos simply cannot be downloaded due to YouTube's technical restrictions. This is a limitation of YouTube's protection, not the app.

## Troubleshooting

### "n challenge solving failed" or "Only images are available"

This means you're missing a JavaScript runtime required by YouTube's protection:

```bash
# Install Deno (recommended)
brew install deno        # macOS
curl -fsSL https://deno.land/install.sh | sh  # Linux

# Or install Node.js 20+
brew install node        # macOS
sudo apt install nodejs  # Ubuntu/Debian
```

The app automatically detects and uses any available JS runtime (Deno, Node.js, or Bun).

### Videos stuck at low quality (360p format 18)

If downloads fall back to low quality, install the PO Token provider:

```bash
pip install bgutil-ytdlp-pot-provider
```

This package provides PO Tokens needed for full-quality "web" and "tv" client downloads.

### FFmpeg Not Found
If you get an error about FFmpeg not being found:
```bash
# Test if FFmpeg is installed
ffmpeg -version

# If not found, install it:
# macOS:
brew install ffmpeg

# Ubuntu/Debian:
sudo apt update && sudo apt install ffmpeg
```

### "Requested format is not available" Error
This means the video has strong protection:

**Try these solutions in order:**
1. **Restart without cookies** - Sometimes the Android client works better
2. **Restart with cookies** - Use browser authentication
3. **Try a different video** - Some videos simply cannot be downloaded
4. **List available formats** - The app will offer this option when it fails

### "Please sign in" or Authentication Errors

**For age-restricted content:**
```bash
python app.py
# When asked: "Use cookies from browser?" type: y
# Select the browser where you're logged into YouTube
```

**For member-only content:**
- You must be logged into an account that holds the required membership tier
- Cookies alone won't bypass actual membership requirements
- Use the browser profile that's subscribed to the channel

**Make sure you're:**
- Logged into YouTube in the selected browser
- Not in incognito/private mode
- Have proper permissions for the video
- For member-only content: actually a member of that channel

### Connection/Network Errors
- Check your internet connection
- Verify the URL is correct and accessible
- Some videos may be region-restricted
- The app automatically retries 3 times before failing

### Cookie Extraction Issues
If the app can't extract cookies from your browser:

**Try these solutions:**
1. **Close all browser windows** and try again
2. **Use a different browser** (Chrome usually works best)
3. **Update your browser** to the latest version
4. **Export cookies manually** (advanced - see yt-dlp wiki)

### General Download Failures

**Common causes:**
- Video is private or unlisted
- Video has been removed or deleted
- Strong copyright protection
- Geographic restrictions
- Age restrictions (try with cookies)

**The app will offer to:**
- Show available formats for debugging
- Suggest alternative approaches
- Guide you through solutions

### Permission Errors
Make sure you have write permissions in the project directory:
```bash
# On macOS/Linux
chmod +w .
```

## Tips and Best Practices

### 🎯 When to Use Cookies
- **Use cookies**: Age-restricted content, member-only videos, private videos
- **Skip cookies**: Regular public videos (faster and more reliable)
- **cookies.txt file**: Place in project directory for automatic detection

### 🚀 Maximizing Success
1. **Install a JS runtime** - Deno/Node/Bun for YouTube signature decryption
2. **Install PO Token provider** - `pip install bgutil-ytdlp-pot-provider` for full quality
3. **Try without cookies first** - works for 80%+ of videos
4. **Use Chrome cookies** if authentication is needed - most reliable for membership content
5. **Different browsers** - try Chrome, Firefox, or Safari
6. **Test with popular videos** - verify the app works with a simple video first

### 📱 Different URL Formats
The app works with various YouTube URL formats:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- Shortened URLs - all work the same way

### 🎵 Music Videos
Music videos often have strong protection:
- Try without cookies first
- If that fails, try with cookies
- Some music videos simply cannot be downloaded

## Advanced Usage

### Batch Downloads
While in the app, you can download multiple files:
- After each download, choose `y` to continue
- Paste another URL when prompted
- Press `q` when you're done

### Format Debugging
When a download fails, the app offers to show available formats:
- Type `y` when prompted to see formats
- This helps identify why download failed
- Useful for technical troubleshooting

## Limitations

**The app cannot download:**
- YouTube Premium content
- YouTube Originals
- Live streams (while they're live)
- Some very recent uploads (may take 24-48 hours)
- Videos with extremely strict protection

**These are YouTube's restrictions, not app limitations.**

## Deactivating the Virtual Environment

When you're done, deactivate the virtual environment:

```bash
deactivate
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**This project uses yt-dlp**, which is released to the public domain. Please respect the terms of service of the platforms you're downloading from.

**Important**: This tool is for educational purposes and personal use only. Always respect copyright laws and platform terms of service.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.
