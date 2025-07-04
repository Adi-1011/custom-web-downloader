import yt_dlp
import subprocess
import os

def custom_download(url, download_path, filename="video_output"):
    temp_file = "__temp_download"

    print("🎬 [YT-DLP Pro] Starting download and re-encode...")
    print(f"📂 Download Path: {download_path}")
    print(f"🔗 URL: {url}")
    print(f"💾 Output: {filename}.mp4")

    # Step 1: yt-dlp download
    ydl_opts = {
        'format': 'bv+ba/b',
        'merge_output_format': 'mp4',
        'restrictfilenames': True,
        'noplaylist': True,
        'force_overwrites': True,
        'outtmpl': os.path.join(download_path, f"{temp_file}.%(ext)s")
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        raise RuntimeError(f"❌ yt-dlp download failed: {e}")

    # Step 2: Re-encode using FFmpeg
    downloaded_file = None
    for ext in ['mp4', 'mkv', 'webm']:
        temp_path = os.path.join(download_path, f"{temp_file}.{ext}")
        if os.path.exists(temp_path):
            downloaded_file = temp_path
            break

    if not downloaded_file:
        raise FileNotFoundError("❌ Could not find the downloaded file for re-encoding.")

    final_output_path = os.path.join(download_path, f"{filename}.mp4")

    ffmpeg_cmd = [
        'ffmpeg', '-y',
        '-i', downloaded_file,
        '-c:v', 'libx264',
        '-preset', 'fast',
        '-crf', '23',
        '-profile:v', 'high',
        '-level', '4.2',
        '-pix_fmt', 'yuv420p',
        '-c:a', 'aac',
        '-b:a', '192k',
        final_output_path
    ]

    try:
        subprocess.run(ffmpeg_cmd, check=True)
        os.remove(downloaded_file)
        print("✅ Re-encode complete! Premiere Pro-ready.")
        print(f"📁 Saved to: {final_output_path}")
    except Exception as e:
        raise RuntimeError(f"❌ FFmpeg re-encoding failed: {e}")
