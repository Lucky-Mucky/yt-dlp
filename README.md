██╗   ██╗████████╗    ██████╗  ██████╗ ██╗    ██╗███╗   ██╗██╗      ██████╗  █████╗ ██████╗ ███████╗██████╗
╚██╗ ██╔╝╚══██╔══╝    ██╔══██╗██╔═══██╗██║    ██║████╗  ██║██║     ██╔═══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗
 ╚████╔╝    ██║       ██║  ██║██║   ██║██║ █╗ ██║██╔██╗ ██║██║     ██║   ██║███████║██║  ██║█████╗  ██████╔╝
  ╚██╔╝     ██║       ██║  ██║██║   ██║██║███╗██║██║╚██╗██║██║     ██║   ██║██╔══██║██║  ██║██╔══╝  ██╔══██╗
   ██║      ██║       ██████╔╝╚██████╔╝╚███╔███╔╝██║ ╚████║███████╗╚██████╔╝██║  ██║██████╔╝███████╗██║  ██║
   ╚═╝      ╚═╝       ╚═════╝  ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝

  A lightweight, zero-install YouTube downloader for Windows.
  Powered by yt-dlp + ffmpeg. No browser extension. No bloat.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  OVERVIEW
  ────────────────────────────────────────────────────────────────────────────────────────────────────────────

  YT Downloader is a simple terminal-based tool for downloading YouTube videos and audio.
  No installation required — just run the script and it handles everything else automatically.

  All binaries (yt-dlp, ffmpeg, ffprobe) are downloaded silently on first run and stored in:

      %APPDATA%\ytdownloader\

  The folder is hidden automatically. Nothing is written to your system PATH.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  REQUIREMENTS
  ────────────────────────────────────────────────────────────────────────────────────────────────────────────

    • Windows 10 / 11
    • Python 3.8 or newer           →  https://python.org/downloads
    • Internet connection (first run only for binary setup)

  No pip packages required. The script uses only Python standard library modules.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  GETTING STARTED
  ────────────────────────────────────────────────────────────────────────────────────────────────────────────

  1. Download or clone this repository.

  2. Run the script:

         python ytdownloader.py

  3. On first launch, yt-dlp and ffmpeg will be downloaded automatically.
     This only happens once. Subsequent launches start instantly.

  4. Use the menu to download video or audio.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  FEATURES
  ────────────────────────────────────────────────────────────────────────────────────────────────────────────

    [1]  Download Video (MP4)
         ├─ Quality selector: Best / 1080p / 720p / 480p
         ├─ Clip trimmer: specify start and end timestamps to grab only a section
         └─ Playlist support: detects playlist URLs and downloads all items into a named subfolder

    [2]  Download Audio (MP3)
         ├─ Extracts and converts audio using ffmpeg
         └─ Clip trimmer available here too

    [3]  Batch Download
         ├─ Point to a .txt file with one URL per line
         ├─ Lines starting with # are treated as comments and skipped
         └─ Mode, quality, and clip range are applied to the entire batch

    [4]  Settings
         ├─ Output folder    — set a custom save directory (default: Videos/)
         ├─ Subtitles        — toggle English subtitle download (.vtt alongside video)
         └─ Cookie browser   — select a browser to pull cookies from for restricted content


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  SETTINGS
  ────────────────────────────────────────────────────────────────────────────────────────────────────────────

  Settings are saved automatically to:

      %APPDATA%\ytdownloader\config.json

  ┌─────────────────────┬──────────────────────────────────────────────────────────────────┐
  │ Key                 │ Description                                                      │
  ├─────────────────────┼──────────────────────────────────────────────────────────────────┤
  │ output_folder       │ Where downloaded files are saved. Default: Videos               │
  │ subtitles           │ Download English subtitles alongside video. Default: false       │
  │ cookie_browser      │ Browser to pull cookies from. Default: none                     │
  └─────────────────────┴──────────────────────────────────────────────────────────────────┘

  Supported cookie browsers:  chrome  |  firefox  |  edge  |  brave  |  opera  |  none


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  BATCH DOWNLOAD — FILE FORMAT
  ────────────────────────────────────────────────────────────────────────────────────────────────────────────

  Create a plain .txt file with one URL per line. Example:

      # Music
      https://www.youtube.com/watch?v=XXXXXXXXXXX
      https://www.youtube.com/watch?v=YYYYYYYYYYY

      # Tutorials
      https://www.youtube.com/watch?v=ZZZZZZZZZZZ

  Then select option 3 from the main menu and provide the path to that file.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  CLIP TRIMMER
  ────────────────────────────────────────────────────────────────────────────────────────────────────────────

  After pasting a URL, you will be prompted for optional start and end times.
  Press Enter on both to skip trimming and download the full video.

  Accepted formats:

      HH:MM:SS    →    01:30:00
      MM:SS       →    02:45
      Seconds     →    90

  Example — grab only the 1:30 to 2:45 mark of a video:

      Start time: 00:01:30
      End time:   00:02:45


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  COOKIE SUPPORT
  ────────────────────────────────────────────────────────────────────────────────────────────────────────────

  Some videos are age-restricted or members-only. To download these, set your browser
  in Settings. YT Downloader will pull cookies directly from that browser's profile.

  ⚠  Close the target browser before downloading with cookie mode enabled.
     Chrome in particular locks its cookie database while running, which will cause an error.
     Firefox is generally more permissive and can be left open.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  FILE STRUCTURE
  ────────────────────────────────────────────────────────────────────────────────────────────────────────────

  Repository:

      yt-downloader/
      ├── ytdownloader.py       ← main script
      └── README.txt            ← this file

  Runtime (auto-created, hidden):

      %APPDATA%\ytdownloader\
      ├── yt-dlp.exe
      ├── config.json
      └── bin\
          ├── ffmpeg.exe
          └── ffprobe.exe

  Downloads (relative to where you run the script):

      Videos\
      ├── Video Title.mp4
      ├── Song Title.mp3
      └── Playlist Name\
          ├── 01 - First Video.mp4
          └── 02 - Second Video.mp4


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  TROUBLESHOOTING
  ────────────────────────────────────────────────────────────────────────────────────────────────────────────

  ┌─ Script opens and closes immediately
  │   Run it from a terminal: python ytdownloader.py
  │   Do not double-click the .py file directly.

  ┌─ "python is not recognized"
  │   Python is not installed or not on your PATH.
  │   Download from https://python.org — check "Add to PATH" during install.

  ┌─ Download fails with HTTP error
  │   The video may be age-restricted. Enable cookie support in Settings.
  │   Make sure your browser is signed into YouTube.

  ┌─ Cookie error from Chrome
  │   Chrome locks its cookie database while running. Close Chrome and retry.

  ┌─ ffmpeg merge fails / no audio in output
  │   The binaries may be corrupted. Delete %APPDATA%\ytdownloader\ and relaunch.
  │   The setup will re-download everything cleanly.

  ┌─ Subtitles not appearing
  │   Not all videos have subtitles. Auto-generated captions may or may not be
  │   available depending on the channel. The download will succeed either way.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  BUILT WITH
  ────────────────────────────────────────────────────────────────────────────────────────────────────────────

    • yt-dlp       https://github.com/yt-dlp/yt-dlp
    • ffmpeg       https://ffmpeg.org
    • Python       https://python.org


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


  LICENSE
  ────────────────────────────────────────────────────────────────────────────────────────────────────────────

  MIT License — do whatever you want with it.


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
