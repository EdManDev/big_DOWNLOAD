# big_DOWNLOAD

A simple Python application to download videos and audio from YouTube and other supported platforms using yt-dlp.

## Features

- **Download videos** in MP4 format with best available quality
- **Download audio** in MP3 format with high-quality extraction (192 kbps)
- **Cookie authentication** support for age-restricted and member-only content
- **Smart client selection** - automatically chooses the best download method
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
python3 -m pip install -r requirements.txt
python3 app.py
```

### Windows:
```cmd
cd big_DOWNLOAD
rmdir /s /q venv
python -m venv venv
venv\Scripts\activate
python -m pip install -r requirements.txt
python app.py
```

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- FFmpeg (required for audio extraction and video merging)

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
pip install -r requirements.txt
```

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

1. **Cookie authentication**: Choose whether to use browser cookies for restricted content
2. **Browser selection**: If using cookies, select your browser (chrome, firefox, safari, etc.)
3. **Enter the YouTube URL**: Paste the link to the video you want to download
4. **Choose download type**: Type either `audio` or `video`
5. **Continue or exit**: Choose to download more files or exit the app

Example session:
```
🍪 Some videos require authentication (age-restricted, etc.)
Use cookies from browser for authentication? (y/n, default: n): n

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
- Download member-only videos
- Support for private videos (if you have access)
- Supports: Chrome, Firefox, Safari, Edge, Opera, Brave, Chromium

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

> **Note**: Some videos simply cannot be downloaded due to YouTube's technical restrictions. This is a limitation of YouTube's protection, not the app.

## Troubleshooting

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

**Make sure you're:**
- Logged into YouTube in the selected browser
- Not in incognito/private mode
- Have proper permissions for the video

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

### 🚀 Maximizing Success
1. **Try without cookies first** - works for 80%+ of videos
2. **Use Chrome cookies** if authentication is needed - most reliable
3. **Different browsers** - try Chrome, Firefox, or Safari
4. **Test with popular videos** - verify the app works with a simple video first

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
