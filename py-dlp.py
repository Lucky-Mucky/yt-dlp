import os
import json
import urllib.request
import subprocess

# =========================
# LINKS
# =========================

YT_DLP_URL = "https://github.com/Lucky-Mucky/yt-dlp/raw/refs/heads/main/yt-dlp.exe"

FFMPEG_BASE = "https://raw.githubusercontent.com/Lucky-Mucky/yt-dlp/main/ffmpeg/ffmpeg.exe.part"
FFPROBE_BASE = "https://raw.githubusercontent.com/Lucky-Mucky/yt-dlp/main/ffprobe/ffprobe.exe.part"

MAX_PARTS = 100

# =========================
# PATHS
# =========================

BASE_DIR = os.path.join(os.getenv("APPDATA"), "py-dlp")
BIN_DIR = os.path.join(BASE_DIR, "bin")
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")

YT_DLP_PATH = os.path.join(BASE_DIR, "yt-dlp.exe")
FFMPEG_PATH = os.path.join(BIN_DIR, "ffmpeg.exe")
FFPROBE_PATH = os.path.join(BIN_DIR, "ffprobe.exe")

# =========================
# DEFAULT CONFIG
# =========================

DEFAULT_CONFIG = {
    "output_folder": "Videos",
    "subtitles": False,
    "cookie_browser": "none",
    "concurrent_fragments": 6
}

# =========================
# CONFIG
# =========================

def load_config():
    """
    Loads config from disk. Merges with DEFAULT_CONFIG so any newly added
    keys are automatically present without breaking old config files.
    """
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r") as f:
                data = json.load(f)
            merged = DEFAULT_CONFIG.copy()
            merged.update(data)
            return merged
        except Exception:
            pass
    return DEFAULT_CONFIG.copy()

def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

# =========================
# DOWNLOAD
# =========================

def download(url, path):
    try:
        urllib.request.urlretrieve(url, path)
        return True
    except Exception:
        return False

# =========================
# MERGE PARTS
# =========================

def download_and_merge(base_url, output_path):
    parts = []

    for i in range(MAX_PARTS):
        part_name = f"{os.path.basename(output_path)}.part{i:03}"
        url = base_url + f"{i:03}"
        part_path = os.path.join(BIN_DIR, part_name)

        if download(url, part_path):
            parts.append(part_path)
        else:
            break

    if not parts:
        return False

    with open(output_path, "wb") as out:
        for part in parts:
            with open(part, "rb") as f:
                out.write(f.read())

    for part in parts:
        os.remove(part)

    return True

# =========================
# SETUP
# =========================

def setup():
    os.makedirs(BIN_DIR, exist_ok=True)

    subprocess.call(["attrib", "+h", BASE_DIR],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL)

    did_install = False

    if not os.path.exists(YT_DLP_PATH):
        if download(YT_DLP_URL, YT_DLP_PATH):
            did_install = True

    if not os.path.exists(FFMPEG_PATH):
        if download_and_merge(FFMPEG_BASE, FFMPEG_PATH):
            did_install = True

    if not os.path.exists(FFPROBE_PATH):
        if download_and_merge(FFPROBE_BASE, FFPROBE_PATH):
            did_install = True

    return did_install

# =========================
# MENU UI
# =========================

def clear():
    os.system("cls")

def menu(config):
    clear()
    subs    = "ON"  if config["subtitles"]           else "OFF"
    cookies = config["cookie_browser"].capitalize()
    folder  = config["output_folder"]

    print("=" * 35)
    print("      YT DOWNLOADER")
    print("=" * 35)
    print("1. Download Video (MP4)")
    print("2. Download Audio (MP3)")
    print("3. Batch Download (from .txt)")
    print("4. Settings")
    print("5. Exit")
    print("=" * 35)
    print(f" Folder  : {folder}")
    print(f" Subs    : {subs}  |  Cookies: {cookies}")
    print("=" * 35)

# =========================
# SETTINGS MENU
# =========================

def settings_menu(config):
    while True:
        clear()
        subs = "ON" if config["subtitles"] else "OFF"
        print("=" * 35)
        print("      SETTINGS")
        print("=" * 35)
        print(f"1. Output folder   [{config['output_folder']}]")
        print(f"2. Subtitles       [{subs}]")
        print(f"3. Cookie browser  [{config['cookie_browser']}]")
        print("4. Back")
        print("=" * 35)

        choice = input("Select option: ").strip()

        if choice == "1":
            folder = input(f"\nOutput folder [{config['output_folder']}]: ").strip()
            if folder:
                config["output_folder"] = folder
                save_config(config)

        elif choice == "2":
            config["subtitles"] = not config["subtitles"]
            save_config(config)

        elif choice == "3":
            valid_browsers = ["none", "chrome", "firefox", "edge", "brave", "opera"]
            print(f"\nOptions: {', '.join(valid_browsers)}")
            browser = input(f"Cookie browser [{config['cookie_browser']}]: ").strip().lower()
            if browser in valid_browsers:
                config["cookie_browser"] = browser
                save_config(config)
            else:
                print("Invalid choice. No change.")
                input("Press Enter to continue...")

        elif choice == "4":
            break

    return config

# =========================
# QUALITY SELECTOR
# =========================

# Format strings map to yt-dlp -f values.
# Fallback /best covers cases where separate streams aren't available.
QUALITY_OPTIONS = {
    "1": ("Best",  "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best"),
    "2": ("1080p", "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]"),
    "3": ("720p",  "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]"),
    "4": ("480p",  "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480]"),
}

def select_quality():
    """
    Returns (label, format_string) for the chosen quality.
    Defaults to Best if the user just hits Enter.
    """
    print("\nQuality:")
    for key, (label, _) in QUALITY_OPTIONS.items():
        print(f"  {key}. {label}")

    choice = input("Select quality [1]: ").strip() or "1"
    return QUALITY_OPTIONS.get(choice, QUALITY_OPTIONS["1"])

# =========================
# CLIP TRIMMER
# =========================

def get_clip_range():
    """
    Prompts for optional start/end timestamps.
    Returns a --download-sections value string, or None to skip trimming.
    Accepts HH:MM:SS, MM:SS, or bare seconds.
    """
    print("\nClip trimmer — press Enter on both to skip:")
    start = input("  Start time (e.g. 00:01:30): ").strip()
    end   = input("  End time   (e.g. 00:02:45): ").strip()

    if start and end:
        return f"*{start}-{end}"
    return None

# =========================
# PLAYLIST SUPPORT
# =========================

def get_playlist_count(url):
    """
    Uses yt-dlp's flat-playlist mode to fetch the total number of items
    in a playlist without downloading anything.
    Returns an int count, or None if the URL is not a playlist or lookup fails.
    """
    result = subprocess.run(
        [YT_DLP_PATH, "--flat-playlist", "--print", "%(playlist_count)s", url],
        capture_output=True,
        text=True
    )
    # yt-dlp prints the count once per item; grab the first valid digit line
    lines = [l.strip() for l in result.stdout.strip().splitlines() if l.strip().isdigit()]
    if lines:
        count = int(lines[0])
        if count > 1:
            return count
    return None

# =========================
# BUILD BASE FLAGS
# =========================

def build_base_flags(config, output_template, is_playlist=False):
    """
    Assembles the yt-dlp flags shared across all download modes.

    Playlist mode skips --quiet so yt-dlp's native "[X/Y] Downloading..."
    lines are visible, giving the user real progress on multi-video queues.

    Single video mode uses a custom progress template for a cleaner look.
    """
    flags = [
        "--ffmpeg-location", BIN_DIR,
        "--concurrent-fragments", str(config["concurrent_fragments"]),
        "--buffer-size", "16K",
        "--no-part",
        "-o", output_template,
        "--progress",
    ]

    if is_playlist:
        # Native output shows "Downloading item X of Y" — don't suppress it
        pass
    else:
        flags += [
            "--quiet",
            "--progress-template",
            "%(progress._percent_str)s %(progress._speed_str)s %(progress._eta_str)s"
        ]

    # Cookie support — pulls cookies directly from the specified browser profile
    if config["cookie_browser"] != "none":
        flags += ["--cookies-from-browser", config["cookie_browser"]]

    # Subtitle support — writes .vtt alongside the video if subs are available
    # yt-dlp silently skips this if the video has no subtitles in the chosen lang
    if config["subtitles"]:
        flags += ["--write-subs", "--sub-lang", "en"]

    return flags

# =========================
# DOWNLOAD FUNCTION
# =========================

def download_video(mode, config):
    url = input("\nPaste YouTube link: ").strip()
    if not url:
        return

    print("\nChecking URL...\n")

    # Detect playlist before doing anything else
    playlist_count = get_playlist_count(url)
    is_playlist = playlist_count is not None

    if is_playlist:
        print(f"Playlist detected — {playlist_count} videos.")
        confirm = input("Download full playlist? (y/N): ").strip().lower()
        if confirm != "y":
            input("\nCancelled. Press Enter to return to menu...")
            return
        # Nest playlist items in a subfolder named after the playlist
        output_template = os.path.join(
            config["output_folder"],
            "%(playlist_title)s",
            "%(playlist_index)02d - %(title)s.%(ext)s"
        )
    else:
        result = subprocess.run(
            [YT_DLP_PATH, "--get-title", "--no-playlist", url],
            capture_output=True,
            text=True
        )
        title = result.stdout.strip() or "Unknown Title"
        print("=" * 35)
        print(f"Downloading: {title}")
        print("=" * 35 + "\n")
        output_template = os.path.join(config["output_folder"], "%(title)s.%(ext)s")

    # Quality selection (MP4 only — audio always grabs best available)
    quality_fmt = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best"
    if mode == "mp4":
        _, quality_fmt = select_quality()

    clip_range = get_clip_range()

    os.makedirs(config["output_folder"], exist_ok=True)

    base_flags = build_base_flags(config, output_template, is_playlist)

    if mode == "mp4":
        cmd = [
            YT_DLP_PATH, url,
            "-f", quality_fmt,
            "--merge-output-format", "mp4",
            *base_flags
        ]
    else:
        cmd = [
            YT_DLP_PATH, url,
            "-x",
            "--audio-format", "mp3",
            *base_flags
        ]

    # Explicitly enforce playlist/single-video behaviour
    cmd += ["--yes-playlist"] if is_playlist else ["--no-playlist"]

    if clip_range:
        cmd += ["--download-sections", clip_range]

    subprocess.run(cmd)

    print("\nDone.")
    input("\nPress Enter to return to menu...")

# =========================
# BATCH DOWNLOAD
# =========================

def batch_download(config):
    """
    Reads a plain-text file of URLs (one per line, # for comments) and
    passes the whole list to yt-dlp via its -a flag.
    Playlist URLs in the batch file are treated as single entries;
    users should expand playlists manually or use the playlist flow instead.
    """
    clear()
    print("=" * 35)
    print("      BATCH DOWNLOAD")
    print("=" * 35)
    print("One URL per line. Lines starting with # are skipped.\n")

    txt_path = input("Path to .txt file: ").strip().strip('"')

    if not txt_path or not os.path.exists(txt_path):
        print("\nFile not found.")
        input("Press Enter to return to menu...")
        return

    with open(txt_path, "r") as f:
        urls = [l.strip() for l in f if l.strip() and not l.strip().startswith("#")]

    if not urls:
        print("\nNo URLs found in file.")
        input("Press Enter to return to menu...")
        return

    print(f"\nFound {len(urls)} URL(s).\n")

    # Mode
    print("Mode:")
    print("  1. Video (MP4)")
    print("  2. Audio (MP3)")
    mode_choice = input("Select [1]: ").strip() or "1"
    mode = "mp4" if mode_choice == "1" else "mp3"

    quality_fmt = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best"
    if mode == "mp4":
        _, quality_fmt = select_quality()

    clip_range = get_clip_range()

    output_template = os.path.join(config["output_folder"], "%(title)s.%(ext)s")
    os.makedirs(config["output_folder"], exist_ok=True)

    base_flags = build_base_flags(config, output_template, is_playlist=False)

    if mode == "mp4":
        cmd = [
            YT_DLP_PATH,
            "-a", txt_path,
            "-f", quality_fmt,
            "--merge-output-format", "mp4",
            *base_flags
        ]
    else:
        cmd = [
            YT_DLP_PATH,
            "-a", txt_path,
            "-x",
            "--audio-format", "mp3",
            *base_flags
        ]

    if clip_range:
        cmd += ["--download-sections", clip_range]

    print(f"\nStarting batch download — {len(urls)} file(s)...\n")
    subprocess.run(cmd)

    print("\nBatch complete.")
    input("\nPress Enter to return to menu...")

# =========================
# MAIN
# =========================

if __name__ == "__main__":
    first_run = setup()
    config = load_config()

    if first_run:
        clear()

    while True:
        menu(config)
        choice = input("Select option: ").strip()

        if choice == "1":
            download_video("mp4", config)
        elif choice == "2":
            download_video("mp3", config)
        elif choice == "3":
            batch_download(config)
        elif choice == "4":
            config = settings_menu(config)
        elif choice == "5":
            break
        else:
            input("Invalid option. Press Enter...")
